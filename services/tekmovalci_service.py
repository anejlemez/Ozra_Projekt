from repositories.tekmovalci_repository import *

def search_tekmovalci_service(ime):
    return search_tekmovalci_repo(ime)

def get_tekmovalec_service(id):
    return get_tekmovalec_repo(id)

def get_nastopi_service(id):
    return get_nastopi_repo(id)

def get_najboljsi_cas_service(id):
    return get_najboljsi_cas_repo(id)