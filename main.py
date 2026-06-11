
import os
import sys
import json
import shutil
import subprocess
import platform
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONFIG_FILE = str(ROOT / "config.json")
LOG_FILE = str(ROOT / "logs" / "update_log.md")
LOGO_FILE = str(ROOT / "assets" / "logo.png")

SYSTEM = platform.system().lower()

DEV_TOOLS = [
    "Git",
    "Docker",
    "Visual Studio Code",
    "Node.js",
    "Python",
    "Java",
    "Postman",
    "AWS CLI",
    "Azure CLI",
    "Terraform",
]


DEFAULT_CONFIG = {
    "auto_update_apps": True,
    "update_all": True,
    "app_list": [],
    "exclude_list": [],
    "schedule_enabled": False,
    "day_interval": 7,
    "allow_system_updates": False,     
    "auto_install_missing": False       
}


def ensure_directories():
    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    Path(LOGO_FILE).parent.mkdir(parents=True, exist_ok=True)


def save_config(config):
    ensure_directories()
    cfg = DEFAULT_CONFIG.copy()
    cfg.update(config or {})
    
    cfg["app_list"] = [str(x).strip() for x in cfg.get("app_list", []) if str(x).strip()]
    cfg["exclude_list"] = [str(x).strip().lower() for x in cfg.get("exclude_list", []) if str(x).strip()]
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def load_config():
    ensure_directories()
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        
        merged = DEFAULT_CONFIG.copy()
        merged.update(cfg)
    
        merged["app_list"] = [str(x).strip() for x in merged.get("app_list", []) if str(x).strip()]
        merged["exclude_list"] = [str(x).strip().lower() for x in merged.get("exclude_list", []) if str(x).strip()]
        return merged
    except Exception:
        
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()


def _relpath(p):
    try:
        return os.path.relpath(p, ROOT)
    except Exception:
        return str(p)


def write_log(content):
    ensure_directories()
    header = "=== UPDATE LOG ===\n\n(fichier de logs — entrées horodatées)\n"
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(header)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_content = str(content).rstrip()
    entry = f"\n## {ts}\n\n```text\n{safe_content}\n```\n"
    
    entry = entry.replace(str(ROOT), _relpath(ROOT))
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


def open_log():
    try:
        if SYSTEM.startswith("win") and hasattr(os, "startfile"):
            os.startfile(LOG_FILE)
        elif shutil.which("xdg-open"):
            subprocess.run(["xdg-open", LOG_FILE], check=False)
        else:
            print("Log saved to:", _relpath(LOG_FILE))
    except Exception:
        print("Unable to open log; saved to:", _relpath(LOG_FILE))


def show_logo():
    if os.path.exists(LOGO_FILE):
        print("Logo found:", _relpath(LOGO_FILE))
    else:
        print("Logo absent (place a file at assets/logo.png to enable)")


def _bin_available(name):
    return shutil.which(name) is not None


def detect_package_manager():
    if _bin_available("apt") or _bin_available("apt-get"):
        return "apt"
    if _bin_available("pacman"):
        return "pacman"
    if _bin_available("dnf"):
        return "dnf"
    return None


def is_installed_windows(app):
    if not SYSTEM.startswith("win") or not _bin_available("winget"):
        return False
    try:
        r = subprocess.run(["winget", "list", app], capture_output=True, text=True, check=False)
        return app.lower() in (r.stdout or "").lower()
    except Exception:
        return False


def install_or_update_windows(tool):
    if not SYSTEM.startswith("win") or not _bin_available("winget"):
        return "winget not available"
    try:
        if is_installed_windows(tool):
            r = subprocess.run(["winget", "upgrade", tool], capture_output=True, text=True, check=False)
        else:
            r = subprocess.run(["winget", "install", "--id", tool, "-e"], capture_output=True, text=True, check=False)
        return (r.stdout or r.stderr or "").strip()
    except Exception as e:
        return f"ERROR: {e}"


def safe_run(cmd_list, allow_shell=False):

    if allow_shell:
        return subprocess.run(" ".join(cmd_list), shell=True, capture_output=True, text=True, check=False)
    try:
        return subprocess.run(cmd_list, capture_output=True, text=True, check=False)
    except Exception as e:
        return subprocess.CompletedProcess(cmd_list, 1, stdout="", stderr=str(e))


def update_dev_tools(config):
    log = f"\n==== DEV TOOLS {datetime.now()} =====\n"
    for tool in DEV_TOOLS:
        out = install_or_update_windows(tool) if SYSTEM.startswith("win") else f"Skipped: {tool} (non-Windows)"
        log += f"{tool}:\n{out}\n\n"
    write_log(log)
    open_log()


