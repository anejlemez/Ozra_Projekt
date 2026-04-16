from repositories.auth_repository import get_admin_repo

def login_service(data):
    admin = get_admin_repo(data["uporIme"])
    if not admin or admin["geslo"] != data["geslo"]:
        return {"success": False}
    return {"success": True, "admin": admin}