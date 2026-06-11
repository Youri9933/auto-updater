import os
import sys
import json
import subprocess
import platform
from datetime import datetime

CONFIG_FILE = "config.json"
LOG_FILE = "logs/update_log.md"
LOGO_FILE = "assets/logo.png"

SYSTEM = platform.system().lower()

DEV_TOOLS = [
    "Git",
    "GitHub Desktop",
    "GitKraken",
    "Docker",
    "Docker Desktop",
    "Kubernetes",
    "Windows Terminal",
    "PowerShell",
    "WSL",
    "Curl",
    "7zip",
    "Visual Studio Code",
    "Visual Studio",
    "JetBrains Toolbox",
    "IntelliJ IDEA",
    "PyCharm",
    "WebStorm",
    "Android Studio",
    "Notepad++",
    "Node.js",
    "Python",
    "Java",
    ".NET SDK",
    "Go",
    "Rust",
    "PHP",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Redis",
    "SQLite",
    "Postman",
    "Insomnia",
    "AWS CLI",
    "Azure CLI",
    "Google Cloud SDK",
    "Terraform"
]


def ensure_directories():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    if not os.path.exists("assets"):
        os.makedirs("assets")


def save_config(config):
    ensure_directories()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def create_default_config():
    config = {
        "auto_update_apps": True,
        "update_all": True,
        "app_list": [],
        "exclude_list": [],
        "schedule_enabled": False,
        "day_interval": 7
    }
    save_config(config)
    return config


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return create_default_config()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return create_default_config()


def write_log(content):
    ensure_directories()
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("=== UPDATE LOG ===\n\n(fichier de logs — entrées horodatées)\n")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n## {ts}\n\n```text\n{content.rstrip()}\n```\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


def open_log():
    try:
        if SYSTEM.startswith("win"):
            os.startfile(LOG_FILE)
        elif SYSTEM == "linux":
            subprocess.run(["xdg-open", LOG_FILE], check=False)
        else:
            print("Log saved to:", LOG_FILE)
    except Exception:
        pass


def show_logo():

    if os.path.exists(LOGO_FILE):
        print(f"[logo] {LOGO_FILE}")
    else:
        print("[logo absent]")


def update_dev_tools():
    if not SYSTEM.startswith("win"):
        print("update_dev_tools: winget disponible uniquement sur Windows")
        return
    for tool in DEV_TOOLS:
        print(f"Update / Install: {tool}")
        subprocess.run(["winget", "install", "--id", tool, "-e", "--source", "winget"], check=False)


def detect_package_manager():
    if os.path.exists("/usr/bin/apt") or os.path.exists("/usr/bin/apt-get"):
        return "apt"
    if os.path.exists("/usr/bin/pacman"):
        return "pacman"
    if os.path.exists("/usr/bin/dnf"):
        return "dnf"
    return None


def update_apps(config):
    print("Mise à jour...")
    log = f"\n===== UPDATE {datetime.now()} ====\n"
    try:
        if SYSTEM.startswith("win"):
            if config.get("update_all", True):
                res = subprocess.run(["winget", "upgrade", "--all"], capture_output=True, text=True, check=False)
                log += (res.stdout or res.stderr or "")
            else:
                for app in config.get("app_list", []):
                    if any(ex in app.lower() for ex in config.get("exclude_list", [])):
                        continue
                    res = subprocess.run(["winget", "upgrade", app], capture_output=True, text=True, check=False)
                    log += (res.stdout or res.stderr or "") + "\n"

        elif SYSTEM == "linux":
            pm = detect_package_manager()
            if pm == "apt":
                subprocess.run(["sudo", "apt", "update"], check=False)
                res = subprocess.run(["sudo", "apt", "upgrade", "-y"], capture_output=True, text=True, check=False)
                log += (res.stdout or res.stderr or "")
            elif pm == "pacman":
                res = subprocess.run(["sudo", "pacman", "-Syu", "--noconfirm"], capture_output=True, text=True, check=False)
                log += (res.stdout or res.stderr or "")
            elif pm == "dnf":
                subprocess.run(["sudo", "dnf", "check-update"], check=False)
                res = subprocess.run(["sudo", "dnf", "upgrade", "-y"], capture_output=True, text=True, check=False)
                log += (res.stdout or res.stderr or "")
            else:
                log += " Aucun gestionnaire de paquets détecté\n"
                print("Gestionnaire de paquets non supporté")
        else:
            log += f"OS non supporté pour update: {SYSTEM}\n"
    except Exception as e:
        log += f"Erreur : {e}\n"
        print("Erreur lors de la mise à jour :", e)

    write_log(log)
    open_log()


def setup_scheduler(config):
    interval = str(config.get("day_interval", 7))
    if SYSTEM.startswith("win"):
        python_exec = sys.executable or "python"
        subprocess.run([
            "schtasks",
            "/Create",
            "/SC", "DAILY",
            "/MO", interval,
            "/TN", "AutoUpdater",
            "/TR", f'"{python_exec}" "{os.path.abspath(__file__)}"',
            "/F"
        ], check=False)
    elif SYSTEM == "linux":
        cron_job = f"0 0 */{interval} * * {sys.executable} {os.path.abspath(__file__)}"
        subprocess.run(f'(crontab -l 2>/dev/null; echo "{cron_job}") | crontab -', shell=True, check=False)
    else:
        print("Scheduler non supporté pour cet OS")
    print("Scheduler activé")


def remove_scheduler():
    if SYSTEM.startswith("win"):
        subprocess.run(["schtasks", "/Delete", "/TN", "AutoUpdater", "/F"], check=False)
    elif SYSTEM == "linux":
        subprocess.run("crontab -r", shell=True, check=False)
    else:
        print("Remove scheduler non supporté pour cet OS")
    print("Scheduler supprimé")


def config_menu(config):
    print("\nConfig")
    print("1 - Toggle update_all")
    print("2 - Ajouter app")
    print("3 - Ajouter exclusion")
    print("4 - Scheduler ON")
    print("5 - Scheduler OFF")
    print("6 - Afficher logo")
    print("0 - Retour")

    choice = input("Choix : ").strip()

    if choice == "1":
        config["update_all"] = not config.get("update_all", True)

    elif choice == "2":
        app = input("Nom app : ").strip()
        if app:
            config.setdefault("app_list", []).append(app)

    elif choice == "3":
        exel = input("Nom à exclure : ").strip()
        if exel:
            config.setdefault("exclude_list", []).append(exel)

    elif choice == "4":
        config["schedule_enabled"] = True
        setup_scheduler(config)

    elif choice == "5":
        config["schedule_enabled"] = False
        remove_scheduler()

    elif choice == "6":
        show_logo()

    save_config(config)


def main():
    ensure_directories()
    config = load_config()

    while True:
        print("\n=== AUTO UPDATER ====")
        print("os détecté :", SYSTEM)
        print("1 - Update")
        print("2 - Config")
        print("3 - Update dev tools (Windows only)")
        print("0 - Quitter")

        choice = input("Choix : ").strip()

        if choice == "1":
            if config.get("auto_update_apps", True):
                update_apps(config)
            else:
                print("Mise à jour automatique désactivée dans la configuration.")
        elif choice == "2":
            config_menu(config)
        elif choice == "3":
            update_dev_tools()
        elif choice == "0":
            break
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()