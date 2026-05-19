from repositories.rezultati_repository import *
from services.spremembe_service import create_sprememba_service


def preveri_obvezna_polja(data):
    napake = []

    if not data.get("tk_tekmovalec"):
        napake.append("Tekmovalec je obvezen.")

    if not data.get("tk_tekmovanje"):
        napake.append("Tekmovanje je obvezno.")

    return napake


def preveri_int_polje(data, field, naziv):
    if field in data and data.get(field) not in (None, ""):
        try:
            int(data.get(field))
        except ValueError:
            return f"{naziv} mora biti celo število."
    return None


def preveri_float_polje(data, field, naziv):
    if field in data and data.get(field) not in (None, ""):
        try:
            float(str(data.get(field)).replace(",", "."))
        except ValueError:
            return f"{naziv} mora biti število."
    return None


def validiraj_rezultat(data, obvezna_polja=True):
    napake = []

    if obvezna_polja:
        napake.extend(preveri_obvezna_polja(data))

    int_preverjanja = [
        ("overallRank", "Skupna uvrstitev"),
        ("genderRank", "Uvrstitev po spolu"),
        ("divRank", "Uvrstitev v diviziji"),
        ("tk_tekmovalec", "Tekmovalec"),
        ("tk_tekmovanje", "Tekmovanje")
    ]

    for field, naziv in int_preverjanja:
        napaka = preveri_int_polje(data, field, naziv)
        if napaka:
            napake.append(napaka)

    napaka = preveri_float_polje(data, "tocke", "Točke")
    if napaka:
        napake.append(napaka)

    return napake


def create_rezultat_service(data):
    napake = validiraj_rezultat(data, obvezna_polja=True)

    if napake:
        return {
            "success": False,
            "errors": napake
        }

    rezultat_id = create_rezultat_repo(data)

    create_sprememba_service(
        tabela="rezultati",
        operacija="CREATE",
        opis=f"Dodan rezultat z ID {rezultat_id}",
        tk_admin=data.get("tk_admin")
    )

    return {
        "success": True,
        "id": rezultat_id
    }


def get_rezultat_service(id):
    rezultat = get_rezultat_repo(id)

    if not rezultat:
        return {
            "success": False,
            "message": "Rezultat ne obstaja."
        }

    return {
        "success": True,
        "data": rezultat
    }


def update_rezultat_service(id, data):
    napake = validiraj_rezultat(data, obvezna_polja=False)

    if napake:
        return {
            "success": False,
            "errors": napake
        }

    updated = update_rezultat_repo(id, data)

    if updated > 0:
        create_sprememba_service(
            tabela="rezultati",
            operacija="UPDATE",
            opis=f"Posodobljen rezultat z ID {id}",
            tk_admin=data.get("tk_admin")
        )

    return {
        "success": updated > 0,
        "updated": updated
    }


def delete_rezultat_service(id, data=None):
    deleted = delete_rezultat_repo(id)

    if deleted > 0:
        create_sprememba_service(
            tabela="rezultati",
            operacija="DELETE",
            opis=f"Izbrisan rezultat z ID {id}",
            tk_admin=(data or {}).get("tk_admin")
        )

    return {
        "success": deleted > 0,
        "deleted": deleted
    }