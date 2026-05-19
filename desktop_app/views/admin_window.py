import csv

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
    QComboBox,
    QFileDialog
)
from PyQt5.QtCore import Qt

from translations import t
from ui_style import apply_base_style

from views.rezultat_form import RezultatForm


class AdminWindow(QMainWindow):
    def __init__(self, api, lang="sl", admin=None):
        super().__init__()

        self.api = api
        self.lang = lang
        self.admin = admin or {}
        self.admin_id = self.admin.get("id_admina")

        self.tekmovanja_data = []
        self.rezultati_data = []
        self.tekmovalci_data = []
        self.primerjava_data = []
        self.primerjava_first_id = None
        self.primerjava_second_id = None

        self.setWindowTitle(t(self.lang, "app_title"))
        self.setGeometry(200, 100, 1200, 700)
        apply_base_style(self)

        self.init_ui()
        self.load_tekmovanja()
        self.load_spremembe()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(10)

        top_layout = QHBoxLayout()

        self.title_label = QLabel(t(self.lang, "app_title"))
        self.title_label.setObjectName("SectionTitle")
        self.title_label.setWordWrap(True)

        self.language_label = QLabel(t(self.lang, "language"))
        self.language_select = QComboBox()
        self.language_select.addItem("Slovenščina", "sl")
        self.language_select.addItem("English", "en")

        if self.lang == "en":
            self.language_select.setCurrentIndex(1)

        self.language_select.currentIndexChanged.connect(self.change_language)

        top_layout.addWidget(self.title_label)
        top_layout.addStretch()
        top_layout.addWidget(self.language_label)
        top_layout.addWidget(self.language_select)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.tab_tekmovanja = QWidget()
        self.tab_tekmovalci = QWidget()
        self.tab_primerjava = QWidget()
        self.tab_validacija = QWidget()
        self.tab_spremembe = QWidget()

        self.tabs.addTab(self.tab_tekmovanja, t(self.lang, "competitions"))
        self.tabs.addTab(self.tab_tekmovalci, t(self.lang, "competitors"))
        self.tabs.addTab(self.tab_primerjava, t(self.lang, "comparison"))
        self.tabs.addTab(self.tab_validacija, t(self.lang, "validation"))
        self.tabs.addTab(self.tab_spremembe, t(self.lang, "changes"))

        self.init_tekmovanja_tab()
        self.init_tekmovalci_tab()
        self.init_primerjava_tab()
        self.init_validacija_tab()
        self.init_spremembe_tab()

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.tabs)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def init_tekmovanja_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        button_layout = QHBoxLayout()

        self.refresh_tekmovanja_btn = QPushButton(t(self.lang, "refresh"))
        self.refresh_tekmovanja_btn.clicked.connect(self.load_tekmovanja)

        self.add_rezultat_btn = QPushButton(t(self.lang, "add"))
        self.add_rezultat_btn.clicked.connect(self.add_rezultat)

        self.edit_rezultat_btn = QPushButton(t(self.lang, "edit"))
        self.edit_rezultat_btn.clicked.connect(self.edit_selected_rezultat)

        self.delete_rezultat_btn = QPushButton(t(self.lang, "delete"))
        self.delete_rezultat_btn.clicked.connect(self.delete_selected_rezultat)

        self.export_csv_btn = QPushButton("Izvozi CSV")
        self.export_csv_btn.clicked.connect(self.export_rezultati_csv)

        button_layout.addWidget(self.refresh_tekmovanja_btn)
        button_layout.addWidget(self.add_rezultat_btn)
        button_layout.addWidget(self.edit_rezultat_btn)
        button_layout.addWidget(self.delete_rezultat_btn)
        button_layout.addWidget(self.export_csv_btn)
        button_layout.addStretch()

        self.tekmovanja_label = QLabel(t(self.lang, "competitions"))

        self.tekmovanja_table = QTableWidget()
        self.tekmovanja_table.setColumnCount(5)
        self.tekmovanja_table.setHorizontalHeaderLabels([
            "ID", "Naziv", "Leto", "Tip", "Lokacija"
        ])
        self.tekmovanja_table.cellClicked.connect(self.on_tekmovanje_selected)
        self.tekmovanja_table.setSelectionBehavior(QTableWidget.SelectRows)

        self.rezultati_label = QLabel(t(self.lang, "results"))

        self.rezultati_table = QTableWidget()
        self.rezultati_table.setColumnCount(11)
        self.rezultati_table.setHorizontalHeaderLabels([
            "ID", "Tekmovalec", "Overall", "Gender", "Div",
            "Bib", "Divizija", "Plavanje", "Kolesarjenje", "Tek", "Skupni čas"
        ])
        self.rezultati_table.setSelectionBehavior(QTableWidget.SelectRows)

        layout.addLayout(button_layout)
        layout.addWidget(self.tekmovanja_label)
        layout.addWidget(self.tekmovanja_table)
        layout.addWidget(self.rezultati_label)
        layout.addWidget(self.rezultati_table)

        self.tab_tekmovanja.setLayout(layout)

    def init_tekmovalci_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Vnesi ime tekmovalca")

        self.search_btn = QPushButton(t(self.lang, "search"))
        self.search_btn.clicked.connect(self.search_tekmovalci)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)

        self.tekmovalci_table = QTableWidget()
        self.tekmovalci_table.setColumnCount(4)
        self.tekmovalci_table.setHorizontalHeaderLabels([
            "ID", "Ime in priimek", "Starost", "Država"
        ])
        self.tekmovalci_table.setSelectionBehavior(QTableWidget.SelectRows)

        self.nastopi_btn = QPushButton("Prikaži nastope izbranega tekmovalca")
        self.nastopi_btn.clicked.connect(self.load_nastopi_selected_tekmovalec)

        self.nastopi_table = QTableWidget()
        self.nastopi_table.setColumnCount(8)
        self.nastopi_table.setHorizontalHeaderLabels([
            "ID", "Overall", "Gender", "Div", "Bib", "Divizija", "Skupni čas", "Tekmovanje ID"
        ])

        layout.addLayout(search_layout)
        layout.addWidget(self.tekmovalci_table)
        layout.addWidget(self.nastopi_btn)
        layout.addWidget(self.nastopi_table)

        self.tab_tekmovalci.setLayout(layout)

    def init_validacija_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        button_layout = QHBoxLayout()

        self.nepopolni_btn = QPushButton(t(self.lang, "incomplete_results"))
        self.nepopolni_btn.clicked.connect(self.load_nepopolni)

        self.duplikati_btn = QPushButton(t(self.lang, "duplicates"))
        self.duplikati_btn.clicked.connect(self.load_duplikati)

        button_layout.addWidget(self.nepopolni_btn)
        button_layout.addWidget(self.duplikati_btn)
        button_layout.addStretch()

        self.validacija_table = QTableWidget()
        self.validacija_table.setColumnCount(6)
        self.validacija_table.setHorizontalHeaderLabels([
            "ID / Tekmovalec", "Tekmovanje", "Count", "Overall", "Skupni čas", "Opis"
        ])

        layout.addLayout(button_layout)
        layout.addWidget(self.validacija_table)

        self.tab_validacija.setLayout(layout)

    def change_language(self):
        self.lang = self.language_select.currentData()

        self.setWindowTitle(t(self.lang, "app_title"))
        self.title_label.setText(t(self.lang, "app_title"))
        self.language_label.setText(t(self.lang, "language"))

        self.tabs.setTabText(0, t(self.lang, "competitions"))
        self.tabs.setTabText(1, t(self.lang, "competitors"))
        self.tabs.setTabText(2, t(self.lang, "comparison"))
        self.tabs.setTabText(3, t(self.lang, "validation"))
        self.tabs.setTabText(4, t(self.lang, "changes"))

        self.refresh_tekmovanja_btn.setText(t(self.lang, "refresh"))
        self.add_rezultat_btn.setText(t(self.lang, "add"))
        self.edit_rezultat_btn.setText(t(self.lang, "edit"))
        self.delete_rezultat_btn.setText(t(self.lang, "delete"))
        self.search_btn.setText(t(self.lang, "search"))
        self.primerjava_search_btn.setText(t(self.lang, "search"))
        self.primerjava_select_first_btn.setText(t(self.lang, "select_first"))
        self.primerjava_select_second_btn.setText(t(self.lang, "select_second"))
        self.primerjava_compare_btn.setText(t(self.lang, "compare"))
        self.nepopolni_btn.setText(t(self.lang, "incomplete_results"))
        self.duplikati_btn.setText(t(self.lang, "duplicates"))
        self.tekmovanja_label.setText(t(self.lang, "competitions"))
        self.rezultati_label.setText(t(self.lang, "results"))
        self.refresh_spremembe_btn.setText(t(self.lang, "refresh"))

        if self.lang == "sl":
            self.export_csv_btn.setText("Izvozi CSV")
        else:
            self.export_csv_btn.setText("Export CSV")

    def load_tekmovanja(self):
        data = self.api.get_tekmovanja()

        if not isinstance(data, list):
            QMessageBox.warning(self, "Napaka", "Tekmovanj ni bilo mogoče naložiti.")
            return

        self.tekmovanja_data = data
        self.tekmovanja_table.setRowCount(len(data))

        for row, item in enumerate(data):
            self.tekmovanja_table.setItem(row, 0, QTableWidgetItem(str(item.get("id_tekmovanja", ""))))
            self.tekmovanja_table.setItem(row, 1, QTableWidgetItem(str(item.get("naziv", ""))))
            self.tekmovanja_table.setItem(row, 2, QTableWidgetItem(str(item.get("leto", ""))))
            self.tekmovanja_table.setItem(row, 3, QTableWidgetItem(str(item.get("tip_tekmovanja", ""))))
            self.tekmovanja_table.setItem(row, 4, QTableWidgetItem(str(item.get("lokacija", ""))))

        self.tekmovanja_table.resizeColumnsToContents()

    def on_tekmovanje_selected(self, row, column):
        tekmovanje = self.tekmovanja_data[row]
        tekmovanje_id = tekmovanje.get("id_tekmovanja")

        if tekmovanje_id:
            self.load_rezultati_tekmovanja(tekmovanje_id)

    def load_rezultati_tekmovanja(self, tekmovanje_id):
        data = self.api.get_rezultati_tekmovanja(tekmovanje_id)

        if not isinstance(data, list):
            QMessageBox.warning(self, "Napaka", "Rezultatov ni bilo mogoče naložiti.")
            return

        self.rezultati_data = data
        self.rezultati_table.setRowCount(len(data))

        for row, item in enumerate(data):
            self.rezultati_table.setItem(row, 0, QTableWidgetItem(str(item.get("id_rezultata", ""))))
            self.rezultati_table.setItem(row, 1, QTableWidgetItem(str(item.get("ime_priimek", ""))))
            self.rezultati_table.setItem(row, 2, QTableWidgetItem(str(item.get("overallRank", ""))))
            self.rezultati_table.setItem(row, 3, QTableWidgetItem(str(item.get("genderRank", ""))))
            self.rezultati_table.setItem(row, 4, QTableWidgetItem(str(item.get("divRank", ""))))
            self.rezultati_table.setItem(row, 5, QTableWidgetItem(str(item.get("bib", ""))))
            self.rezultati_table.setItem(row, 6, QTableWidgetItem(str(item.get("divizija", ""))))
            self.rezultati_table.setItem(row, 7, QTableWidgetItem(str(item.get("plavanje", ""))))
            self.rezultati_table.setItem(row, 8, QTableWidgetItem(str(item.get("kolesarjenje", ""))))
            self.rezultati_table.setItem(row, 9, QTableWidgetItem(str(item.get("tek", ""))))
            self.rezultati_table.setItem(row, 10, QTableWidgetItem(str(item.get("skupniCas", ""))))

        self.rezultati_table.resizeColumnsToContents()

    def search_tekmovalci(self):
        ime = self.search_input.text().strip()

        if not ime:
            QMessageBox.warning(self, "Napaka", "Vnesi ime tekmovalca.")
            return

        data = self.api.search_tekmovalci(ime)

        if not isinstance(data, list):
            QMessageBox.warning(self, "Napaka", "Tekmovalcev ni bilo mogoče naložiti.")
            return

        self.tekmovalci_data = data
        self.tekmovalci_table.setRowCount(len(data))

        for row, item in enumerate(data):
            self.tekmovalci_table.setItem(row, 0, QTableWidgetItem(str(item.get("id_tekmovalec", ""))))
            self.tekmovalci_table.setItem(row, 1, QTableWidgetItem(str(item.get("ime_priimek", ""))))
            self.tekmovalci_table.setItem(row, 2, QTableWidgetItem(str(item.get("starost", ""))))
            self.tekmovalci_table.setItem(row, 3, QTableWidgetItem(str(item.get("drzava", ""))))

        self.tekmovalci_table.resizeColumnsToContents()

    def load_nastopi_selected_tekmovalec(self):
        row = self.tekmovalci_table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Napaka", "Najprej izberi tekmovalca.")
            return

        tekmovalec_id = self.tekmovalci_table.item(row, 0).text()
        data = self.api.get_nastopi_tekmovalca(tekmovalec_id)

        if not isinstance(data, list):
            QMessageBox.warning(self, "Napaka", "Nastopov ni bilo mogoče naložiti.")
            return

        self.nastopi_table.setRowCount(len(data))

        for row, item in enumerate(data):
            self.nastopi_table.setItem(row, 0, QTableWidgetItem(str(item.get("id_rezultata", ""))))
            self.nastopi_table.setItem(row, 1, QTableWidgetItem(str(item.get("overallRank", ""))))
            self.nastopi_table.setItem(row, 2, QTableWidgetItem(str(item.get("genderRank", ""))))
            self.nastopi_table.setItem(row, 3, QTableWidgetItem(str(item.get("divRank", ""))))
            self.nastopi_table.setItem(row, 4, QTableWidgetItem(str(item.get("bib", ""))))
            self.nastopi_table.setItem(row, 5, QTableWidgetItem(str(item.get("divizija", ""))))
            self.nastopi_table.setItem(row, 6, QTableWidgetItem(str(item.get("skupniCas", ""))))
            self.nastopi_table.setItem(row, 7, QTableWidgetItem(str(item.get("tk_tekmovanje", ""))))

        self.nastopi_table.resizeColumnsToContents()

    def delete_selected_rezultat(self):
        row = self.rezultati_table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Napaka", "Najprej izberi rezultat.")
            return

        rezultat_id = self.rezultati_table.item(row, 0).text()

        odgovor = QMessageBox.question(
            self,
            "Brisanje",
            f"Ali res želiš izbrisati rezultat ID {rezultat_id}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if odgovor != QMessageBox.Yes:
            return

        result = self.api.delete_rezultat(rezultat_id, {"tk_admin": self.admin_id})

        if result.get("success"):
            QMessageBox.information(self, "Uspeh", "Rezultat je bil izbrisan.")
            self.rezultati_table.removeRow(row)
        else:
            napaka = result.get("errors") or result.get("error") or "Rezultata ni bilo mogoče izbrisati."
            QMessageBox.warning(self, "Napaka", str(napaka))

    def load_nepopolni(self):
        data = self.api.get_nepopolni()

        if not isinstance(data, list):
            QMessageBox.warning(self, "Napaka", "Nepopolnih rezultatov ni bilo mogoče naložiti.")
            return

        self.validacija_table.setRowCount(len(data))

        for row, item in enumerate(data):
            self.validacija_table.setItem(row, 0, QTableWidgetItem(str(item.get("id_rezultata", ""))))
            self.validacija_table.setItem(row, 1, QTableWidgetItem(str(item.get("tk_tekmovanje", ""))))
            self.validacija_table.setItem(row, 2, QTableWidgetItem(""))
            self.validacija_table.setItem(row, 3, QTableWidgetItem(str(item.get("overallRank", ""))))
            self.validacija_table.setItem(row, 4, QTableWidgetItem(str(item.get("skupniCas", ""))))
            self.validacija_table.setItem(row, 5, QTableWidgetItem("Manjka skupni čas"))

        self.validacija_table.resizeColumnsToContents()

    def load_duplikati(self):
        data = self.api.get_duplikati()

        if not isinstance(data, list):
            QMessageBox.warning(self, "Napaka", "Duplikatov ni bilo mogoče naložiti.")
            return

        self.validacija_table.setRowCount(len(data))

        for row, item in enumerate(data):
            self.validacija_table.setItem(row, 0, QTableWidgetItem(str(item.get("tk_tekmovalec", ""))))
            self.validacija_table.setItem(row, 1, QTableWidgetItem(str(item.get("tk_tekmovanje", ""))))
            self.validacija_table.setItem(row, 2, QTableWidgetItem(str(item.get("cnt", ""))))
            self.validacija_table.setItem(row, 3, QTableWidgetItem(""))
            self.validacija_table.setItem(row, 4, QTableWidgetItem(""))
            self.validacija_table.setItem(row, 5, QTableWidgetItem("Možen podvojen rezultat"))

        self.validacija_table.resizeColumnsToContents()

    def init_primerjava_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        search_layout = QHBoxLayout()

        self.primerjava_search_input = QLineEdit()
        self.primerjava_search_input.setPlaceholderText("Vnesi ime tekmovalca")

        self.primerjava_search_btn = QPushButton(t(self.lang, "search"))
        self.primerjava_search_btn.clicked.connect(self.search_primerjava_tekmovalci)

        search_layout.addWidget(self.primerjava_search_input)
        search_layout.addWidget(self.primerjava_search_btn)

        self.primerjava_table = QTableWidget()
        self.primerjava_table.setColumnCount(4)
        self.primerjava_table.setHorizontalHeaderLabels([
            "ID", "Ime in priimek", "Starost", "Država"
        ])
        self.primerjava_table.setSelectionBehavior(QTableWidget.SelectRows)

        izbor_layout = QHBoxLayout()

        self.primerjava_first_label = QLabel(t(self.lang, "selected_first"))
        self.primerjava_first_input = QLineEdit()
        self.primerjava_first_input.setReadOnly(True)

        self.primerjava_second_label = QLabel(t(self.lang, "selected_second"))
        self.primerjava_second_input = QLineEdit()
        self.primerjava_second_input.setReadOnly(True)

        self.primerjava_select_first_btn = QPushButton(t(self.lang, "select_first"))
        self.primerjava_select_first_btn.clicked.connect(self.set_primerjava_first)

        self.primerjava_select_second_btn = QPushButton(t(self.lang, "select_second"))
        self.primerjava_select_second_btn.clicked.connect(self.set_primerjava_second)

        izbor_left = QVBoxLayout()
        izbor_left.addWidget(self.primerjava_first_label)
        izbor_left.addWidget(self.primerjava_first_input)
        izbor_left.addWidget(self.primerjava_select_first_btn)

        izbor_right = QVBoxLayout()
        izbor_right.addWidget(self.primerjava_second_label)
        izbor_right.addWidget(self.primerjava_second_input)
        izbor_right.addWidget(self.primerjava_select_second_btn)

        izbor_layout.addLayout(izbor_left)
        izbor_layout.addLayout(izbor_right)

        self.primerjava_compare_btn = QPushButton(t(self.lang, "compare"))
        self.primerjava_compare_btn.clicked.connect(self.compare_selected_tekmovalca)

        self.primerjava_result_table = QTableWidget()
        self.primerjava_result_table.setColumnCount(3)
        self.primerjava_result_table.setRowCount(2)
        self.primerjava_result_table.setHorizontalHeaderLabels([
            "Lastnost", "Tekmovalec 1", "Tekmovalec 2"
        ])
        self.primerjava_result_table.setVerticalHeaderLabels([
            "Nastopi", "Najboljši čas"
        ])
        self.primerjava_result_table.setItem(0, 0, QTableWidgetItem("Nastopi"))
        self.primerjava_result_table.setItem(1, 0, QTableWidgetItem("Najboljši čas"))

        layout.addLayout(search_layout)
        layout.addWidget(self.primerjava_table)
        layout.addLayout(izbor_layout)
        layout.addWidget(self.primerjava_compare_btn)
        layout.addWidget(self.primerjava_result_table)

        self.tab_primerjava.setLayout(layout)

    def search_primerjava_tekmovalci(self):
        ime = self.primerjava_search_input.text().strip()

        if not ime:
            QMessageBox.warning(self, "Napaka", "Vnesi ime tekmovalca.")
            return

        data = self.api.search_tekmovalci(ime)

        if not isinstance(data, list):
            QMessageBox.warning(self, "Napaka", "Tekmovalcev ni bilo mogoče naložiti.")
            return

        self.primerjava_data = data
        self.primerjava_table.setRowCount(len(data))

        for row, item in enumerate(data):
            self.primerjava_table.setItem(row, 0, QTableWidgetItem(str(item.get("id_tekmovalec", ""))))
            self.primerjava_table.setItem(row, 1, QTableWidgetItem(str(item.get("ime_priimek", ""))))
            self.primerjava_table.setItem(row, 2, QTableWidgetItem(str(item.get("starost", ""))))
            self.primerjava_table.setItem(row, 3, QTableWidgetItem(str(item.get("drzava", ""))))

        self.primerjava_table.resizeColumnsToContents()

    def _get_primerjava_selected_tekmovalec(self):
        row = self.primerjava_table.currentRow()

        if row < 0 or row >= len(self.primerjava_data):
            return None

        return self.primerjava_data[row]

    def set_primerjava_first(self):
        item = self._get_primerjava_selected_tekmovalec()

        if not item:
            QMessageBox.warning(self, "Napaka", "Najprej izberi tekmovalca v tabeli.")
            return

        self.primerjava_first_id = item.get("id_tekmovalec")
        self.primerjava_first_input.setText(f'{self.primerjava_first_id} - {item.get("ime_priimek", "")}')

    def set_primerjava_second(self):
        item = self._get_primerjava_selected_tekmovalec()

        if not item:
            QMessageBox.warning(self, "Napaka", "Najprej izberi tekmovalca v tabeli.")
            return

        self.primerjava_second_id = item.get("id_tekmovalec")
        self.primerjava_second_input.setText(f'{self.primerjava_second_id} - {item.get("ime_priimek", "")}')

    def _format_primerjava_value(self, value):
        if value in (None, ""):
            return "-"

        return str(value)

    def compare_selected_tekmovalca(self):
        if not self.primerjava_first_id or not self.primerjava_second_id:
            QMessageBox.warning(self, "Napaka", "Izberi oba tekmovalca za primerjavo.")
            return

        result = self.api.primerjaj_tekmovalca(self.primerjava_first_id, self.primerjava_second_id)

        if not isinstance(result, dict):
            QMessageBox.warning(self, "Napaka", "Primerjave ni bilo mogoče naložiti.")
            return

        t1 = result.get("tekmovalec1") or {}
        t2 = result.get("tekmovalec2") or {}

        self.primerjava_result_table.setItem(0, 1, QTableWidgetItem(self._format_primerjava_value(t1.get("nastopi"))))
        self.primerjava_result_table.setItem(0, 2, QTableWidgetItem(self._format_primerjava_value(t2.get("nastopi"))))
        self.primerjava_result_table.setItem(1, 1, QTableWidgetItem(self._format_primerjava_value(t1.get("najboljsi"))))
        self.primerjava_result_table.setItem(1, 2, QTableWidgetItem(self._format_primerjava_value(t2.get("najboljsi"))))

        self.primerjava_result_table.resizeColumnsToContents()

    def get_selected_tekmovanje_id(self):
        row = self.tekmovanja_table.currentRow()

        if row < 0:
            return None

        item = self.tekmovanja_table.item(row, 0)
        if not item:
            return None

        return item.text()

    def add_rezultat(self):
        tekmovanje_id = self.get_selected_tekmovanje_id()

        if not tekmovanje_id:
            QMessageBox.warning(self, "Napaka", "Najprej izberi tekmovanje.")
            return

        tekmovalec_row = self.tekmovalci_table.currentRow()
        if tekmovalec_row < 0:
            QMessageBox.warning(
                self,
                "Napaka",
                "Najprej na zavihku Tekmovalci poišči in izberi tekmovalca."
            )
            return

        tekmovalec_id = self.tekmovalci_table.item(tekmovalec_row, 0).text()

        form = RezultatForm(
            self,
            tekmovalec_id=tekmovalec_id,
            tekmovanje_id=tekmovanje_id
        )

        if form.exec_():
            form.saved_data["tk_admin"] = self.admin_id
            result = self.api.create_rezultat(form.saved_data)

            if result.get("success"):
                QMessageBox.information(self, "Uspeh", "Rezultat je bil dodan.")
                self.load_rezultati_tekmovanja(tekmovanje_id)
            else:
                napake = result.get("errors") or result.get("error") or "Rezultata ni bilo mogoče dodati."
                QMessageBox.warning(self, "Napaka", str(napake))

    def edit_selected_rezultat(self):
        row = self.rezultati_table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Napaka", "Najprej izberi rezultat.")
            return

        rezultat_id = self.rezultati_table.item(row, 0).text()

        if row >= len(self.rezultati_data):
            QMessageBox.warning(self, "Napaka", "Podatkov rezultata ni mogoče prebrati.")
            return

        rezultat = self.rezultati_data[row]

        form = RezultatForm(self, rezultat=rezultat)

        if form.exec_():
            form.saved_data["tk_admin"] = self.admin_id
            result = self.api.update_rezultat(rezultat_id, form.saved_data)

            if result.get("success"):
                QMessageBox.information(self, "Uspeh", "Rezultat je bil posodobljen.")

                tekmovanje_id = self.get_selected_tekmovanje_id()
                if tekmovanje_id:
                    self.load_rezultati_tekmovanja(tekmovanje_id)
            else:
                napake = result.get("errors") or result.get("error") or "Rezultata ni bilo mogoče posodobiti."
                QMessageBox.warning(self, "Napaka", str(napake))

    def export_rezultati_csv(self):
        if not self.rezultati_data:
            QMessageBox.warning(self, "Napaka", "Ni rezultatov za izvoz.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Shrani CSV",
            "rezultati.csv",
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file, delimiter=";")

                writer.writerow([
                    "ID rezultata",
                    "Tekmovalec",
                    "Overall Rank",
                    "Gender Rank",
                    "Division Rank",
                    "Bib",
                    "Divizija",
                    "Točke",
                    "Plavanje",
                    "T1",
                    "Kolesarjenje",
                    "T2",
                    "Tek",
                    "Skupni čas",
                    "Tekmovalec ID",
                    "Tekmovanje ID"
                ])

                for item in self.rezultati_data:
                    writer.writerow([
                        item.get("id_rezultata", ""),
                        item.get("ime_priimek", ""),
                        item.get("overallRank", ""),
                        item.get("genderRank", ""),
                        item.get("divRank", ""),
                        item.get("bib", ""),
                        item.get("divizija", ""),
                        item.get("tocke", ""),
                        item.get("plavanje", ""),
                        item.get("t1", ""),
                        item.get("kolesarjenje", ""),
                        item.get("t2", ""),
                        item.get("tek", ""),
                        item.get("skupniCas", ""),
                        item.get("tk_tekmovalec", ""),
                        item.get("tk_tekmovanje", "")
                    ])

            QMessageBox.information(self, "Uspeh", "CSV datoteka je bila uspešno izvožena.")

        except Exception as e:
            QMessageBox.warning(self, "Napaka", f"Napaka pri izvozu CSV: {e}")

    def init_spremembe_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        button_layout = QHBoxLayout()

        self.refresh_spremembe_btn = QPushButton(t(self.lang, "refresh"))
        self.refresh_spremembe_btn.clicked.connect(self.load_spremembe)

        button_layout.addWidget(self.refresh_spremembe_btn)
        button_layout.addStretch()

        self.spremembe_table = QTableWidget()
        self.spremembe_table.setColumnCount(8)
        self.spremembe_table.setHorizontalHeaderLabels([
            "ID",
            "Tabela",
            "Operacija",
            "Čas",
            "Opis",
            "Admin ID",
            "Uporabniško ime",
            "Ime admina"
        ])

        layout.addLayout(button_layout)
        layout.addWidget(self.spremembe_table)

        self.tab_spremembe.setLayout(layout)

    def load_spremembe(self):
        data = self.api.get_spremembe()

        if not isinstance(data, list):
            QMessageBox.warning(self, "Napaka", "Sprememb ni bilo mogoče naložiti.")
            return

        self.spremembe_table.setRowCount(len(data))

        for row, item in enumerate(data):
            ime_admina = f"{item.get('ime') or ''} {item.get('priimek') or ''}".strip()

            self.spremembe_table.setItem(row, 0, QTableWidgetItem(str(item.get("id_spremembe", ""))))
            self.spremembe_table.setItem(row, 1, QTableWidgetItem(str(item.get("tabela", ""))))
            self.spremembe_table.setItem(row, 2, QTableWidgetItem(str(item.get("operacija", ""))))
            self.spremembe_table.setItem(row, 3, QTableWidgetItem(str(item.get("cas", ""))))
            self.spremembe_table.setItem(row, 4, QTableWidgetItem(str(item.get("opis", ""))))
            self.spremembe_table.setItem(row, 5, QTableWidgetItem(str(item.get("tk_admin", ""))))
            self.spremembe_table.setItem(row, 6, QTableWidgetItem(str(item.get("uporIme", ""))))
            self.spremembe_table.setItem(row, 7, QTableWidgetItem(ime_admina))

        self.spremembe_table.resizeColumnsToContents()