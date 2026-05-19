BASE_STYLE = """
QWidget {
    font-size: 12px;
}

QMainWindow, QWidget {
    background: #f5f7fb;
}

QLabel#SectionTitle {
    font-size: 16px;
    font-weight: 600;
    color: #1f2937;
}

QPushButton {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 12px;
    min-height: 30px;
}

QPushButton:hover {
    background: #1d4ed8;
}

QPushButton:pressed {
    background: #1e40af;
}

QLineEdit, QComboBox, QTableWidget {
    background: white;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 6px;
}

QTableWidget {
    gridline-color: #e5e7eb;
    selection-background-color: #dbeafe;
    selection-color: #111827;
}

QHeaderView::section {
    background: #e5e7eb;
    color: #111827;
    border: none;
    padding: 6px;
    font-weight: 600;
}

QTabWidget::pane {
    border: 1px solid #d1d5db;
    top: -1px;
    background: white;
}

QTabBar::tab {
    background: #e5e7eb;
    padding: 8px 12px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}

QTabBar::tab:selected {
    background: white;
    font-weight: 600;
}
"""


def apply_base_style(widget):
    widget.setStyleSheet(BASE_STYLE)