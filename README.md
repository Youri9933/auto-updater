# auto-updater

Français — 
---------------------------------

Description  
auto-updater est un petit script Python pour automatiser la mise à jour d'applications sur Windows (winget) et Linux (apt/pacman/dnf). Il garde un journal en Markdown (logs/update_log.md) et propose un mode d'installation pour les applications manquantes (Windows).

Principes de sécurité
- Ne pas exécuter sans inspection : le script lance des commandes système (sudo, winget, pacman, dnf). Vérifiez le code avant exécution.
- Les mises à jour système sous Linux sont désactivées par défaut ; activez-les explicitement via config.json (allow_system_updates).
- Les installations automatiques d'apps manquantes sont optionnelles (auto_install_missing).
- Le projet utilise des chemins relatifs (config.json, logs/, assets/) — pas de chemins absolus codés en dur.

Installation rapide
1. Cloner le dépôt :
   ```
   git clone <repo-url>
   cd auto-updater
   ```
2. (Optionnel) Créer un environnement virtuel :
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Lancer :
   ```
   python3 main.py
   ```

Configuration (config.json)
- Emplacement : ./config.json
- Exemple minimal :
```json
{
  "auto_update_apps": true,
  "update_all": true,
  "app_list": ["Visual Studio Code", "Git"],
  "exclude_list": ["driver", "nvidia"],
  "schedule_enabled": false,
  "day_interval": 7,
  "allow_system_updates": false,
  "auto_install_missing": false
}
```
- auto_update_apps : activer la mise à jour depuis le menu.
- update_all : true pour tout mettre à jour ; false pour utiliser app_list.
- allow_system_updates : required to run apt/pacman/dnf upgrades.
- auto_install_missing : si true, installe automatiquement les apps manquantes (Windows).

Utilisation
- Menu interactif : lancez `python3 main.py` et suivez les options :
  - 1 — Update
  - 2 — Config (modifier les options ci‑dessus)
  - 3 — Update dev tools (Windows uniquement)
  - 0 — Quitter

Logs
- Fichier : logs/update_log.md (format Markdown, entrées horodatées).
- Le script ouvre le log automatiquement si possible (xdg-open sur Linux, os.startfile sur Windows).

Scheduler
- Windows : crée une tâche avec schtasks (daily /MO day_interval).
- Linux : ajoute une entrée cron (0 0 */day_interval * *).
- Le scheduler n'est activé que si `schedule_enabled` est true.

Bonnes pratiques
- Inspectez le script avant d'exécuter.  
- Pour tests, ne pas activer allow_system_updates ni auto_install_missing.  
- Ajoutez `logs/` et `assets/` au .gitignore si vous stockez données sensibles localement.

Contribuer
- Fork → modifs → PR. Signalez clairement les tests et OS utilisés.

Licence
- Ajoutez un fichier LICENSE (MIT recommandé).

English — 
--------------------------------

Description  
auto-updater is a small Python tool to automate app updates on Windows (winget) and Linux (apt/pacman/dnf). It logs to Markdown (logs/update_log.md) and can offer to install missing apps on Windows.

Security principles
- Inspect code before running — it executes system commands (sudo, winget, pacman, dnf).
- Linux system updates are disabled by default; enable with allow_system_updates in config.json.
- Auto-install of missing apps is optional (auto_install_missing).
- Uses relative paths (config.json, logs/, assets/) — no hard-coded absolute paths.

Quick start
1. Clone:
   ```
   git clone <repo-url>
   cd auto-updater
   ```
2. Optional venv:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Run:
   ```
   python3 main.py
   ```

Configuration (config.json)
- Location: ./config.json
- Example: see French section above.
- Key flags: auto_update_apps, update_all, allow_system_updates, auto_install_missing.

Usage
- Run `python3 main.py` and use the interactive menu:
  - 1 — Update
  - 2 — Config
  - 3 — Update dev tools (Windows only)
  - 0 — Quit

Logs
- File: logs/update_log.md (timestamped Markdown entries).
- Script opens log automatically when possible (xdg-open / os.startfile).

Scheduler
- Windows: schtasks daily.
- Linux: cron entry added.
- Only active when schedule_enabled is true.

Best practices
- Review code first.
- Keep allow_system_updates and auto_install_missing off for initial tests.
- Add logs/ and assets/ to .gitignore if needed.

Contributing & License
- Fork / PR workflow. Add LICENSE (MIT recommended).

