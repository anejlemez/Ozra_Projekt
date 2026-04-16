from repositories.tekmovanja_repository import (
    get_all_tekmovanja_repo,
    get_one_tekmovanje_repo,
    get_rezultati_za_tekmovanje_repo
)

def get_all_tekmovanja_service():
    return get_all_tekmovanja_repo()

def get_one_tekmovanje_service(tekmovanje_id):
    return get_one_tekmovanje_repo(tekmovanje_id)

def get_rezultati_za_tekmovanje_service(tekmovanje_id):
    return get_rezultati_za_tekmovanje_repo(tekmovanje_id)