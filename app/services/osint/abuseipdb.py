import requests
from ..config import config as conf

api_key, url_abuse, url_end_point = conf.config_abuse()


# ブラックリストと照合
def check_ip_in_abuseipdb(ip_address):
    output = []
    headers = {"Accept": "application/json", "Key": api_key}
    url = url_abuse.format(ip_address=ip_address)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()["data"]
        if data.get("isPublic"):
            if data["abuseConfidenceScore"] > 0:
                output.append(
                    f"{ip_address} is blacklisted with a score of {data['abuseConfidenceScore']}."
                )
                malignant_point = 0
            else:
                output.append(f"{ip_address} is not blacklisted")
                malignant_point = 1
        else:
            malignant_point = 1
        return output, malignant_point
    else:
        output.append(f"Error: {response.content}")
        malignant_point = 1
        return output, malignant_point


# 詳細表示
def display_abuseipdb_info(ip_address):
    querystring = {"ipAddress": ip_address, "maxAgeInDays": "365"}
    headers = {"Accept": "application/json", "Key": api_key}

    response = requests.get(url_end_point, headers=headers, params=querystring)

    output = []

    result, malignant_point = check_ip_in_abuseipdb(ip_address)
    output.extend(result)

    if response.status_code == 200:
        data = response.json().get("data", {})
        for key, value in data.items():
            output.append(
                f"{key.capitalize()}: {value}"
                if value
                else f"{key.capitalize()}: No Data"
            )
    else:
        output.append(f"Error: {response.status_code}")

    return output, malignant_point
