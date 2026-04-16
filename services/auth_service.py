from repositories.auth_repository import get_admin_by_username_repo

def login_admin_service(data):
    uporabnisko_ime = data.get("uporIme")
    geslo = data.get("geslo")

    admin = get_admin_by_username_repo(uporabnisko_ime)

    if not admin:
        return {"success": False, "message": "Admin ne obstaja"}

    if admin["geslo"] != geslo:
        return {"success": False, "message": "Napačno geslo"}

    return {
        "success": True,
        "message": "Prijava uspešna",
        "admin": {
            "id_admina": admin["id_admina"],
            "ime": admin["ime"],
            "priimek": admin["priimek"],
            "email": admin["email"]
        }
    }