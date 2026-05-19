import requests
from config import API_BASE_URL


class ApiClient:
    def __init__(self):
        self.base_url = API_BASE_URL

    def _url(self, endpoint):
        return f"{self.base_url}{endpoint}"

    def get(self, endpoint, params=None):
        try:
            response = requests.get(self._url(endpoint), params=params, timeout=10)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Napaka povezave: {e}"
            }

    def post(self, endpoint, data=None):
        try:
            response = requests.post(self._url(endpoint), json=data, timeout=10)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Napaka povezave: {e}"
            }

    def put(self, endpoint, data=None):
        try:
            response = requests.put(self._url(endpoint), json=data, timeout=10)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Napaka povezave: {e}"
            }

    def delete(self, endpoint, data=None):
        try:
            response = requests.delete(self._url(endpoint), json=data, timeout=10)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Napaka povezave: {e}"
            }

    def _handle_response(self, response):
        try:
            data = response.json()
        except ValueError:
            return {
                "success": False,
                "error": "Strežnik ni vrnil JSON odgovora."
            }

        if response.status_code >= 400:
            return {
                "success": False,
                "status_code": response.status_code,
                "error": data
            }

        return data

    def login(self, upor_ime, geslo):
        return self.post("/auth/login", {
            "uporIme": upor_ime,
            "geslo": geslo
        })

    def get_tekmovanja(self):
        return self.get("/tekmovanja")

    def get_rezultati_tekmovanja(self, tekmovanje_id):
        return self.get(f"/tekmovanja/{tekmovanje_id}/rezultati")

    def search_tekmovalci(self, ime):
        return self.get("/tekmovalci/iskanje", {
            "ime": ime
        })

    def get_nastopi_tekmovalca(self, tekmovalec_id):
        return self.get(f"/tekmovalci/{tekmovalec_id}/nastopi")

    def create_rezultat(self, data):
        return self.post("/rezultati", data)

    def update_rezultat(self, rezultat_id, data):
        return self.put(f"/rezultati/{rezultat_id}", data)

    def delete_rezultat(self, rezultat_id):
        return self.delete(f"/rezultati/{rezultat_id}")

    def get_nepopolni(self):
        return self.get("/validacija/nepopolni")

    def get_duplikati(self):
        return self.get("/validacija/duplikati")

    def primerjaj_tekmovalca(self, tekmovalec1_id, tekmovalec2_id):
        return self.get("/primerjava", {
            "tekmovalec1": tekmovalec1_id,
            "tekmovalec2": tekmovalec2_id
        })
    
    def get_spremembe(self):
        return self.get("/spremembe")