import requests
from ..config import config as conf


url = conf.config_cinsscore()


def check_ip_in_cinsscore(ip_address):
    response = requests.get(url)
    blacklist = response.text.split("\n")
    return ip_address in blacklist


# 詳細表示
def display_cinsscore_info(ip_address):
    output = []
    if check_ip_in_cinsscore(ip_address):
        output.append(f"{ip_address} is blacklisted")
        malignant_point = 0
    else:
        output.append(f"{ip_address} is not blacklisted")
        malignant_point = 1
    return output, malignant_point
