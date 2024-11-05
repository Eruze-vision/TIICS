# TIICS
Threat of IP address and its information collection system

## Installation / インストール

Run the following command:
以下のコマンドを実行:
```bash
pip install -r requirements.txt
```

## Configuration / 設定

Create `TIICS/app/services/config/config_secret.toml` and add the following content:  
`TIICS/app/services/config/config_secret.toml`を作成し、以下の内容を記述する:

```toml
[apikey]
AbuseIPDB_APIkey = "your API key"  # 自身のAPIキー
VirusTotal_APIkey = "your API key"  # 自身のAPIキー
