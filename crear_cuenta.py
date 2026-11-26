import argparse
from getpass import GetPassWarning, getpass
from hmac import compare_digest
import json
import warnings

from local_auth import ROLES, hash_password, normalize_username


def main():
    parser = argparse.ArgumentParser(description="Genera una cuenta RAP para los secretos de Streamlit.")
    parser.add_argument("usuario", help="Usuario de acceso, por ejemplo coordinacion.rap")
    parser.add_argument("--nombre", required=True, help="Nombre que verá el usuario en la app")
    parser.add_argument("--rol", choices=sorted(ROLES), default="admin")
    args = parser.parse_args()

    username = normalize_username(args.usuario)
    if not username or not args.nombre.strip():
        parser.error("Usa un usuario de hasta 64 caracteres y un nombre para mostrar.")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", GetPassWarning)
            password = getpass("Nueva contraseña (mínimo 16 caracteres): ")
            confirmation = getpass("Confirma la contraseña: ")
    except (EOFError, GetPassWarning, KeyboardInterrupt):
        parser.exit(1, "Abre una terminal interactiva para introducir la contraseña de forma oculta.\n")
    if not compare_digest(password.encode("utf-8"), confirmation.encode("utf-8")):
        parser.error("Las contraseñas no coinciden.")
    try:
        encoded = hash_password(password)
    except ValueError as exc:
        parser.error(str(exc))

    print(f'\n[rap_accounts."{username}"]')
    print(f"nombre = {json.dumps(args.nombre.strip(), ensure_ascii=False)}")
    print(f'rol = "{args.rol}"')
    print(f'hash_contrasena = "{encoded}"')


if __name__ == "__main__":
    main()