```<!-- filepath: /home/youri/Documents/proje de auto-mise-ajoure/auto-updater/README.md -->
# auto-updater

Français — 
---------------------------------

Description  
auto-updater est un petit script Python pour automatiser la mise à jour d'applications sur Windows (winget) et Linux (apt/pacman/dnf). Il garde un journal en Markdown (logs/update_log.md) et propose un mode d'installation pour les applications manquantes (Windows).

Principes de sécurité
- Ne pas exécuter sans inspection : le script lance des commandes système (sudo, winget, pacman, dnf). Vérifiez le code avant exécution.
- Les mises à jour système sous Linux sont désactivées par défaut ; activez-les explicitement via config.json (allow_system_updates).
- Les installations automatiques d'apps manquantes sont optionnelles (auto_install_missing).
- Le projet utilise des chemins relatifs (config.json, logs/, assets/) — pas de chemins absolus codés en dur.

Installation rapide
1. Cloner le dépôt :
   ```
   git clone <repo-url>
   cd auto-updater
   ```
2. (Optionnel) Créer un environnement virtuel :
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Lancer :
   ```
   python3 main.py
   ```

Configuration (config.json)
- Emplacement : ./config.json
- Exemple minimal :
```json
{
  "auto_update_apps": true,
  "update_all": true,
  "app_list": ["Visual Studio Code", "Git"],
  "exclude_list": ["driver", "nvidia"],
  "schedule_enabled": false,
  "day_interval": 7,
  "allow_system_updates": false,
  "auto_install_missing": false
}
```
- auto_update_apps : activer la mise à jour depuis le menu.
- update_all : true pour tout mettre à jour ; false pour utiliser app_list.
- allow_system_updates : required to run apt/pacman/dnf upgrades.
- auto_install_missing : si true, installe automatiquement les apps manquantes (Windows).

Utilisation
- Menu interactif : lancez `python3 main.py` et suivez les options :
  - 1 — Update
  - 2 — Config (modifier les options ci‑dessus)
  - 3 — Update dev tools (Windows uniquement)
  - 0 — Quitter

Logs
- Fichier : logs/update_log.md (format Markdown, entrées horodatées).
- Le script ouvre le log automatiquement si possible (xdg-open sur Linux, os.startfile sur Windows).

Scheduler
- Windows : crée une tâche avec schtasks (daily /MO day_interval).
- Linux : ajoute une entrée cron (0 0 */day_interval * *).
- Le scheduler n'est activé que si `schedule_enabled` est true.

Bonnes pratiques
- Inspectez le script avant d'exécuter.  
- Pour tests, ne pas activer allow_system_updates ni auto_install_missing.  
- Ajoutez `logs/` et `assets/` au .gitignore si vous stockez données sensibles localement.

Contribuer
- Fork → modifs → PR. Signalez clairement les tests et OS utilisés.

Licence
- Ajoutez un fichier LICENSE (MIT recommandé).

English — 
--------------------------------

Description  
auto-updater is a small Python tool to automate app updates on Windows (winget) and Linux (apt/pacman/dnf). It logs to Markdown (logs/update_log.md) and can offer to install missing apps on Windows.

Security principles
- Inspect code before running — it executes system commands (sudo, winget, pacman, dnf).
- Linux system updates are disabled by default; enable with allow_system_updates in config.json.
- Auto-install of missing apps is optional (auto_install_missing).
- Uses relative paths (config.json, logs/, assets/) — no hard-coded absolute paths.

Quick start
1. Clone:
   ```
   git clone <repo-url>
   cd auto-updater
   ```
2. Optional venv:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Run:
   ```
   python3 main.py
   ```

Configuration (config.json)
- Location: ./config.json
- Example: see French section above.
- Key flags: auto_update_apps, update_all, allow_system_updates, auto_install_missing.

Usage
- Run `python3 main.py` and use the interactive menu:
  - 1 — Update
  - 2 — Config
  - 3 — Update dev tools (Windows only)
  - 0 — Quit

Logs
- File: logs/update_log.md (timestamped Markdown entries).
- Script opens log automatically when possible (xdg-open / os.startfile).

Scheduler
- Windows: schtasks daily.
- Linux: cron entry added.
- Only active when schedule_enabled is true.

Best practices
- Review code first.
- Keep allow_system_updates and auto_install_missing off for initial tests.
- Add logs/ and assets/ to .gitignore if needed.

Contributing & License
- Fork / PR workflow. Add LICENSE (MIT recommended).
