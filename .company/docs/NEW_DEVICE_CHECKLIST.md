# 🆕 新デバイス導入チェックリスト (MCP / Antigravity)

> このファイルは、新しいデバイスで Antigravity エージェントと MCP サーバーを正しく動作させるために確認すべき事項をまとめたものです。
> 秘書は朝の挨拶時に「このデバイスでセットアップが完了しているか」を確認するために、このファイルを参照してください。

---

## ✅ セットアップ項目

### 0. このファイルの目的の確認
- [ ] このチェックリストを新デバイスセットアップ後に一通り実行した（完了日: YYYY-MM-DD）

---

### 1. 依存ツールのインストール

#### Node.js (npx)
- [ ] `nvm` のインストール
  ```bash
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | NVM_DIR="$HOME/.nvm" bash
  ```
- [ ] Node.js LTS のインストール
  ```bash
  source "$HOME/.nvm/nvm.sh" && nvm install --lts
  ```
- [ ] `npx` のパス確認（記録する）
  ```bash
  ls "$HOME/.nvm/versions/node/"   # バージョンを確認
  # 例: /Users/username/.nvm/versions/node/v24.14.0/bin/npx
  ```

#### uv (uvx)
- [ ] `uv` のインストール
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- [ ] `uvx` のパス確認（記録する）
  ```bash
  ls "$HOME/.local/bin/uvx"
  # 例: /Users/username/.local/bin/uvx
  ```

---

### 2. mcp_config.json の更新

**ファイルパス**: `~/.gemini/antigravity/mcp_config.json`

- [ ] `npx` のコマンドパスを実際の絶対パスに書き換え
- [ ] `uvx` のコマンドパスを実際の絶対パスに書き換え
- [ ] `GOOGLE_OAUTH_CREDENTIALS` のパスをこのデバイスの実際のパスに書き換え
  - OneDrive 経由の場合は `/Users/username/Library/CloudStorage/OneDrive-...` 形式を確認
  - パスに **末尾スペースがないこと** を確認
- [ ] `PATH` 環境変数に Node.js / uv のバイナリディレクトリを追加

**テンプレート（書き換え後のイメージ）**:
```json
{
    "mcpServers": {
        "google-calendar": {
            "command": "/Users/[username]/.nvm/versions/node/v[VERSION]/bin/npx",
            "args": ["-y", "@sudomcp/google-calendar-mcp"],
            "env": {
                "PATH": "/Users/[username]/.nvm/versions/node/v[VERSION]/bin:/Users/[username]/.local/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin",
                "GOOGLE_OAUTH_CREDENTIALS": "/Users/[username]/Library/CloudStorage/OneDrive-NITech/Antigravity/Takama-Systems-Group/credentials/gcp-oauth.keys.json"
            }
        },
        "google_workspace": {
            "command": "/Users/[username]/.local/bin/uvx",
            "args": ["workspace-mcp", "--transport", "streamable-http"],
            "env": {
                "PATH": "/Users/[username]/.nvm/versions/node/v[VERSION]/bin:/Users/[username]/.local/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin",
                "GOOGLE_OAUTH_CLIENT_ID": "YOUR_CLIENT_ID",
                "GOOGLE_OAUTH_CLIENT_SECRET": "YOUR_CLIENT_SECRET"
            }
        }
    }
}
```

---

### 3. Antigravity 内での MCP 登録

- [ ] Antigravity アプリを起動し「Manage MCP Servers」を開く
- [ ] `mcp_config.json` のパスを入力して登録
- [ ] `google-calendar` が **Running（緑）** になっているか確認
- [ ] テスト: エージェントに「カレンダーみれる？」と聞いて予定が返ってくるか確認

---

---

### 4. その他確認事項

- [ ] `credentials/gcp-oauth.keys.json` が OneDrive 経由で同期されているか確認
- [ ] OneDrive の同期が「完了」になっているかステータスバーを確認

---

### 5. よくあるエラーと対処法

| エラー | 原因 | 対処法 |
|--------|------|--------|
| `exec: "npx": not found` | npx が PATH にない | Node.js をインストール し、絶対パスを config に記述 |
| `exec: "uvx": not found` | uv が PATH にない | uv をインストールし、絶対パスを config に記述 |
| `env: node: No such file or directory` | PATH に node bin が含まれていない | env の PATH に node のディレクトリを追加 |
| 認証ファイルが見つからない | ファイルパスに余分なスペースや Windows パス | パスを正確にコピーし、末尾スペースを除去 |
| 同期が反映されない | OneDrive が一時停止中など | OneDrive を再起動・同期再開する |

---

> **最終更新**: 2026-03-24 (初版)
> **次回デバイス**: 追加時にこのファイルに `完了日` を記録する
