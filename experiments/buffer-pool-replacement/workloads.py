"""実験に使う4つのワークロード（ページ番号の並び）を作る。

すべて乱数の種を固定しているので、何度実行しても同じ並びになる。
"""
import bisect
import itertools
import random

N_ACCESS = 100_000  # アクセスの回数
N_PAGES = 1_000  # 「普段使う」ページの種類


def _zipf_sampler(n, alpha, rng):
    """1..n の順位に Zipf 分布で偏ったページを返す関数を作る（人気の順位はランダムに並べ替える）。"""
    weights = [1 / (k ** alpha) for k in range(1, n + 1)]
    cum = list(itertools.accumulate(weights))
    pages = list(range(n))
    rng.shuffle(pages)

    def sample():
        return pages[bisect.bisect_left(cum, rng.random() * cum[-1])]

    return sample


def w1_skewed(seed=1):
    """W1 偏りあり：一部の人気ページにアクセスが集中する（OLTP 風）。"""
    rng = random.Random(seed)
    sample = _zipf_sampler(N_PAGES, 1.0, rng)
    return [sample() for _ in range(N_ACCESS)]


def w2_loop(seed=2, loop_len=150):
    """W2 ループスキャン：キャッシュより少し大きい範囲を、何周も順に読む。"""
    return [i % loop_len for i in range(N_ACCESS)]


SCAN_PAGE_START = 1_000_000  # 全件スキャンのページ番号はここから始まる（普段のページとは重ならない）


def w3_skewed_with_scans(seed=3, scan_ratio=1 / 3):
    """W3 偏り＋全件スキャン：W1 と同時に、一度しか読まないページを順に読むバッチが流れる。

    アクセスの約 1/3 がバッチのスキャン。昼間の OLTP の裏で分析クエリが走る状況をまねている。
    """
    rng = random.Random(seed)
    sample = _zipf_sampler(N_PAGES, 1.0, rng)
    trace, next_scan_page = [], SCAN_PAGE_START
    for _ in range(N_ACCESS):
        if rng.random() < scan_ratio:
            trace.append(next_scan_page)
            next_scan_page += 1
        else:
            trace.append(sample())
    return trace


def w4_shift(seed=4):
    """W4 人気の入れ替わり：途中で、人気ページの集合がまるごと別のページに変わる。"""
    rng = random.Random(seed)
    before = _zipf_sampler(N_PAGES, 1.0, rng)
    after = _zipf_sampler(N_PAGES, 1.0, rng)
    half = N_ACCESS // 2
    return [before() for _ in range(half)] + [N_PAGES + after() for _ in range(N_ACCESS - half)]


WORKLOADS = {
    "W1 偏りあり": w1_skewed,
    "W2 ループスキャン": w2_loop,
    "W3 偏り+全件スキャン": w3_skewed_with_scans,
    "W4 人気の入れ替わり": w4_shift,
}
