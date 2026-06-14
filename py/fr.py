import os
import requests
import pyfiglet
from base64 import b64encode
from pywidevine.L3.decrypt.wvdecryptcustom import WvDecrypt
from pywidevine.L3.cdm import deviceconfig

# ===================== CONSTANTES ===================== #
# Couleurs terminal
RED = "\x1b[38;5;160m"
GREEN = "\x1b[38;5;46m"
CYAN = "\x1b[38;5;14m"
YELLOW = "\x1b[38;5;226m"
END = "\x1b[0m"

# ===================== AFFICHAGE ===================== #

def print_title():
    title = pyfiglet.figlet_format("Widevine Decryptor Keys", font="slant", width=150)
    print(f"{CYAN}{title}{END}")

# ===================== VALIDATION ===================== #

def validate_pssh(pssh: str) -> bool:
    if len(pssh) >= 150:
        print(f"{RED}❌ PSSH invalide{END}")
        return False
    return True

# ===================== WIDEVINE ===================== #

def get_widevine_keys(pssh: str, headers: str, LICENCE_URL: str):
    wvdecrypt = WvDecrypt(init_data_b64=pssh, device=deviceconfig.device_android_generic)
    try:
        response = requests.post(LICENCE_URL, data=wvdecrypt.get_challenge(), headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"{RED}Erreur licence Widevine : {e}{END}")
        return []

    license_b64 = b64encode(response.content)
    wvdecrypt.update_license(license_b64)
    success, keys = wvdecrypt.start_process()
    return keys if success else []

# ===================== MAIN ===================== #

def main():
    print_title()
    pssh = input(f"{RED}PSSH:{END} {YELLOW}")
    if not validate_pssh(pssh):
        print(f"{RED}PSSH invalide.{END}")
        return

    token = input(f"{RED}dt-auth-token:{END} {YELLOW}")
    if not token:
        print(f"{RED}Le token ne peut pas être vide.{END}")
        return
    headers = {"x-dt-auth-token": token}
    LICENCE_URL = "https://lic.drmtoday.com/license-proxy-widevine/cenc/?specConform=true"
    keys = get_widevine_keys(pssh, headers, LICENCE_URL)
    if not keys:
        print(f"{RED}❌ Aucune clé retrouvée.{END}")
        return

    for key in keys:
        print(f"{GREEN}--KEY:{END} {RED}{key}{END}")

    input("\nAppuyez sur Entrée pour quitter...")


# ===================== EXEC ===================== #

if __name__ == "__main__":
    main()
