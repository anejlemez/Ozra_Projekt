from repositories.rezultati_repository import *

def create_rezultat_service(data):
    return {"id": create_rezultat_repo(data)}

def get_rezultat_service(id):
    return get_rezultat_repo(id)

def update_rezultat_service(id, data):
    return {"updated": update_rezultat_repo(id, data)}

def delete_rezultat_service(id):
    return {"deleted": delete_rezultat_repo(id)}