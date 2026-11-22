"""4つのワークロードで LRU / LFU / ARC / OPT のヒット率を比べ、表とグラフを出力する。

使い方:
  python3 -m venv .venv && .venv/bin/pip install matplotlib
  .venv/bin/python run.py
出力:
  results.md                                   … 結果の表
  ../../public/images/writings/buffer-pool-arc/ … 記事用の SVG グラフ
"""
import json
from pathlib import Path

import matplotlib
import matplotlib.ticker

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from policies import ARC, LFU, LRU, OPT  # noqa: E402
from workloads import SCAN_PAGE_START, WORKLOADS  # noqa: E402

CAPACITY = 100
HERE = Path(__file__).resolve().parent
IMG = HERE.parent.parent / "public" / "images" / "writings" / "buffer-pool-arc"
COLORS = {"LRU": "#d97706", "LFU": "#7c3aed", "ARC": "#0f766e", "OPT": "#9ca3af"}

plt.rcParams.update({
    "font.family": ["Hiragino Sans", "sans-serif"],
    "svg.fonttype": "path",
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def simulate(policy, trace, track_p=False):
    """ヒット率を返す。全件スキャンのページ（どの方式でも必ずミスする）は数えず、普段のアクセスだけで測る。"""
    hits = counted = 0
    p_series = []
    for i, page in enumerate(trace):
        hit = policy.access(page)
        if page < SCAN_PAGE_START:
            counted += 1
            hits += hit
        if track_p and i % 50 == 0:
            p_series.append((i, policy.p))
    return hits / counted, p_series


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    results, p_by_workload, traces = {}, {}, {}
    for wname, make in WORKLOADS.items():
        trace = make()
        traces[wname] = trace
        row = {}
        for policy in (LRU(CAPACITY), LFU(CAPACITY), ARC(CAPACITY), OPT(CAPACITY, trace)):
            rate, p_series = simulate(policy, trace, track_p=isinstance(policy, ARC))
            row[policy.name] = rate
            if p_series:
                p_by_workload[wname] = p_series
        results[wname] = row
        print(wname, {k: f"{v:.1%}" for k, v in row.items()})

    # 結果の表
    names = ["LRU", "LFU", "ARC", "OPT"]
    lines = ["| ワークロード | " + " | ".join(names) + " |", "| --- |" + " ---: |" * len(names)]
    for wname, row in results.items():
        lines.append(f"| {wname} | " + " | ".join(f"{row[n]:.1%}" for n in names) + " |")
    (HERE / "results.md").write_text(
        f"キャッシュ {CAPACITY} ページ、各 {len(next(iter(traces.values()))):,} アクセスのヒット率（W3 はスキャン以外のアクセスだけで計算）\n\n" + "\n".join(lines) + "\n",
        encoding="utf-8",
    )
    (HERE / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    # 図: ワークロードのアクセスの様子（時間 × ページ番号）
    # 全体を描くと模様が見えないワークロードは、最初の一部分だけを拡大する
    windows = {"W1": 3_000, "W2": 600, "W3": 3_000, "W4": None}
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.4))
    for ax, (wname, trace) in zip(axes, traces.items()):
        n = windows[wname[:2]] or len(trace)
        step = max(1, n // 3_000)
        xs = list(range(0, n, step))
        normal = [i for i in xs if trace[i] < SCAN_PAGE_START]
        scan = [i for i in xs if trace[i] >= SCAN_PAGE_START]
        ax.scatter(normal, [trace[i] for i in normal], s=2, color="#334155", alpha=0.45, linewidths=0)
        if scan:
            # スキャンのページ番号はとても大きいので、普段のページの上に帯として描く
            ax.scatter(scan, [1_100 + (trace[i] - SCAN_PAGE_START) * 0.4 for i in scan], s=2, color=COLORS["LRU"],
                       linewidths=0, label="スキャン（一度だけ読む）")
            ax.legend(frameon=False, fontsize=8, loc="lower right", markerscale=4)
            ax.set_yticks([0, 500, 1000], ["0", "500", "1000"])
        ax.set_title(wname + ("" if n == len(trace) else f"（最初の {n:,} 回）"), fontsize=10)
        ax.set_xlabel("アクセスの順番")
        ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v / 1000:g}k" if v else "0"))
    axes[0].set_ylabel("ページ番号")
    fig.tight_layout()
    fig.savefig(IMG / "workloads.svg")
    plt.close(fig)

    # 図: ヒット率の比較（第1ラウンド: LRU/LFU/OPT、第2ラウンド: +ARC）
    for fname, shown in (("round1.svg", ["LRU", "LFU", "OPT"]), ("round2.svg", names)):
        fig, ax = plt.subplots(figsize=(9, 4))
        width = 0.8 / len(shown)
        for j, n in enumerate(shown):
            xs = [i + (j - (len(shown) - 1) / 2) * width for i in range(len(results))]
            vals = [results[w][n] * 100 for w in results]
            ax.bar(xs, vals, width, label=n, color=COLORS[n])
            for x, v in zip(xs, vals):
                ax.text(x, v + 1, f"{v:.0f}", ha="center", fontsize=8)
        ax.set_xticks(range(len(results)), list(results))
        ax.set_ylabel("ヒット率（%）")
        ax.set_ylim(0, 100)
        ax.legend(frameon=False, ncol=len(shown))
        fig.tight_layout()
        fig.savefig(IMG / fname)
        plt.close(fig)

    # 図: ARC の p の時間変化
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.2), sharey=True)
    window = 40  # 移動平均の幅（記録点の数。1点 = 50 アクセス）
    for ax, (wname, series) in zip(axes, p_by_workload.items()):
        xs, ps = [i for i, _ in series], [p for _, p in series]
        smooth = [sum(ps[max(0, k - window + 1):k + 1]) / len(ps[max(0, k - window + 1):k + 1]) for k in range(len(ps))]
        ax.plot(xs, ps, color=COLORS["ARC"], lw=0.5, alpha=0.3)
        ax.plot(xs, smooth, color=COLORS["ARC"], lw=1.8)
        if wname.startswith("W4"):
            ax.axvline(len(traces[wname]) // 2, color="#64748b", ls="--", lw=1)
            ax.text(len(traces[wname]) // 2, CAPACITY * 0.45, " 人気が入れ替わる", fontsize=8, color="#475569")
        ax.set_title(wname, fontsize=10)
        ax.set_xlabel("アクセスの順番")
        ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v / 1000:g}k" if v else "0"))
    axes[0].set_ylabel(f"p（T1 の目標サイズ、容量 {CAPACITY}）")
    axes[0].set_ylim(0, CAPACITY / 2)
    fig.tight_layout()
    fig.savefig(IMG / "arc-p.svg")
    plt.close(fig)


if __name__ == "__main__":
    main()
