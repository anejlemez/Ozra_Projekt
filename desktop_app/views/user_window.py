from PyQt5.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget
)

from translations import t
from ui_style import apply_base_style


class UserWindow(QMainWindow):
    def __init__(self, api, lang="sl"):
        super().__init__()

        self.api = api
        self.lang = lang

        self.tekmovanja_data = []
        self.tekmovanja_map = {}
        self.tekmovalci_data = []
        self.tekmovalci_filtered_data = []
        self.primerjava_data = []
        self.primerjava_first_id = None
        self.primerjava_second_id = None

        self.setWindowTitle(t(self.lang, "public_view"))
        self.setGeometry(180, 90, 1350, 820)
        apply_base_style(self)

        self.init_ui()
        self.load_tekmovanja()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(10)

        top_layout = QHBoxLayout()

        self.title_label = QLabel(t(self.lang, "public_view"))
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

        self.tabs.addTab(self.tab_tekmovanja, t(self.lang, "competitions"))
        self.tabs.addTab(self.tab_tekmovalci, t(self.lang, "competitors"))
        self.tabs.addTab(self.tab_primerjava, t(self.lang, "comparison"))

        self.init_tekmovanja_tab()
        self.init_tekmovalci_tab()
        self.init_primerjava_tab()

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.tabs)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def change_language(self):
        self.lang = self.language_select.currentData()

        self.setWindowTitle(t(self.lang, "public_view"))
        self.title_label.setText(t(self.lang, "public_view"))
        self.language_label.setText(t(self.lang, "language"))

        self.tabs.setTabText(0, t(self.lang, "competitions"))
        self.tabs.setTabText(1, t(self.lang, "competitors"))
        self.tabs.setTabText(2, t(self.lang, "comparison"))

        self.refresh_tekmovanja_btn.setText(t(self.lang, "refresh"))
        self.tekmovanja_details_label.setText(t(self.lang, "competition_details"))
        self.tekmovanja_results_label.setText(t(self.lang, "competition_results"))

        self.search_btn.setText(t(self.lang, "search"))
        self.age_group_label.setText(t(self.lang, "age_group"))
        self.select_competitor_btn.setText(t(self.lang, "statistics"))
        self.selected_competitor_label.setText(t(self.lang, "selected_competitor"))
        self.total_starts_label.setText(t(self.lang, "starts"))
        self.statistics_title_label.setText(t(self.lang, "statistics"))
        self.best_time_label.setText(t(self.lang, "best_time"))
        self.best_rank_label.setText(t(self.lang, "best_rank"))
        self.best_competition_label.setText(t(self.lang, "best_competition"))
        self.discipline_averages_label.setText(t(self.lang, "discipline_averages"))
        self.starts_label.setText(t(self.lang, "starts"))

        self.primerjava_search_btn.setText(t(self.lang, "search"))
        self.primerjava_select_first_btn.setText(t(self.lang, "select_first"))
        self.primerjava_select_second_btn.setText(t(self.lang, "select_second"))
        self.primerjava_compare_btn.setText(t(self.lang, "compare_selected"))

        self._reload_age_group_labels()

    def _reload_age_group_labels(self):
        current_value = self.age_group_select.currentData()
        self.age_group_select.blockSignals(True)
        self.age_group_select.clear()

        options = [
            (t(self.lang, "all"), "all"),
            ("0-17", "0-17"),
            ("18-24", "18-24"),
            ("25-29", "25-29"),
            ("30-34", "30-34"),
            ("35-39", "35-39"),
            ("40-44", "40-44"),
            ("45-49", "45-49"),
            ("50+", "50+")
        ]

        for label, value in options:
            self.age_group_select.addItem(label, value)

        index = self.age_group_select.findData(current_value)
        self.age_group_select.setCurrentIndex(index if index >= 0 else 0)
        self.age_group_select.blockSignals(False)

    def init_tekmovanja_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        button_layout = QHBoxLayout()

        self.refresh_tekmovanja_btn = QPushButton(t(self.lang, "refresh"))
        self.refresh_tekmovanja_btn.clicked.connect(self.load_tekmovanja)

        button_layout.addWidget(self.refresh_tekmovanja_btn)
        button_layout.addStretch()

        self.tekmovanja_details_label = QLabel(t(self.lang, "competition_details"))
        self.tekmovanja_details_value = QLabel("-")
        self.tekmovanja_results_label = QLabel(t(self.lang, "competition_results"))

        self.tekmovanja_table = QTableWidget()
        self.tekmovanja_table.setColumnCount(5)
        self.tekmovanja_table.setHorizontalHeaderLabels([
            "ID", "Naziv", "Leto", "Tip", "Lokacija"
        ])
        self.tekmovanja_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.tekmovanja_table.cellClicked.connect(self.on_tekmovanje_selected)

        self.rezultati_table = QTableWidget()
        self.rezultati_table.setColumnCount(11)
        self.rezultati_table.setHorizontalHeaderLabels([
            "Tekmovalec", "Overall", "Gender", "Div", "Bib",
            "Divizija", "Plavanje", "T1", "Kolesarjenje", "T2", "Skupni čas"
        ])
        self.rezultati_table.setSelectionBehavior(QTableWidget.SelectRows)

        layout.addLayout(button_layout)
        layout.addWidget(self.tekmovanja_details_label)
        layout.addWidget(self.tekmovanja_details_value)
        layout.addWidget(self.tekmovanja_results_label)
        layout.addWidget(self.tekmovanja_table)
        layout.addWidget(self.rezultati_table)

        self.tab_tekmovanja.setLayout(layout)

    def init_tekmovalci_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Vnesi ime tekmovalca")

        self.age_group_label = QLabel(t(self.lang, "age_group"))
        self.age_group_select = QComboBox()
        self.age_group_select.currentIndexChanged.connect(self.apply_tekmovalci_filter)
        self._reload_age_group_labels()

        self.search_btn = QPushButton(t(self.lang, "search"))
        self.search_btn.clicked.connect(self.search_tekmovalci)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.age_group_label)
        search_layout.addWidget(self.age_group_select)
        search_layout.addWidget(self.search_btn)

        self.tekmovalci_table = QTableWidget()
        self.tekmovalci_table.setColumnCount(4)
        self.tekmovalci_table.setHorizontalHeaderLabels([
            "ID", "Ime in priimek", "Starost", "Država"
        ])
        self.tekmovalci_table.setSelectionBehavior(QTableWidget.SelectRows)

        self.select_competitor_btn = QPushButton(t(self.lang, "statistics"))
        self.select_competitor_btn.clicked.connect(self.load_selected_tekmovalec_statistics)

        self.selected_competitor_label = QLabel(t(self.lang, "selected_competitor"))
        self.selected_competitor_value = QLabel("-")

        self.statistics_title_label = QLabel(t(self.lang, "statistics"))
        self.total_starts_label = QLabel(t(self.lang, "starts"))
        self.total_starts_value = QLabel("-")
        self.best_time_label = QLabel(t(self.lang, "best_time"))
        self.best_time_value = QLabel("-")
        self.best_rank_label = QLabel(t(self.lang, "best_rank"))
        self.best_rank_value = QLabel("-")
        self.best_competition_label = QLabel(t(self.lang, "best_competition"))
        self.best_competition_value = QLabel("-")

        self.discipline_averages_label = QLabel(t(self.lang, "discipline_averages"))
        self.discipline_averages_table = QTableWidget()
        self.discipline_averages_table.setColumnCount(2)
        self.discipline_averages_table.setHorizontalHeaderLabels(["Disciplina", "Povprečje"])

        self.starts_label = QLabel(t(self.lang, "starts"))
        self.starts_table = QTableWidget()
        self.starts_table.setColumnCount(6)
        self.starts_table.setHorizontalHeaderLabels([
            "Tekmovanje", "Overall", "Gender", "Div", "Skupni čas", "Tekmovanje ID"
        ])

        layout.addLayout(search_layout)
        layout.addWidget(self.tekmovalci_table)
        layout.addWidget(self.select_competitor_btn)
        layout.addWidget(self.selected_competitor_label)
        layout.addWidget(self.selected_competitor_value)
        layout.addWidget(self.statistics_title_label)
        layout.addWidget(self.total_starts_label)
        layout.addWidget(self.total_starts_value)
        layout.addWidget(self.best_time_label)
        layout.addWidget(self.best_time_value)
        layout.addWidget(self.best_rank_label)
        layout.addWidget(self.best_rank_value)
        layout.addWidget(self.best_competition_label)
        layout.addWidget(self.best_competition_value)
        layout.addWidget(self.discipline_averages_label)
        layout.addWidget(self.discipline_averages_table)
        layout.addWidget(self.starts_label)
        layout.addWidget(self.starts_table)

        self.tab_tekmovalci.setLayout(layout)

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

        selection_layout = QHBoxLayout()

        self.primerjava_first_label = QLabel(t(self.lang, "selected_first"))
        self.primerjava_first_value = QLabel("-")
        self.primerjava_second_label = QLabel(t(self.lang, "selected_second"))
        self.primerjava_second_value = QLabel("-")

        self.primerjava_select_first_btn = QPushButton(t(self.lang, "select_first"))
        self.primerjava_select_first_btn.clicked.connect(self.set_primerjava_first)

        self.primerjava_select_second_btn = QPushButton(t(self.lang, "select_second"))
        self.primerjava_select_second_btn.clicked.connect(self.set_primerjava_second)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.primerjava_first_label)
        left_layout.addWidget(self.primerjava_first_value)
        left_layout.addWidget(self.primerjava_select_first_btn)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.primerjava_second_label)
        right_layout.addWidget(self.primerjava_second_value)
        right_layout.addWidget(self.primerjava_select_second_btn)

        selection_layout.addLayout(left_layout)
        selection_layout.addLayout(right_layout)

        self.primerjava_compare_btn = QPushButton(t(self.lang, "compare_selected"))
        self.primerjava_compare_btn.clicked.connect(self.compare_selected_tekmovalca)

        self.primerjava_result_table = QTableWidget()
        self.primerjava_result_table.setColumnCount(3)
        self.primerjava_result_table.setRowCount(2)
        self.primerjava_result_table.setHorizontalHeaderLabels([
            "Metric", "Tekmovalec 1", "Tekmovalec 2"
        ])
        self.primerjava_result_table.setItem(0, 0, QTableWidgetItem("Nastopi"))
        self.primerjava_result_table.setItem(1, 0, QTableWidgetItem("Najboljši čas"))

        layout.addLayout(search_layout)
        layout.addWidget(self.primerjava_table)
        layout.addLayout(selection_layout)
        layout.addWidget(self.primerjava_compare_btn)
        layout.addWidget(self.primerjava_result_table)

        self.tab_primerjava.setLayout(layout)

    def load_tekmovanja(self):
        data = self.api.get_tekmovanja()

        if not isinstance(data, list):
            QMessageBox.warning(self, "Napaka", "Tekmovanj ni bilo mogoče naložiti.")
            return

        self.tekmovanja_data = data
        self.tekmovanja_map = {}
        self.tekmovanja_table.setRowCount(len(data))

        for row, item in enumerate(data):
            tekmovanje_id = item.get("id_tekmovanja", "")
            self.tekmovanja_map[tekmovanje_id] = item
            self.tekmovanja_table.setItem(row, 0, QTableWidgetItem(str(tekmovanje_id)))
            self.tekmovanja_table.setItem(row, 1, QTableWidgetItem(str(item.get("naziv", ""))))
            self.tekmovanja_table.setItem(row, 2, QTableWidgetItem(str(item.get("leto", ""))))
            self.tekmovanja_table.setItem(row, 3, QTableWidgetItem(str(item.get("tip_tekmovanja", ""))))
            self.tekmovanja_table.setItem(row, 4, QTableWidgetItem(str(item.get("lokacija", ""))))

        self.tekmovanja_table.resizeColumnsToContents()

    def on_tekmovanje_selected(self, row, column):
        if row < 0 or row >= len(self.tekmovanja_data):
            return

        tekmovanje = self.tekmovanja_data[row]
        tekmovanje_id = tekmovanje.get("id_tekmovanja")

        naziv = tekmovanje.get("naziv", "")
        leto = tekmovanje.get("leto", "")
        tip = tekmovanje.get("tip_tekmovanja", "")
        lokacija = tekmovanje.get("lokacija", "")
        self.tekmovanja_details_value.setText(f"{naziv} | {leto} | {tip} | {lokacija}")

        if tekmovanje_id:
            self.load_rezultati_tekmovanja(tekmovanje_id)

    def load_rezultati_tekmovanja(self, tekmovanje_id):
        data = self.api.get_rezultati_tekmovanja(tekmovanje_id)

        if not isinstance(data, list):
            QMessageBox.warning(self, "Napaka", "Rezultatov ni bilo mogoče naložiti.")
            return

        self.rezultati_table.setRowCount(len(data))

        for row, item in enumerate(data):
            self.rezultati_table.setItem(row, 0, QTableWidgetItem(str(item.get("ime_priimek", ""))))
            self.rezultati_table.setItem(row, 1, QTableWidgetItem(str(item.get("overallRank", ""))))
            self.rezultati_table.setItem(row, 2, QTableWidgetItem(str(item.get("genderRank", ""))))
            self.rezultati_table.setItem(row, 3, QTableWidgetItem(str(item.get("divRank", ""))))
            self.rezultati_table.setItem(row, 4, QTableWidgetItem(str(item.get("bib", ""))))
            self.rezultati_table.setItem(row, 5, QTableWidgetItem(str(item.get("divizija", ""))))
            self.rezultati_table.setItem(row, 6, QTableWidgetItem(str(item.get("plavanje", ""))))
            self.rezultati_table.setItem(row, 7, QTableWidgetItem(str(item.get("t1", ""))))
            self.rezultati_table.setItem(row, 8, QTableWidgetItem(str(item.get("kolesarjenje", ""))))
            self.rezultati_table.setItem(row, 9, QTableWidgetItem(str(item.get("t2", ""))))
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
        self.apply_tekmovalci_filter()

    def apply_tekmovalci_filter(self):
        group = self.age_group_select.currentData()

        if group == "all":
            filtered = list(self.tekmovalci_data)
        else:
            filtered = [item for item in self.tekmovalci_data if self._age_matches_group(item.get("starost"), group)]

        self.tekmovalci_filtered_data = filtered
        self.tekmovalci_table.setRowCount(len(filtered))

        for row, item in enumerate(filtered):
            self.tekmovalci_table.setItem(row, 0, QTableWidgetItem(str(item.get("id_tekmovalec", ""))))
            self.tekmovalci_table.setItem(row, 1, QTableWidgetItem(str(item.get("ime_priimek", ""))))
            self.tekmovalci_table.setItem(row, 2, QTableWidgetItem(str(item.get("starost", ""))))
            self.tekmovalci_table.setItem(row, 3, QTableWidgetItem(str(item.get("drzava", ""))))

        self.tekmovalci_table.resizeColumnsToContents()

    def _age_matches_group(self, age_value, group):
        age = self._safe_int(age_value)

        if age is None:
            return False

        if group == "0-17":
            return 0 <= age <= 17
        if group == "18-24":
            return 18 <= age <= 24
        if group == "25-29":
            return 25 <= age <= 29
        if group == "30-34":
            return 30 <= age <= 34
        if group == "35-39":
            return 35 <= age <= 39
        if group == "40-44":
            return 40 <= age <= 44
        if group == "45-49":
            return 45 <= age <= 49
        if group == "50+":
            return age >= 50

        return True

    def load_selected_tekmovalec_statistics(self):
        row = self.tekmovalci_table.currentRow()

        if row < 0 or row >= len(self.tekmovalci_filtered_data):
            QMessageBox.warning(self, "Napaka", "Najprej izberi tekmovalca.")
            return

        tekmovalec = self.tekmovalci_filtered_data[row]
        self.load_tekmovalec_statistics(tekmovalec)

    def load_tekmovalec_statistics(self, tekmovalec):
        tekmovalec_id = tekmovalec.get("id_tekmovalec")
        data = self.api.get_nastopi_tekmovalca(tekmovalec_id)

        if not isinstance(data, list):
            QMessageBox.warning(self, "Napaka", "Statistike ni bilo mogoče naložiti.")
            return

        self.selected_competitor_value.setText(
            f'{tekmovalec.get("ime_priimek", "")} | {tekmovalec.get("starost", "")} | {tekmovalec.get("drzava", "")}')

        total_starts = len(data)
        best_result = self._find_best_result(data)
        best_time = best_result.get("skupniCas") if best_result else None
        best_rank = self._find_best_rank(data)
        best_competition = self._competition_name(best_result.get("tk_tekmovanje")) if best_result else "-"

        self.total_starts_value.setText(str(total_starts))
        self.best_time_value.setText(self._format_value(best_time))
        self.best_rank_value.setText(self._format_value(best_rank))
        self.best_competition_value.setText(self._format_value(best_competition))

        averages = self._calculate_averages(data)
        disciplines = [
            ("plavanje", "Plavanje"),
            ("t1", "T1"),
            ("kolesarjenje", "Kolesarjenje"),
            ("t2", "T2"),
            ("tek", "Tek"),
            ("skupniCas", "Skupni čas")
        ]

        self.discipline_averages_table.setRowCount(len(disciplines))
        for row, (field, label) in enumerate(disciplines):
            self.discipline_averages_table.setItem(row, 0, QTableWidgetItem(label))
            self.discipline_averages_table.setItem(row, 1, QTableWidgetItem(self._format_seconds(averages.get(field))))

        self.discipline_averages_table.resizeColumnsToContents()

        self.starts_table.setRowCount(len(data))
        for row, item in enumerate(data):
            competition_name = self._competition_name(item.get("tk_tekmovanje"))
            self.starts_table.setItem(row, 0, QTableWidgetItem(competition_name))
            self.starts_table.setItem(row, 1, QTableWidgetItem(str(item.get("overallRank", ""))))
            self.starts_table.setItem(row, 2, QTableWidgetItem(str(item.get("genderRank", ""))))
            self.starts_table.setItem(row, 3, QTableWidgetItem(str(item.get("divRank", ""))))
            self.starts_table.setItem(row, 4, QTableWidgetItem(str(item.get("skupniCas", ""))))
            self.starts_table.setItem(row, 5, QTableWidgetItem(str(item.get("tk_tekmovanje", ""))))

        self.starts_table.resizeColumnsToContents()

    def _find_best_result(self, data):
        best_item = None
        best_time = None

        for item in data:
            current_time = self._parse_time(item.get("skupniCas"))
            if current_time is None:
                continue

            if best_time is None or current_time < best_time:
                best_time = current_time
                best_item = item

        return best_item

    def _find_best_rank(self, data):
        best_rank = None
        for item in data:
            rank = self._safe_int(item.get("overallRank"))
            if rank is None:
                continue
            if best_rank is None or rank < best_rank:
                best_rank = rank
        return best_rank

    def _calculate_averages(self, data):
        fields = ["plavanje", "t1", "kolesarjenje", "t2", "tek", "skupniCas"]
        totals = {field: [] for field in fields}

        for item in data:
            for field in fields:
                seconds = self._parse_time(item.get(field))
                if seconds is not None:
                    totals[field].append(seconds)

        averages = {}
        for field in fields:
            values = totals[field]
            averages[field] = sum(values) / len(values) if values else None

        return averages

    def _competition_name(self, competition_id):
        if competition_id in self.tekmovanja_map:
            item = self.tekmovanja_map[competition_id]
            naziv = item.get("naziv", "")
            leto = item.get("leto", "")
            return f"{naziv} ({leto})".strip()

        return self._format_value(competition_id)

    def _format_value(self, value):
        if value in (None, ""):
            return "-"

        return str(value)

    def _safe_int(self, value):
        if value in (None, ""):
            return None

        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def _parse_time(self, value):
        if value in (None, ""):
            return None

        if isinstance(value, (int, float)):
            return float(value)

        text = str(value).strip()
        if not text or text == "-":
            return None

        parts = text.split(":")

        try:
            numbers = [float(part.replace(",", ".")) for part in parts]
        except ValueError:
            return None

        if len(numbers) == 3:
            hours, minutes, seconds = numbers
            return hours * 3600 + minutes * 60 + seconds

        if len(numbers) == 2:
            minutes, seconds = numbers
            return minutes * 60 + seconds

        if len(numbers) == 1:
            return numbers[0]

        return None

    def _format_seconds(self, seconds):
        if seconds in (None, ""):
            return "-"

        total_seconds = int(round(float(seconds)))
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        remaining_seconds = total_seconds % 60

        return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"

    def set_primerjava_first(self):
        item = self._get_selected_primerjava_tekmovalec()

        if not item:
            QMessageBox.warning(self, "Napaka", "Najprej izberi tekmovalca v tabeli.")
            return

        self.primerjava_first_id = item.get("id_tekmovalec")
        self.primerjava_first_value.setText(f'{self.primerjava_first_id} - {item.get("ime_priimek", "")}')

    def set_primerjava_second(self):
        item = self._get_selected_primerjava_tekmovalec()

        if not item:
            QMessageBox.warning(self, "Napaka", "Najprej izberi tekmovalca v tabeli.")
            return

        self.primerjava_second_id = item.get("id_tekmovalec")
        self.primerjava_second_value.setText(f'{self.primerjava_second_id} - {item.get("ime_priimek", "")}')

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

    def _get_selected_primerjava_tekmovalec(self):
        row = self.primerjava_table.currentRow()

        if row < 0 or row >= len(self.primerjava_data):
            return None

        return self.primerjava_data[row]

    def compare_selected_tekmovalca(self):
        if not self.primerjava_first_id or not self.primerjava_second_id:
            QMessageBox.warning(self, "Napaka", "Izberi oba tekmovalca za primerjavo.")
            return

        result = self.api.primerjaj_tekmovalca(self.primerjava_first_id, self.primerjava_second_id)

        if not isinstance(result, dict):
            QMessageBox.warning(self, "Napaka", "Primerjave ni bilo mogoče naložiti.")
            return

        tekmovalec1 = result.get("tekmovalec1") or {}
        tekmovalec2 = result.get("tekmovalec2") or {}

        self.primerjava_result_table.setItem(0, 1, QTableWidgetItem(self._format_value(tekmovalec1.get("nastopi"))))
        self.primerjava_result_table.setItem(0, 2, QTableWidgetItem(self._format_value(tekmovalec2.get("nastopi"))))
        self.primerjava_result_table.setItem(1, 1, QTableWidgetItem(self._format_seconds(self._parse_time(tekmovalec1.get("najboljsi")))))
        self.primerjava_result_table.setItem(1, 2, QTableWidgetItem(self._format_seconds(self._parse_time(tekmovalec2.get("najboljsi")))))

        self.primerjava_result_table.resizeColumnsToContents()
