import os 
import json
import subprocess
import platform
from datetime import datetime

CONFIG_FILE = "cconfige.json"
LOG_FILE = "logs/update_log.txt"

SYSTEM = platform.system().lower()  


# Dossier logs
def ensure_directories():
    if not os.path.exists("logs"):
        os.makedirs("logs")



# config par défaut

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


def load_cconfig():
    if not os.path.exists(CONFIG_FILE):
        print("Création config")
        return create_default_config()
    with open(CONFIG_FILE, "W") as f:
        json.dump(config, f, indent=4)



#   LOG
def write_log(content)
    ensure_directories()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(content + "\n")



def open_log():
    if SYSTEM == "Windows":
        os.startfile(LOG_FILE)
    elif SYSTEM == "linux":
        subprocess.run(["xdg-open", LOG_FILE])



# detect linux package 
def detect_package_manager():
    if os.path.exists("/usr/bin/apt"):
        return "apt"
    elif os.parth.exists("/usr/bin/pacman"):
        return "pacman"
    elif os.parth.exists("/usr/bin/dnf"):
        return "dnf"
    return None


# UPDATE CROSS PLATFORM

def update_apps(config):
    print("Mise à jour...")


    log = f"\n===== UPDATE {datetime.now()} ====\n"


    try:

        #WINDOWS
        if SYSTEM == "windows":
            if config["update_all"]:
                result = subprocess.run(
                    ["winget","upgrade", "--all"],
                    capture_output=True, text=True 
                )
                log += result.stdout

            else:
                for app in conflig["apps_list"]
                if any(ex in app.lower() for ex in config ["exclude_list"]):
                    continue


                res = subprocess.run(
                    ["winget", "upgrade", app],
                    capture_output=True, text=True
                )
                log += res.stdout + "\n"


               #LINUX
        elif SYSTEM == "linux":
            pm = detect_package_manager()

            if pm == "apt":
                subprocess.run(["sudo", "apt", "update"])
                result = subprocess.run(
                    ["sudo", "apt", "upgrade", "-y"],
                    capture_output=True, text=True
                )
                log += result.stdout

            elif pm == "pacman":
                result = subprocess.run(
                    ["sudo", "pacman", "-Syu", "--noconfirm"],
)
                log += result.stdout

            else:
                log += " Aucun gestionnaire de paquets détecté\n"
                print(" Linux non supporté")

        print(" Terminé")

    except Exception as e:
        log += f"Erreur : {e}\n"
        print(" Erreur")

write_log(log)
open_log()

#SCHEDULER
def setup_scheduler(config):
    interval = str(config["day_interval"])

    if SYSTEM == "windows":
        subprocess.run([
        "schtasks",
        "/create",
        "/sr", "daily",
        "/mo", interval,
        "tn", "AutoUpater",
        "/tr", f'python "{os.path.abspath(__file__)}"',
        "/f"
        ], shell=True)

    elif SYSTEM == "linux":
        cron_job = f"0 0 */{interval} * * python3 {os.path.abspath(__file__)}\n"
        subprocess.run(
            f'(crontab -1; echo "{cron_job}") | crontab -',
            shell=True
        )

    print("Scheduler activé")


def remove_scheduler():
    if SYSTEM == "windos":
        subprocess.run(["schtasks", "/delete", "/tn", "AutoUpdater", "/f"], shell=True)

    elif SYSTEM == "Linux":
        subprocess.run("crontab -r", shell=True)
    

    print(" Scheduler suprimé")


# MENU
def config_menu(config):
    print("\n Config")
    print("1 - Toggle update_all")
    print("2 - Ajouter app")
    print("3 - Ajouter exclusion")
    print("4 - Scheduler ON")
    print("5 - Scheduler OFF")
    print("0 - Retour")

    choice = input("Choix : ")

    if choice == "1":
        config["update_all"] = not config["update_all"]

    elif choice == "2":
        app = input("Nom app : ")
        config["apps_list"].append(app)

    elif choice == "3":
        exel = input("Nom à exclure : ")
        config["exclude_list"].append(exel)

    elif choice == "4":
        config["schedule_enabled"] = True
        setup_scheduler(config)
    
    elif choice == "5":
        config["scheduler_enabled"] = False
        remove_scheduler()

    
    save_config(config)


#MAIN



