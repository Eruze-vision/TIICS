import toml
import os
from dotenv import load_dotenv
# .envファイルを読み込む
load_dotenv()

def load_config(file_path):
    toml_dir = os.getenv("TOML_DIR", "services/config")
    toml_file = os.path.join(toml_dir, file_path)

    # Tomlファイルの読み込み
    config = toml.load(toml_file)
    return config


def config_toml():
    conf_path = os.getenv("CONF_PATH")
    conf_secret_path = os.getenv("CONF_SECRET_PATH")

    conf = load_config(conf_path)
    conf_secret = load_config(conf_secret_path)

    return conf, conf_secret


def config_abuse():
    conf, conf_secret = config_toml()
    api_abuse = f"{conf_secret['apikey']['AbuseIPDB_APIkey']}"
    url_abuse = f"{conf['urls']['AbuseIPDB_URL']}"
    url_abuse_end_point = f"{conf['urls']['AbuseIPDB_URL_end_point']}"
    return api_abuse, url_abuse, url_abuse_end_point


def config_virus_total():
    conf, conf_secret = config_toml()
    api_vt = f"{conf_secret['apikey']['VirusTotal_APIkey']}"
    url_vt = f"{conf['urls']['VirusTotal_URL']}"
    return api_vt, url_vt


def config_greensnow():
    conf, _ = config_toml()
    url_gs = f"{conf['urls']['GreenSnow_URL']}"
    return url_gs


def config_cinsscore():
    conf, _ = config_toml()
    url_cs = f"{conf['urls']['CINSscore_URL']}"
    return url_cs


def config_bruteforceblocker():
    conf, _ = config_toml()
    url_bfb = f"{conf['urls']['BruteForceBlocker_URL']}"
    return url_bfb


def geolite2_path():
    geolite2_path = os.path.join(
        os.environ["PYTHONPATH"],
        "NAIADES/naiades/backend/data/geolite2/GeoLite2-City.mmdb",
    )
    return geolite2_path


def results_path(latest_run_time, days_ago, more_days_ago):
    results_file = os.path.join(
        os.environ["PYTHONPATH"],
        f"./NAIADES/naiades/backend/analysis/results/{latest_run_time}_{days_ago}d_{more_days_ago}d.pdf",
    )
    return results_file