def update_apps(config):
    log = f"\n===== UPDATE {datetime.now()} ====\n"
    try:
        
        if SYSTEM.startswith("win") and _bin_available("winget"):
            if config.get("update_all", True):
                r = safe_run(["winget", "upgrade", "--all"])
                log += (r.stdout or r.stderr or "")
            else:
                for app in config.get("app_list", []):
                    if any(ex in app.lower() for ex in config.get("exclude_list", [])):
                        log += f"Skipped (excluded): {app}\n"
                        continue
                    installed = is_installed_windows(app)
                    if not installed:
                        if config.get("auto_install_missing", False):
                            out = install_or_update_windows(app)
                            log += f"{app} (installed):\n{out}\n\n"
                        else:
                
                            ans = input(f"'{app}' not installed. Install? [y/N]: ").strip().lower()
                            if ans.startswith("y"):
                                out = install_or_update_windows(app)
                                log += f"{app} (installed):\n{out}\n\n"
                            else:
                                log += f"{app}: skipped (not installed)\n"
                            continue
                    r = safe_run(["winget", "upgrade", app])
                    log += (r.stdout or r.stderr or "") + "\n"
        
        elif SYSTEM == "linux":
            if not config.get("allow_system_updates", False):
                log += "System updates skipped: allow_system_updates is false in config\n"
                print("System updates are disabled in config. Set allow_system_updates=true to enable.")
            else:
                pm = detect_package_manager()
                if pm == "apt":
                    safe_run(["sudo", "apt", "update"])
                    r = safe_run(["sudo", "apt", "upgrade", "-y"])
                    log += (r.stdout or r.stderr or "")
                elif pm == "pacman":
                    r = safe_run(["sudo", "pacman", "-Syu", "--noconfirm"])
                    log += (r.stdout or r.stderr or "")
                elif pm == "dnf":
                    safe_run(["sudo", "dnf", "check-update"])
                    r = safe_run(["sudo", "dnf", "upgrade", "-y"])
                    log += (r.stdout or r.stderr or "")
                else:
                    log += "No supported package manager detected\n"
                    print("No supported package manager detected on this system.")
        else:
            log += f"Update not supported on this OS: {SYSTEM}\n"
    except Exception as e:
        log += f"Exception during update: {e}\n"
        print("Error during update:", e)

    write_log(log)
    open_log()


def setup_scheduler(config):
    interval = int(config.get("day_interval", 7))
    if SYSTEM.startswith("win"):
        python_exec = sys.executable or "python"
        cmd = [
            "schtasks", "/Create", "/SC", "DAILY", "/MO", str(interval),
            "/TN", "AutoUpdater", "/TR", f'"{python_exec}" "{os.path.abspath(__file__)}"', "/F"
        ]
        safe_run(cmd)
    elif SYSTEM == "linux":
        cron_job = f"0 0 */{interval} * * {sys.executable} {os.path.abspath(__file__)}"
        
        safe_run(["bash", "-lc", f'(crontab -l 2>/dev/null; echo "{cron_job}") | crontab -'])
    else:
        print("Scheduler not supported for this OS")
    print("Scheduler activated")


def remove_scheduler():
    if SYSTEM.startswith("win"):
        safe_run(["schtasks", "/Delete", "/TN", "AutoUpdater", "/F"])
    elif SYSTEM == "linux":
        safe_run(["crontab", "-r"])
    else:
        print("Remove scheduler not supported for this OS")
    print("Scheduler removed")


def config_menu(config):
    print("\nConfig")
    print("1 - Toggle update_all (current: {})".format(config.get("update_all")))
    print("2 - Ajouter app")
    print("3 - Ajouter exclusion")
    print("4 - Toggle schedule_enabled (current: {})".format(config.get("schedule_enabled")))
    print("5 - Toggle allow_system_updates (current: {})".format(config.get("allow_system_updates")))
    print("6 - Toggle auto_install_missing (current: {})".format(config.get("auto_install_missing")))
    print("7 - Afficher logo")
    print("0 - Retour")

    choice = input("Choix : ").strip()
    if choice == "1":
        config["update_all"] = not config.get("update_all", True)
    elif choice == "2":
        app = input("Nom app : ").strip()
        if app:
            config.setdefault("app_list", []).append(app)
    elif choice == "3":
        ex = input("Sous-chaîne à exclure : ").strip().lower()
        if ex:
            config.setdefault("exclude_list", []).append(ex)
    elif choice == "4":
        config["schedule_enabled"] = not config.get("schedule_enabled", False)
        if config["schedule_enabled"]:
            setup_scheduler(config)
        else:
            remove_scheduler()
    elif choice == "5":
        config["allow_system_updates"] = not config.get("allow_system_updates", False)
    elif choice == "6":
        config["auto_install_missing"] = not config.get("auto_install_missing", False)
    elif choice == "7":
        show_logo()
    save_config(config)


def main():
    ensure_directories()
    config = load_config()
    while True:
        print("\n=== AUTO UPDATER ===")
        print("Detected OS:", SYSTEM)
        print("1 - Update")
        print("2 - Config")
        print("3 - Update dev tools (Windows only)")
        print("0 - Quit")
        choice = input("Choice: ").strip()
        if choice == "1":
            if config.get("auto_update_apps", True):
                update_apps(config)
            else:
                print("Auto update disabled in config.")
        elif choice == "2":
            config_menu(config)
        elif choice == "3":
            update_dev_tools(config)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
