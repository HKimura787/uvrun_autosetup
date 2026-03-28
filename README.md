# uvrun.bat — Windows 向け `uv run` ラッパー

このリポジトリの主役は **`uvrun.bat`** です。プロジェクトルートで `uv run` を実行し、**`uv` が無い環境では公式インストーラで自動インストール**してから動かします（PATH がまだ効いていないセッション向けに、既定の配置も補正します）。

付属の **Python（`main.py` と `pyproject.toml`）はサンプル**です。`uv run` が実際のプロジェクトでどう動くかを示すための最小例として置いてあります（PySide6 の電卓 GUI）。

## `uvrun.bat` の動き（要約）

1. バッチと同じフォルダに `cd` する。
2. `uv` を PATH または `%USERPROFILE%\.local\bin` / `\.cargo\bin` から解決する。無ければ PowerShell で [公式 install.ps1](https://docs.astral.sh/uv/getting-started/installation/) を実行する。
3. **引数なし** → `uv run python main.py`（サンプルアプリ起動）。
4. **引数あり** → `uv run` にそのまま渡す（例: `uvrun.bat python -c "print(1)"`、`uvrun.bat --help`）。

## 使い方（Windows）

1. リポジトリを取得し、**`uvrun.bat` があるディレクトリ**で実行する（ダブルクリックでも可）。
2. 初回のみ `uv` のダウンロード・インストールが走ることがあります。

サンプル以外のコマンドを試す場合は引数を付けてください。

## サンプル Python プロジェクトについて

| ファイル | 役割 |
|----------|------|
| `pyproject.toml` / `uv.lock` | サンプル用の依存定義（`uv sync` / `uv run` のデモ） |
| `main.py` | デモ用の電卓 GUI（引数なし実行時のデフォルト） |

本番の自分用プロジェクトでは、このバッチをコピーして **`pyproject.toml` 側を差し替え**、必要ならバッチ内のデフォルトコマンド（いまは `python main.py`）を書き換えてください。

## 参考: `uv` だけ使う場合（全 OS）

`uv` が既に入っている環境では、サンプルは次のようにも起動できます。

```bash
uv sync
uv run python main.py
```

## ライセンス

リポジトリ内の [LICENSE](LICENSE) に従います。
