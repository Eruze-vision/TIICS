from services.osint import greensnow as gs
from services.osint import cinsscore as cs
from services.osint import bruteforceblocker as bfb
from services.osint import abuseipdb as ab
from services.osint import virustotal as vt
from datetime import datetime

import os
from dotenv import load_dotenv


# ブラックリストに載っている場合，詳細表示
def display_osint_info(ip_address):
    output = []
    # 現在の日付と時間を取得
    now = datetime.now()
    today = now.strftime("%Y年%m月%d日 %H時%M分")

    # 年、月、日、時間、分を表示
    output.append(f"調査日：{today}")

    result = gs.check_ip_in_greensnow(ip_address)
    output.append("= = = = = details of greensnow = = = = =")
    if result is not None:
        output_greensnow, malignant_point_gs = gs.display_greensnow_info(ip_address)
        output.extend(output_greensnow)
    else:
        output.append("No data")
        malignant_point_gs = 1

    result = cs.check_ip_in_cinsscore(ip_address)
    output.append("= = = = = details of cinsscore = = = = =")
    if result is not None:
        output_cinsscore, malignant_point_cs = cs.display_cinsscore_info(ip_address)
        output.extend(output_cinsscore)
    else:
        output.append("No data")
        malignant_point_cs = 1

    result = bfb.check_ip_in_bruteforceblocker(ip_address)
    output.append("= = = details of bruteforceblocker = = =")
    if result is not None:
        (
            output_bruteforceblocker,
            malignant_point_bfb,
        ) = bfb.display_bruteforceblocker_info(ip_address)
        output.extend(output_bruteforceblocker)
    else:
        output.append("No data")
        malignant_point_bfb = 1

    result = ab.check_ip_in_abuseipdb(ip_address)
    output.append("= = = = = details of abuseipdb = = = = =")
    if result is not None:
        output_abuseipdb, malignant_point_ab = ab.display_abuseipdb_info(ip_address)
        output.extend(output_abuseipdb)
    else:
        output.append("No data")
        malignant_point_ab = 1

    malignant_result = (
        malignant_point_gs
        * malignant_point_cs
        * malignant_point_bfb
        * malignant_point_ab
    )

    if malignant_result < 1:
        result = vt.check_ip_in_virustotal(ip_address)
        output.append("= = = = = details of virustotal = = = = =")
        if result is not None:
            output_virustotal = vt.display_virustotal_info(result)
            output.extend(output_virustotal)
        else:
            output.append("No data")

    output.append("\n")
    output_txt = "\n".join(output)
    print(output_txt)
    write_ip_details_to_txt(ip_address, output_txt)


# レポート内容を.txtで出力
def write_ip_details_to_txt(ip_address, output_txt):
    load_dotenv()

    directory_path = os.getenv("RESULTS_DIR", "results")
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    file_path = os.path.join(directory_path, f"{ip_address}.txt")

    try:
        with open(file_path, "x", encoding="utf-8") as file:
            file.write(output_txt)
            # print(f"created {file_path} successfully")
    except FileExistsError:
        # 既存のファイルの内容を一時的に保存
        with open(file_path, "r", encoding="utf-8") as file:
            temp = file.read()

        # 新しい内容を書き込み、一時的に保存した内容を追加
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"{output_txt}\n{temp}")
            # print(f"added txt to {file_path}")
