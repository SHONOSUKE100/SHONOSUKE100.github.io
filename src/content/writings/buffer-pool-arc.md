---
title: "LRU vs. LFU vs. ARC: Which One Wins on Hit Rate?"
locale: en
description: "Comparing the cache replacement policies used in database buffer pools with experiments on four workloads"
publishedAt: 2026-11-22
category: "engineering-systems"
tags: ["database", "cache", "algorithm"]
draft: false
---

## What a 1% Difference in Hit Rate Does

Whether a database is fast often comes down to one question: was the data it needed already in memory?

Reading from memory takes about 100 nanoseconds. Reading from an SSD takes about 100 microseconds, a thousand times longer. If we call the fraction of reads served from memory the **hit rate**, the average time per read is roughly:

```text
average time = hit rate × 0.1µs + (1 − hit rate) × 100µs
```

At a 99% hit rate the average is about 1.1µs. At 98% it is about 2.1µs. Drop the hit rate by just one point and the average read time nearly doubles. That is how expensive the 100µs of a miss is.

This is why databases put so much care into deciding what to keep in their limited memory and what to evict. In this post I implement three of these decisions, called replacement policies — LRU, LFU, and ARC — and compare their hit rates on four kinds of workloads.

Here is the conclusion up front.

> Which eviction policy works best depends on the workload. ARC uses "did I regret evicting that?" as its signal and tunes the balance by itself.

## What a Buffer Pool Is

A database handles data on disk in fixed-size chunks called **pages** (8KB in PostgreSQL). Pages read from disk are kept in a dedicated area of memory. That area is the **buffer pool**.

![How the in-memory buffer pool relates to disk. When a query asks for page 2, the page table shows it is in frame 1. If it were not there, the page would be read from disk into a free frame](/images/writings/buffer-pool-arc/en/buffer-pool.svg)

*Figure 1: Buffer pool layout*

A buffer pool consists of an array of slots that hold pages (**frames**) and a table recording which page is in which frame (the **page table**). When a query requests a page, the buffer pool first checks the page table.

- If the page is there, it is a **hit**, and the page in memory is returned as is.
- If not, it is a **miss**. The page is read from disk and placed in a free frame.

There are only so many frames, so the pool eventually fills up. At that point one page has to be evicted to make room. The rule for choosing which page to evict is the replacement policy, and it is the subject of this post. PostgreSQL's `shared_buffers` and MySQL InnoDB's `innodb_buffer_pool_size` are the settings that size this buffer pool.

Real databases have more rules, such as "never evict a page that is in use (pinned)" and "write a modified (dirty) page back to disk before evicting it." This post only compares hit rates, so I leave those out.

## The Experiment Setup

I wrote a small simulator in Python. It takes a sequence of page IDs one at a time and counts how many are hits. There is no disk and no threading. The cache holds 100 pages, the workloads use 1,000 distinct pages in normal operation, and each workload makes 100,000 accesses.

