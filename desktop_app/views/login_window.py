from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QComboBox
)

from api_client import ApiClient
from translations import t
from views.admin_window import AdminWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.api = ApiClient()
        self.lang = "sl"
        self.admin_window = None

        self.setWindowTitle(t(self.lang, "login"))
        self.setFixedSize(350, 260)

        self.title_label = QLabel(t(self.lang, "app_title"))

        self.language_select = QComboBox()
        self.language_select.addItem("Slovenščina", "sl")
        self.language_select.addItem("English", "en")
        self.language_select.currentIndexChanged.connect(self.change_language)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(t(self.lang, "username"))

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(t(self.lang, "password"))
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton(t(self.lang, "login_button"))
        self.login_button.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.language_select)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def change_language(self):
        self.lang = self.language_select.currentData()
        self.setWindowTitle(t(self.lang, "login"))
        self.title_label.setText(t(self.lang, "app_title"))
        self.username_input.setPlaceholderText(t(self.lang, "username"))
        self.password_input.setPlaceholderText(t(self.lang, "password"))
        self.login_button.setText(t(self.lang, "login_button"))

    def login(self):
        upor_ime = self.username_input.text().strip()
        geslo = self.password_input.text().strip()

        if not upor_ime or not geslo:
            QMessageBox.warning(
                self,
                t(self.lang, "login"),
                t(self.lang, "login_error")
            )
            return

        result = self.api.login(upor_ime, geslo)

        if result.get("success"):
            self.admin_window = AdminWindow(
                api=self.api,
                lang=self.lang,
                admin=result.get("admin")
            )
            self.admin_window.show()
            self.close()