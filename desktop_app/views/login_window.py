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
from views.user_window import UserWindow
from ui_style import apply_base_style


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.api = ApiClient()
        self.lang = "sl"
        self.admin_window = None
        self.user_window = None

        self.setWindowTitle(t(self.lang, "login"))
        self.setFixedSize(350, 310)
        apply_base_style(self)

        self.title_label = QLabel(t(self.lang, "app_title"))
        self.title_label.setObjectName("SectionTitle")
        self.title_label.setWordWrap(True)

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

        self.user_button = QPushButton(t(self.lang, "open_public_view"))
        self.user_button.clicked.connect(self.open_user_view)

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)
        layout.addWidget(self.title_label)
        layout.addWidget(self.language_select)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.user_button)

        self.setLayout(layout)

    def change_language(self):
        self.lang = self.language_select.currentData()
        self.setWindowTitle(t(self.lang, "login"))
        self.title_label.setText(t(self.lang, "app_title"))
        self.username_input.setPlaceholderText(t(self.lang, "username"))
        self.password_input.setPlaceholderText(t(self.lang, "password"))
        self.login_button.setText(t(self.lang, "login_button"))
        self.user_button.setText(t(self.lang, "open_public_view"))

    def open_user_view(self):
        self.user_window = UserWindow(api=self.api, lang=self.lang)
        self.user_window.show()
        self.user_window.raise_()
        self.user_window.activateWindow()

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