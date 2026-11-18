"""First-boot and every-boot settings for DeepTutor on Railway.

DeepTutor's Docker image ignores environment variables for its own settings
and reads JSON files under /app/data/user/settings instead. This script writes
the few values a Railway deploy needs into those files:

* auth.json   - login turned on, admin user from ADMIN_USERNAME, bcrypt hash of
                ADMIN_PASSWORD (rehashed only when the password changes),
                secure cookies when served from a Railway HTTPS domain.
* system.json - frontend port from PORT, public domain added to CORS origins.

Everything else (models, API keys, knowledge bases) stays as the user set it
in the web UI, on the /app/data volume.
"""

import os
import sys
from pathlib import Path

import bcrypt

from deeptutor.services.setup import init_user_directories
from deeptutor.services.config import get_runtime_settings_service


def log(msg: str) -> None:
    print(f"[railway-setup] {msg}", flush=True)


def main() -> int:
    init_user_directories(Path("/app"))
    service = get_runtime_settings_service()

    username = os.environ.get("ADMIN_USERNAME", "").strip() or "admin"
    password = os.environ.get("ADMIN_PASSWORD", "")
    if len(password) < 12:
        log("ADMIN_PASSWORD is missing or shorter than 12 characters; refusing to start "
            "an internet-facing DeepTutor without a login. Set ADMIN_PASSWORD and redeploy.")
        return 1

    domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "").strip()

    auth = service.load_auth(include_process_overrides=False)
    current_hash = str(auth.get("password_hash") or "")
    same = False
    if current_hash and auth.get("username") == username:
        try:
            same = bcrypt.checkpw(password.encode(), current_hash.encode())
        except ValueError:
            same = False
    auth["enabled"] = True
    auth["username"] = username
    if not same:
        auth["password_hash"] = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        log(f"admin login set for user '{username}'")
    auth["cookie_secure"] = bool(domain)
    service.save_auth(auth)

    system = service.load_system(include_process_overrides=False)
    port = os.environ.get("PORT", "").strip()
    if port.isdigit() and 0 < int(port) < 65536:
        if int(port) == int(system.get("backend_port") or 8001):
            log(f"PORT {port} clashes with the backend port; keeping frontend port "
                f"{system.get('frontend_port')}")
        else:
            system["frontend_port"] = int(port)
    origins = list(system.get("cors_origins") or [])
    if domain:
        origin = f"https://{domain}"
        if origin not in origins:
            origins.append(origin)
    system["cors_origins"] = origins
    service.save_system(system)
    log(f"web UI on port {system['frontend_port']}, login enabled")
    return 0


if __name__ == "__main__":
    sys.exit(main())
