"""置換方式の実装が正しく動くかを確かめるテスト。 .venv/bin/python test_policies.py で実行する。"""
import random

from policies import ARC, LFU, LRU, OPT
from workloads import WORKLOADS


def check_arc_invariants(arc):
    t1, t2, b1, b2, c = arc.t1, arc.t2, arc.b1, arc.b2, arc.c
    assert len(t1) + len(t2) <= c, "キャッシュの中身が容量を超えた"
    assert len(t1) + len(b1) <= c, "T1 + B1 が容量を超えた"
    assert len(t1) + len(t2) + len(b1) + len(b2) <= 2 * c, "全体が 2c を超えた"
    assert 0 <= arc.p <= c
    lists = [set(t1), set(t2), set(b1), set(b2)]
    assert sum(map(len, lists)) == len(set().union(*lists)), "同じページが複数のリストにいる"


def test_arc_invariants():
    rng = random.Random(0)
    for trace in [[rng.randrange(300) for _ in range(20_000)], *[f()[:20_000] for f in WORKLOADS.values()]]:
        arc = ARC(50)
        for page in trace:
            arc.access(page)
            check_arc_invariants(arc)


def test_small_examples():
    # LRU: 容量3で A B C A D B E → ヒットは4番目の A だけ
    lru = LRU(3)
    assert [lru.access(x) for x in "ABCADBE"] == [False, False, False, True, False, False, False]
    # LFU: 回数の多い A は残り、回数1のうち一番古い B が追い出される
    lfu = LFU(2)
    assert [lfu.access(x) for x in "AABCA"] == [False, True, False, False, True]
    # ARC: 2回目のアクセスで T1 から T2 へ移る
    arc = ARC(3)
    arc.access("A"); arc.access("A")
    assert "A" in arc.t2 and "A" not in arc.t1


def test_opt_is_upper_bound():
    rng = random.Random(1)
    trace = [int(rng.paretovariate(1.2)) % 400 for _ in range(20_000)]
    hits = {}
    for p in (LRU(60), LFU(60), ARC(60), OPT(60, trace)):
        hits[p.name] = sum(p.access(x) for x in trace)
    assert hits["OPT"] >= max(hits["LRU"], hits["LFU"], hits["ARC"]), hits


if __name__ == "__main__":
    test_arc_invariants()
    test_small_examples()
    test_opt_is_upper_bound()
    print("all tests passed")
