from repositories.spremembe_repository import *


def create_sprememba_service(tabela, operacija, opis, tk_admin=None):
    create_sprememba_repo(tabela, operacija, opis, tk_admin)


def get_all_spremembe_service():
    return get_all_spremembe_repo()