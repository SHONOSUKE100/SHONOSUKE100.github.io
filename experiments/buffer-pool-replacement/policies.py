"""バッファプールの置換方式（LRU / LFU / ARC / OPT）のシミュレーション実装。

どの方式も「ページ番号を1つ受け取り、ヒットしたかを返す」access() だけを持つ。
ディスク I/O、ピン、dirty、スレッドは扱わない（ヒット率だけを比べるため）。
"""
from collections import OrderedDict, defaultdict
import heapq


class LRU:
    """一番昔に使われたページを追い出す。"""

    name = "LRU"

    def __init__(self, capacity):
        self.capacity = capacity
        self.pages = OrderedDict()  # 先頭が一番古い、末尾が一番新しい

    def access(self, page):
        if page in self.pages:
            self.pages.move_to_end(page)
            return True
        if len(self.pages) >= self.capacity:
            self.pages.popitem(last=False)
        self.pages[page] = None
        return False


class LFU:
    """キャッシュにいる間の使用回数が一番少ないページを追い出す。

    回数が同じなら、その中で一番昔に使われたページを追い出す。
    追い出したページの回数は忘れる（in-cache LFU）。
    """

    name = "LFU"

    def __init__(self, capacity):
        self.capacity = capacity
        self.count = {}
        self.buckets = defaultdict(OrderedDict)  # 回数 -> その回数のページ（古い順）
        self.min_count = 0

    def _touch(self, page):
        c = self.count[page]
        del self.buckets[c][page]
        if not self.buckets[c]:
            del self.buckets[c]
            if self.min_count == c:
                self.min_count = c + 1
        self.count[page] = c + 1
        self.buckets[c + 1][page] = None

    def access(self, page):
        if page in self.count:
            self._touch(page)
            return True
        if len(self.count) >= self.capacity:
            victim, _ = self.buckets[self.min_count].popitem(last=False)
            if not self.buckets[self.min_count]:
                del self.buckets[self.min_count]
            del self.count[victim]
        self.count[page] = 1
        self.buckets[1][page] = None
        self.min_count = 1
        return False


class ARC:
    """Adaptive Replacement Cache（Megiddo & Modha, FAST 2003）の論文どおりの実装。

    T1: 1回だけ使われたページ   B1: T1 から追い出したページの ID（ゴースト）
    T2: 2回以上使われたページ   B2: T2 から追い出したページの ID（ゴースト）
    p : T1 の目標サイズ
    各リストは OrderedDict で、先頭が LRU 側（古い）、末尾が MRU 側（新しい）。
    """

    name = "ARC"

    def __init__(self, capacity):
        self.c = capacity
        self.p = 0.0
        self.t1, self.t2 = OrderedDict(), OrderedDict()
        self.b1, self.b2 = OrderedDict(), OrderedDict()

    def _replace(self, in_b2):
        # T1 が目標 p より大きければ T1 から、そうでなければ T2 から追い出し、ID をゴーストへ
        if self.t1 and ((in_b2 and len(self.t1) == self.p) or len(self.t1) > self.p):
            old, _ = self.t1.popitem(last=False)
            self.b1[old] = None
        else:
            old, _ = self.t2.popitem(last=False)
            self.b2[old] = None

    def access(self, x):
        # ケース1: キャッシュにある（ヒット）→ T2 の MRU へ
        if x in self.t1:
            del self.t1[x]
            self.t2[x] = None
            return True
        if x in self.t2:
            self.t2.move_to_end(x)
            return True

        # ケース2: B1 にある →「最近の組を追い出しすぎた」ので p を増やす
        if x in self.b1:
            delta = max(len(self.b2) / len(self.b1), 1)
            self.p = min(self.c, self.p + delta)
            self._replace(in_b2=False)
            del self.b1[x]
            self.t2[x] = None
            return False

        # ケース3: B2 にある →「常連を追い出しすぎた」ので p を減らす
        if x in self.b2:
            delta = max(len(self.b1) / len(self.b2), 1)
            self.p = max(0.0, self.p - delta)
            self._replace(in_b2=True)
            del self.b2[x]
            self.t2[x] = None
            return False

        # ケース4: どこにもない（初めて、または完全に忘れた）→ T1 の MRU へ
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


class OPT:
    """Belady の最適方式：次に使われるのが一番遠いページを追い出す。

    未来のアクセス列を知っている必要があるので、現実には作れない「理論上の上限」。
    """

    name = "OPT"

    def __init__(self, capacity, trace):
        self.capacity = capacity
        # next_use[i] = trace[i] と同じページが次に現れる位置（なければ無限大）
        self.next_use = [0] * len(trace)
        last = {}
        for i in range(len(trace) - 1, -1, -1):
            self.next_use[i] = last.get(trace[i], float("inf"))
            last[trace[i]] = i
        self.i = 0
        self.resident = {}  # page -> 次に使われる位置
        self.heap = []  # (-次に使われる位置, page)。古い情報は取り出すときに読み飛ばす

    def access(self, page):
        nxt = self.next_use[self.i]
        self.i += 1
        hit = page in self.resident
        if not hit and len(self.resident) >= self.capacity:
            while True:
                neg, victim = heapq.heappop(self.heap)
                if self.resident.get(victim) == -neg:
                    del self.resident[victim]
                    break
        self.resident[page] = nxt
        heapq.heappush(self.heap, (-nxt, page))
        return hit
