from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox
)


class RezultatForm(QDialog):
    def __init__(self, parent=None, rezultat=None, tekmovalec_id=None, tekmovanje_id=None):
        super().__init__(parent)

        self.rezultat = rezultat or {}
        self.tekmovalec_id = tekmovalec_id
        self.tekmovanje_id = tekmovanje_id
        self.saved_data = None

        self.setWindowTitle("Rezultat")
        self.setMinimumWidth(450)

        self.init_ui()
        self.fill_data()

    def init_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        self.overall_rank = QLineEdit()
        self.gender_rank = QLineEdit()
        self.div_rank = QLineEdit()
        self.bib = QLineEdit()
        self.divizija = QLineEdit()
        self.tocke = QLineEdit()
        self.plavanje = QLineEdit()
        self.t1 = QLineEdit()
        self.kolesarjenje = QLineEdit()
        self.t2 = QLineEdit()
        self.tek = QLineEdit()
        self.skupni_cas = QLineEdit()
        self.tk_tekmovalec = QLineEdit()
        self.tk_tekmovanje = QLineEdit()

        self.tk_tekmovalec.setReadOnly(True)
        self.tk_tekmovanje.setReadOnly(True)

        form.addRow("Skupna uvrstitev:", self.overall_rank)
        form.addRow("Uvrstitev po spolu:", self.gender_rank)
        form.addRow("Uvrstitev v diviziji:", self.div_rank)
        form.addRow("Bib:", self.bib)
        form.addRow("Divizija:", self.divizija)
        form.addRow("Točke:", self.tocke)
        form.addRow("Plavanje:", self.plavanje)
        form.addRow("T1:", self.t1)
        form.addRow("Kolesarjenje:", self.kolesarjenje)
        form.addRow("T2:", self.t2)
        form.addRow("Tek:", self.tek)
        form.addRow("Skupni čas:", self.skupni_cas)
        form.addRow("Tekmovalec ID:", self.tk_tekmovalec)
        form.addRow("Tekmovanje ID:", self.tk_tekmovanje)

        button_layout = QHBoxLayout()

        self.save_btn = QPushButton("Shrani")
        self.cancel_btn = QPushButton("Prekliči")

        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(form)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def fill_data(self):
        self.overall_rank.setText(str(self.rezultat.get("overallRank") or ""))
        self.gender_rank.setText(str(self.rezultat.get("genderRank") or ""))
        self.div_rank.setText(str(self.rezultat.get("divRank") or ""))
        self.bib.setText(str(self.rezultat.get("bib") or ""))
        self.divizija.setText(str(self.rezultat.get("divizija") or ""))
        self.tocke.setText(str(self.rezultat.get("tocke") or ""))
        self.plavanje.setText(str(self.rezultat.get("plavanje") or ""))
        self.t1.setText(str(self.rezultat.get("t1") or ""))
        self.kolesarjenje.setText(str(self.rezultat.get("kolesarjenje") or ""))
        self.t2.setText(str(self.rezultat.get("t2") or ""))
        self.tek.setText(str(self.rezultat.get("tek") or ""))
        self.skupni_cas.setText(str(self.rezultat.get("skupniCas") or ""))

        tekmovalec = self.rezultat.get("tk_tekmovalec") or self.tekmovalec_id or ""
        tekmovanje = self.rezultat.get("tk_tekmovanje") or self.tekmovanje_id or ""

        self.tk_tekmovalec.setText(str(tekmovalec))
        self.tk_tekmovanje.setText(str(tekmovanje))

    def empty_to_none(self, value):
        value = value.strip()
        return value if value != "" else None

    def validate_int(self, value, field_name, required=False):
        value = value.strip()

        if required and not value:
            return False, f"{field_name} je obvezen."

        if value:
            try:
                int(value)
            except ValueError:
                return False, f"{field_name} mora biti celo število."

        return True, None

    def validate_float(self, value, field_name):
        value = value.strip()

        if value:
            try:
                float(value.replace(",", "."))
            except ValueError:
                return False, f"{field_name} mora biti število."

        return True, None

    def save(self):
        checks = [
            self.validate_int(self.overall_rank.text(), "Skupna uvrstitev"),
            self.validate_int(self.gender_rank.text(), "Uvrstitev po spolu"),
            self.validate_int(self.div_rank.text(), "Uvrstitev v diviziji"),
            self.validate_int(self.tk_tekmovalec.text(), "Tekmovalec", required=True),
            self.validate_int(self.tk_tekmovanje.text(), "Tekmovanje", required=True),
            self.validate_float(self.tocke.text(), "Točke")
        ]

        for ok, message in checks:
            if not ok:
                QMessageBox.warning(self, "Napaka", message)
                return

        self.saved_data = {
            "overallRank": int(self.overall_rank.text()) if self.overall_rank.text().strip() else None,
            "genderRank": int(self.gender_rank.text()) if self.gender_rank.text().strip() else None,
            "divRank": int(self.div_rank.text()) if self.div_rank.text().strip() else None,
            "bib": self.empty_to_none(self.bib.text()),
            "divizija": self.empty_to_none(self.divizija.text()),
            "tocke": float(self.tocke.text().replace(",", ".")) if self.tocke.text().strip() else None,
            "plavanje": self.empty_to_none(self.plavanje.text()),
            "t1": self.empty_to_none(self.t1.text()),
            "kolesarjenje": self.empty_to_none(self.kolesarjenje.text()),
            "t2": self.empty_to_none(self.t2.text()),
            "tek": self.empty_to_none(self.tek.text()),
            "skupniCas": self.empty_to_none(self.skupni_cas.text()),
            "tk_tekmovalec": int(self.tk_tekmovalec.text()),
            "tk_tekmovanje": int(self.tk_tekmovanje.text())
        }

        self.accept()