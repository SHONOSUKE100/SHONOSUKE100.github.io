# バッファプールの置換方式の比較実験

記事「LRU と LFU と ARC、ヒット率で勝つのはどれか」（`src/content/writings/ja/buffer-pool-arc.md`）で使った実験です。

| ファイル | 中身 |
| --- | --- |
| `policies.py` | LRU / LFU / ARC / OPT の実装 |
| `workloads.py` | 4つのワークロード（W1〜W4） |
| `run.py` | 実験を回し、`results.md` と記事用の SVG（`public/images/writings/buffer-pool-arc/`）を出力する |
| `test_policies.py` | 実装のテスト（ARC の不変条件、小さな例、OPT が上限になること） |

## 実行

```sh
cd experiments/buffer-pool-replacement
python3 -m venv .venv
.venv/bin/pip install matplotlib
.venv/bin/python test_policies.py
.venv/bin/python run.py
```

乱数の種は固定しているので、何度実行しても同じ結果になります。
