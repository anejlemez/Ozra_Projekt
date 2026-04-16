from repositories.tekmovanja_repository import *

def get_all_tekmovanja_service():
    return get_all_tekmovanja_repo()

def get_one_tekmovanje_service(id):
    return get_one_tekmovanje_repo(id)

def get_rezultati_tekmovanja_service(id):
    return get_rezultati_tekmovanja_repo(id)