As a baseline I also measure **OPT** (Belady's optimal policy). OPT evicts the page whose next use is furthest in the future, so it can only run if it knows every future access. It cannot be built in practice, but it gives an upper bound: no policy can beat its hit rate.

I prepared four workloads.

![Access patterns of the four workloads. The x-axis is the access number and the y-axis is the page ID. W1 is random access skewed toward popular pages, W2 is a sawtooth that reads 150 pages in order over and over, W3 is W1 mixed with scan pages that are read only once, and W4 swaps its whole set of popular pages halfway through](/images/writings/buffer-pool-arc/en/workloads.svg)

*Figure 2: Access patterns of the four workloads*

| # | Name | What it does | Real-world analogy |
| --- | --- | --- | --- |
| W1 | Skewed | Accesses concentrate on a few popular pages (Zipf distribution) | Everyday transactions of a web service (OLTP) |
| W2 | Looping scan | Reads 150 pages, slightly more than the cache holds, in order, many times | A join that rereads the same table |
| W3 | Skewed + scans | W1 running alongside a batch job that reads pages in order, each only once (about 1/3 of accesses) | An analytics batch running behind daytime OLTP |
| W4 | Shifting hot set | Halfway through, the set of popular pages is replaced by an entirely different set | A sale starting, or a trend changing |

In a Zipf distribution, the k-th most popular page is chosen with probability proportional to 1/k, so a small number of pages get most of the accesses.

The scan pages in W3 appear only once, so every policy misses on them. For W3 I therefore measure the hit rate of the regular accesses only, excluding the scan. What I want to see is how much the regular accesses' hit rate drops while the batch is running.

## The Two Classics: LRU and LFU

### LRU: What You Used Recently, You Will Use Again Soon

LRU (Least Recently Used) evicts the page that was used longest ago. The bet is that pages used recently will be used again soon.

All it needs is to keep pages in the order they were used, so with Python's `OrderedDict` it takes about a dozen lines.

```python
from collections import OrderedDict

class LRU:
    def __init__(self, capacity):
        self.capacity = capacity
        self.pages = OrderedDict()  # head is the oldest, tail is the newest

    def access(self, page):
        if page in self.pages:
            self.pages.move_to_end(page)  # hit: move to the newest position
            return True
        if len(self.pages) >= self.capacity:
            self.pages.popitem(last=False)  # full: evict the oldest page
        self.pages[page] = None
        return False
```

Reordering on every access is expensive, so real databases often use CLOCK, a lighter approximation of LRU. PostgreSQL's clock-sweep belongs to this family. It keeps a single "recently used" bit per page, sweeps over the pages like the hand of a clock, and evicts the first page whose bit is not set.

### LFU: What Is Used Often Will Keep Being Used

LFU (Least Frequently Used) evicts the page that has been used the fewest times. The bet is that popular pages will stay popular. In my implementation, ties go to the page used longest ago, and the count of an evicted page is forgotten.

### Round 1 Results

![Hit rates of LRU, LFU, and OPT. W1: LRU 58%, LFU 67%, OPT 75%. W2: LRU and LFU 0%, OPT 66%. W3: LRU 48%, LFU 65%, OPT 75%. W4: LRU 57%, LFU 34%, OPT 75%](/images/writings/buffer-pool-arc/en/round1.svg)

*Figure 3: Round 1 hit rates (LRU, LFU, OPT)*

In W1, where the set of popular pages never changes, LFU's counting pays off: it scores 67% against LRU's 58%.

The big gaps open up in W3 and W4, and the loser switches sides between them.

In W3 it is LRU that drops sharply, from 58% in W1 to 48% once the batch scan is mixed in. Scan pages are never used again, yet LRU keeps them as recently used pages and evicts popular pages that are used again and again instead. This is known as sequential flooding. LFU throws away the scan pages first, since their count is 1, and holds at 65%.

In W4 the roles reverse and LFU falls to 34%. The popular pages from the first half keep their large counts, so they are never evicted, while each new popular page from the second half becomes the next eviction target while its count is still 1. Under LRU, the old popular pages stop being used and get evicted oldest first, so it reaches 57%, about the same as in W1.

Both score 0% on W2. I come back to that in the discussion.

LRU looks only at whether a page was used recently, LFU only at how many times it was used, and each has a case where its hit rate falls sharply. Ideally we would use both kinds of information and switch between them as the situation demands. That is what ARC does.

## ARC: A Cache That Learns from Regret

### The Idea

ARC (Adaptive Replacement Cache) is a replacement policy published in 2003 by Nimrod Megiddo and Dharmendra Modha of IBM.

It rests on two ideas. First, split the cache into a group of pages used once and a group of pages used twice or more. The first covers recency, where LRU is strong, and the second covers frequency, where LFU is strong. Second, adjust how many pages each group gets automatically, to fit the workload.

The signal for that adjustment is whether a page it evicted turned out to be needed again.

### Four Lists

ARC keeps four lists.

![The four lists of ARC. From left to right: B1, T1, T2, B2. T1 and T2 hold the cached pages, c pages in total. B1 and B2 are ghosts that remember only the IDs of evicted pages. The border between T1 and T2 moves with p](/images/writings/buffer-pool-arc/en/arc-lists.svg)

*Figure 4: The four lists of ARC*

| List | Contents |
| --- | --- |
| T1 | Pages used once (the recent group) |
| T2 | Pages used twice or more (the frequent group) |
| B1 | Only the IDs of pages evicted from T1 (ghosts) |
| B2 | Only the IDs of pages evicted from T2 (ghosts) |

The pages actually in the cache are those in T1 and T2, and together they fill the cache's capacity c. B1 and B2 are called **ghost lists**. They do not hold page contents, only IDs, so they take almost no memory.

ARC also keeps a value called **p**. It is the target size for T1, the number of pages ARC would like T1 to have, and it marks the border between T1 and T2. The larger p is, the more ARC favors the recent group; the smaller, the more it favors the frequent group.

### Ghost Lists Are a "Regret Sensor"

To me, the most interesting part of ARC is how it uses its ghost lists.

Suppose a requested page is not in the cache, but its ID is still in B1. A page evicted from the recent group was needed again shortly afterward. ARC evicted recent pages too early — that is the regret. So ARC increases p and gives T1 more room.

If the ID is in B2 instead, ARC evicted frequent pages too early. This time it decreases p and gives T2 more room.

How far p moves depends on the size ratio to the opposite ghost list. On a hit in B1, p grows by `max(|B2| / |B1|, 1)`, so a hit in the smaller ghost list moves p further.

In other words, the ghost lists are a "regret sensor": they measure whether past eviction decisions were wrong and use that to change the next decision.

### The Four Cases on Each Access

When ARC accesses page x, what it does depends on where x is.

![Flowchart of the four cases when ARC accesses a page. If the page is in T1 or T2, it is a hit and moves to the head of T2. If it is in B1, increase p; if in B2, decrease p; evict one page and put it at the head of T2. If it is nowhere, evict if full and put it at the head of T1](/images/writings/buffer-pool-arc/en/arc-flow.svg)

*Figure 5: The four cases on each access*

1. In T1 or T2 (a hit): move it to the head of T2. It has now been used at least twice, so it joins the frequent group.
2. In B1: increase p, evict one page to make room, then put x at the head of T2.
3. In B2: decrease p, then do the same as in case 2.
4. Nowhere: if the cache is full, evict one page, then put x at the head of T1.

When evicting, ARC takes the tail of T1 if T1 is larger than p, and the tail of T2 otherwise, and moves that page's ID to B1 or B2 accordingly. p is the yardstick that decides which group to evict from next.

### Tracing It by Hand

Let's feed the sequence `A B C A D B E A` to a cache of capacity 3. In each list, the left end is the head (newest) and the right end is the tail (oldest). I produced this table by running the implementation shown later.

| # | Access | Result | T1 | T2 | B1 | B2 | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A | New | A | | | | 0 |
| 2 | B | New | B A | | | | 0 |
| 3 | C | New | C B A | | | | 0 |
| 4 | A | Hit | C B | A | | | 0 |
| 5 | D | New | D C | A | B | | 0 |
| 6 | B | Hit in B1 | D | B A | C | | 1 |
| 7 | E | New | E D | B | C | A | 1 |
| 8 | A | Hit in B2 | E | A B | D C | | 0 |

The fourth access, A, is in T1, so it hits, and since this is its second use it moves to T2.

The first eviction happens at D, once the cache is full. T1's size (2) is larger than p (0), so B at the tail of T1 is evicted and its ID stays in B1. The very next access is B, which is still in B1. Recent pages were evicted too early, so p rises from 0 to 1. To make room, C at the tail of T1 is evicted, and B goes into T2 because this is its second use.

At E, T1's size (1) does not exceed p (1), so the page evicted is A at the tail of T2, and its ID stays in B2. When A is accessed at the end, ARC learns it evicted a frequent page too early, and p goes back from 1 to 0.

You can watch p move back and forth with the access pattern.

### Implementation

Following the paper's procedure directly in Python gives about 70 lines. Each list is an `OrderedDict` whose head is the old side (where evictions happen) and whose tail is the new side.

```python
from collections import OrderedDict

class ARC:
    def __init__(self, capacity):
        self.c = capacity
        self.p = 0.0  # target size of T1
        self.t1, self.t2 = OrderedDict(), OrderedDict()
        self.b1, self.b2 = OrderedDict(), OrderedDict()

    def _replace(self, in_b2):
        # Evict from T1 if it is larger than the target p, otherwise from T2, and keep the ID as a ghost
        if self.t1 and ((in_b2 and len(self.t1) == self.p) or len(self.t1) > self.p):
            old, _ = self.t1.popitem(last=False)
            self.b1[old] = None
        else:
            old, _ = self.t2.popitem(last=False)
            self.b2[old] = None

    def access(self, x):
        # Case 1: in the cache (hit) -> head of T2
        if x in self.t1:
            del self.t1[x]
            self.t2[x] = None
            return True
        if x in self.t2:
            self.t2.move_to_end(x)
            return True

        # Case 2: in B1 -> "evicted recent pages too early", so increase p
        if x in self.b1:
            self.p = min(self.c, self.p + max(len(self.b2) / len(self.b1), 1))
            self._replace(in_b2=False)
            del self.b1[x]
            self.t2[x] = None
            return False

        # Case 3: in B2 -> "evicted frequent pages too early", so decrease p
        if x in self.b2:
            self.p = max(0.0, self.p - max(len(self.b1) / len(self.b2), 1))
            self._replace(in_b2=True)
            del self.b2[x]
            self.t2[x] = None
            return False

        # Case 4: nowhere -> head of T1
        l1 = len(self.t1) + len(self.b1)
        total = l1 + len(self.t2) + len(self.b2)
        if l1 == self.c:
            if len(self.t1) < self.c:
                self.b1.popitem(last=False)
                self._replace(in_b2=False)
            else:
                self.t1.popitem(last=False)
        elif l1 < self.c and total >= self.c:
            if total == 2 * self.c:
                self.b2.popitem(last=False)
            self._replace(in_b2=False)
        self.t1[x] = None
        return False
```

The branches in case 4 look a bit involved. Their job is to stop the ghost lists from growing without bound. ARC keeps T1 plus B1 at no more than c, and all four lists together at no more than 2c: the history of the recent group never exceeds one cache's worth, and everything including ghosts never exceeds two. When an access would break this rule, the oldest ghost is dropped first.

I confirmed that the implementation keeps this rule with a test that checks it after every one of 100,000 accesses.

## Round 2: Adding ARC

![Hit rates of LRU, LFU, ARC, and OPT. ARC scores 64% on W1, 0% on W2, 66% on W3, and 64% on W4](/images/writings/buffer-pool-arc/en/round2.svg)

*Figure 6: Round 2 hit rates (with ARC)*

| Workload | LRU | LFU | ARC | OPT |
| --- | ---: | ---: | ---: | ---: |
| W1 Skewed | 57.7% | **66.6%** | 64.1% | 75.5% |
| W2 Looping scan | 0.0% | 0.0% | 0.0% | 66.3% |
| W3 Skewed + scans | 48.1% | 64.9% | **65.7%** | 75.4% |
| W4 Shifting hot set | 57.5% | 34.0% | **63.9%** | 75.4% |

ARC loses slightly to LFU on W1, but beats both LRU and LFU on W3 and W4. On W3, where LRU's hit rate dropped, and on W4, where LFU's dropped, ARC stays at 64–66%. Never losing badly on any workload is ARC's strength.

### Watching p Move

To see how ARC actually adjusts, let's look at p over time.

![p over time in ARC. The thin line is the actual value and the thick line is a moving average. On W1 and W3, p settles below 10. On W2 it stays at 0. On W4, p jumps right after the hot set changes and then comes back down](/images/writings/buffer-pool-arc/en/arc-p.svg)

*Figure 7: p over time in ARC*

On W1 and W3, p settles at small values below 10. That means ARC gives 90 or more of the cache's 100 pages to the frequent group (T2). In W3, scan pages enter T1 and are evicted from its tail without ever being used again. Nothing is evicted from T2, where the popular pages live, so the sequential flooding that hurt LRU does not happen.

On W4, p jumps right after the hot set changes. Because p is small, each new popular page that enters T1 is evicted from the tail of T1 at the next eviction. But it is popular, so it is accessed again soon and found in B1, again and again. ARC reads this as "evicted recent pages too early" and temporarily gives T1 more room. Once the new popular pages have moved into T2, p comes back down. Where LFU lost hit rate because of stale counts, ARC used the number of hits in B1 to shift the balance.

This is what I mean by "learning from regret."

## Discussion

### Where ARC Loses Too: The Looping Scan

On W2, LRU, LFU, and ARC all scored 0%. When a range just slightly larger than the cache (150 pages versus 100) is read in order over and over, every page is evicted just before it is needed again.

ARC cannot learn here because of the rule described above. In W2 every page appears to be used only once, so T1 takes over the whole cache. Then the rule that keeps T1 plus B1 at no more than c leaves no room in B1. The regret sensor is empty, so p never moves from 0.

OPT, meanwhile, scores 66%. For this pattern, the right move is to evict the most recently used page first (MRU). If part of the loop stays in the cache permanently, that part hits on every pass.

Real databases deal with this using mechanisms outside the replacement policy. When PostgreSQL scans a large table, it gives that scan only a small ring buffer, so pages read by the scan do not fill up the whole buffer pool. Another approach is to bypass the buffer pool entirely and keep scanned pages local to the query. And because a database knows the query plan, if it can tell that a table will be read many times over, it can use a different eviction strategy for that scan alone.

No replacement policy fits every case. ARC's strength is that it rarely loses badly.

### Costs, and Use in Real Systems

ARC has costs too. The ghost lists add bookkeeping, up to twice the cache's capacity in page IDs. And because the lists are reordered on every access, many threads accessing at once tend to contend for the lock that protects them. That is one reason lighter policies such as CLOCK are popular.

As for real-world use, ZFS (a file system) uses ARC for its cache. PostgreSQL adopted ARC in 8.0 but removed it soon after because of IBM's patent, replacing it with a different policy called 2Q in 8.0.2. Since 8.1 it has used clock-sweep. MySQL InnoDB splits its LRU list into an old part and a young part. A new page first goes into old and moves to young only when it is used again, so pages read by a scan rarely reach young and sequential flooding is less likely. The idea is close to ARC's T1 and T2.

As an aside, the design of "split memory into fixed-size slots, track where things are with a table, and choose carefully what to evict when space runs out" shows up outside databases too. vLLM's PagedAttention, an LLM inference engine technique, splits GPU memory into fixed-size blocks and manages them with a block table. The field is different, but the problems you hit when designing a cache are the same.

## Summary

LRU's hit rate fell when full scans were mixed in, and LFU's fell when the hot set changed. ARC used its ghost lists to measure whether its eviction decisions were wrong and adjusted the balance between its two groups by itself, so it did not lose badly in either case. Still, ARC cannot win against a looping scan over a range slightly larger than the cache.

Which eviction policy works best depends on the workload. What makes ARC interesting is that the cache makes that adjustment itself, by learning from its own regrets.

The experiment code is on [GitHub](https://github.com/SHONOSUKE100/SHONOSUKE100.github.io/tree/main/experiments/buffer-pool-replacement). The random seeds are fixed, so the results are reproducible.

### References

- Nimrod Megiddo and Dharmendra S. Modha. "ARC: A Self-Tuning, Low Overhead Replacement Cache." *FAST '03*, 2003.
- Andy Pavlo. CMU 15-445/645 Database Systems (Fall 2025), Lecture #04: Memory & Disk Management.
