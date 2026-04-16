from repositories.rezultati_repository import (
    create_rezultat_repo,
    update_rezultat_repo,
    delete_rezultat_repo
)

def create_rezultat_service(data):
    required_fields = ["tk_tekmovalec", "tk_tekmovanje"]
    for field in required_fields:
        if field not in data or data[field] in [None, ""]:
            return {"message": f"Manjka polje: {field}"}

    new_id = create_rezultat_repo(data)
    return {"message": "Rezultat uspešno dodan", "id": new_id}

def update_rezultat_service(rezultat_id, data):
    updated = update_rezultat_repo(rezultat_id, data)
    if updated == 0:
        return {"message": "Rezultat ne obstaja"}
    return {"message": "Rezultat uspešno posodobljen"}

def delete_rezultat_service(rezultat_id):
    deleted = delete_rezultat_repo(rezultat_id)
    if deleted == 0:
        return {"message": "Rezultat ne obstaja"}
    return {"message": "Rezultat uspešno izbrisan"}