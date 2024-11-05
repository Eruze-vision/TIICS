import requests
from ..config import config as conf


api_key, url_vt = conf.config_virus_total()


def check_ip_in_virustotal(ip_address):
    url = f"{url_vt}{ip_address}"
    headers = {"x-apikey": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def display_virustotal_info(result):
    num = 0
    # IPアドレスに関連する主要な情報を抽出
    ip_address = result["data"]["id"]
    last_analysis_stats = result["data"]["attributes"]["last_analysis_stats"]

    # 結果を整形して表示
    output = []
    output.append(f"IPアドレス: {ip_address}")
    output.append("最終分析統計:")
    for key, value in last_analysis_stats.items():
        output.append(f"  {key}: {value}")

    # 悪性と判断された場合の詳細情報を表示
    if last_analysis_stats["malicious"] > 0:
        output.append("\n悪性と判断された詳細情報:")
        for engine_name, engine_data in result["data"]["attributes"][
            "last_analysis_results"
        ].items():
            if engine_data["category"] == "malicious":
                if num < 1:
                    output.append("malicious")
                if num > 0:
                    output.append("------------------------------------------")
                num += 1
                output.append(f"No.{num}")
                output.append(f"  エンジン名: {engine_name}")
                output.append(f"  検出したマルウェア: {engine_data['result']}")
                if "update" in engine_data:
                    output.append(f"  更新日時: {engine_data['update']}")
                # 関連するドメイン名を表示
                if "resolutions" in result["data"]["attributes"]:
                    if result["data"]["attributes"]["resolutions"]:
                        output.append("\n関連するドメイン名:")
                        for resolution in result["data"]["attributes"]["resolutions"]:
                            output.append(f"  ドメイン名: {resolution['hostname']}")
                    else:
                        output.append("\n関連するドメイン名はありません。")
                else:
                    output.append("ドメイン名を提供していません")
        num = 0

    # 悪性の疑いありと判断された場合の詳細情報を表示
    if last_analysis_stats["suspicious"] > 0:
        output.append("\n悪性と判断された詳細情報:")
        for engine_name, engine_data in result["data"]["attributes"][
            "last_analysis_results"
        ].items():
            if engine_data["category"] == "suspicious":
                if num < 1:
                    output.append("・・・・・・・・・・・・・・・・・・・・・")
                    output.append("suspicious")
                if num > 0:
                    output.append("------------------------------------------")
                num += 1
                output.append(f"No.{num}")
                output.append(f"  エンジン名: {engine_name}")
                output.append(f"  検出したマルウェア: {engine_data['result']}")
                if "update" in engine_data:
                    output.append(f"  更新日時: {engine_data['update']}")
                if "resolutions" in result["data"]["attributes"]:
                    if result["data"]["attributes"]["resolutions"]:
                        output.append("\n関連するドメイン名:")
                        for resolution in result["data"]["attributes"]["resolutions"]:
                            output.append(f"  ドメイン名: {resolution['hostname']}")
                    else:
                        output.append("\n関連するドメイン名はありません。")
                else:
                    output.append("ドメイン名を提供していません")

    return output
