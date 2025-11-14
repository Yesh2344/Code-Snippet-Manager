import sys
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLineEdit, QPushButton, QListWidget, QTextEdit, QInputDialog,
                               QComboBox, QLabel, QSplitter, QMessageBox, QFileDialog)
from PySide6.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter, QIcon
from PySide6.QtCore import Qt, QRegularExpression, QSize
from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

class CodeSnippetManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Code Snippet Manager")
        self.setGeometry(100, 100, 1000, 700)
        self.snippets = {}
        self.load_snippets()

        self.setup_ui()

    def setup_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search snippets...")
        self.search_bar.textChanged.connect(self.filter_snippets)

        self.snippet_list = QListWidget()
        self.snippet_list.itemClicked.connect(self.show_snippet)

        add_button = QPushButton("Add Snippet")
        add_button.setIcon(QIcon.fromTheme("list-add"))
        add_button.clicked.connect(self.add_snippet)

        left_layout.addWidget(QLabel("Search:"))
        left_layout.addWidget(self.search_bar)
        left_layout.addWidget(QLabel("Snippets:"))
        left_layout.addWidget(self.snippet_list)
        left_layout.addWidget(add_button)
        left_panel.setLayout(left_layout)

        # Right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout()

        self.language_combo = QComboBox()
        self.language_combo.addItems(["Python", "JavaScript", "HTML", "CSS", "Java", "C++", "C#", "Ruby", "PHP", "Swift", "Go", "Rust", "TypeScript", "SQL", "Shell", "Markdown", "JSON", "YAML"])
        self.language_combo.currentTextChanged.connect(self.change_language)

        self.code_editor = QTextEdit()
        self.code_editor.setFont(QFont("Courier", 12))

        button_layout = QHBoxLayout()
        save_button = QPushButton("Save Changes")
        save_button.setIcon(QIcon.fromTheme("document-save"))
        save_button.clicked.connect(self.save_changes)
        delete_button = QPushButton("Delete Snippet")
# Added comment
        delete_button.setIcon(QIcon.fromTheme("edit-delete"))
        delete_button.clicked.connect(self.delete_snippet)
        export_button = QPushButton("Export Snippet")
        export_button.setIcon(QIcon.fromTheme("document-export"))
        export_button.clicked.connect(self.export_snippet)
        button_layout.addWidget(save_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(export_button)

        right_layout.addWidget(QLabel("Language:"))
        right_layout.addWidget(self.language_combo)
        right_layout.addWidget(QLabel("Code:"))
        right_layout.addWidget(self.code_editor)
        right_layout.addLayout(button_layout)
        right_panel.setLayout(right_layout)

        # Create a splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])

        main_layout.addWidget(splitter)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Set up menu bar
        self.setup_menu()

        self.update_snippet_list()

    def setup_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        import_action = file_menu.addAction("Import Snippets")
        import_action.triggered.connect(self.import_snippets)
        export_all_action = file_menu.addAction("Export All Snippets")
        export_all_action.triggered.connect(self.export_all_snippets)
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        help_menu = menu_bar.addMenu("Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)

    def load_snippets(self):
        try:
            with open("snippets.json", "r") as f:
                self.snippets = json.load(f)
        except FileNotFoundError:
            self.snippets = {}

    def save_snippets(self):
        with open("snippets.json", "w") as f:
            json.dump(self.snippets, f)

    def update_snippet_list(self):
        self.snippet_list.clear()
        self.snippet_list.addItems(sorted(self.snippets.keys()))

    def filter_snippets(self):
        search_text = self.search_bar.text().lower()
        self.snippet_list.clear()
        for name in sorted(self.snippets.keys()):
            if search_text in name.lower() or search_text in self.snippets[name]["code"].lower():
                self.snippet_list.addItem(name)

    def show_snippet(self, item):
        name = item.text()
        snippet = self.snippets[name]
        self.code_editor.setPlainText(snippet["code"])
        self.language_combo.setCurrentText(snippet["language"])
        self.highlight_syntax(snippet["language"])

    def add_snippet(self):
        name, ok = QInputDialog.getText(self, "Add Snippet", "Enter snippet name:")
        if ok and name:
            if name in self.snippets:
                QMessageBox.warning(self, "Warning", "A snippet with this name already exists.")
                return
            language = self.language_combo.currentText()
            self.snippets[name] = {"language": language, "code": ""}
            self.update_snippet_list()
            self.save_snippets()
            self.snippet_list.setCurrentRow(self.snippet_list.count() - 1)
            self.code_editor.setFocus()

    def save_changes(self):
        current_item = self.snippet_list.currentItem()
        if current_item:
            name = current_item.text()
            self.snippets[name]["code"] = self.code_editor.toPlainText()
            self.snippets[name]["language"] = self.language_combo.currentText()
            self.save_snippets()
            QMessageBox.information(self, "Success", "Snippet saved successfully.")
        else:
            QMessageBox.warning(self, "Warning", "No snippet selected.")

    def delete_snippet(self):
        current_item = self.snippet_list.currentItem()
        if current_item:
            name = current_item.text()
            reply = QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete the snippet '{name}'?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                del self.snippets[name]
                self.update_snippet_list()
                self.code_editor.clear()
                self.save_snippets()
        else:
            QMessageBox.warning(self, "Warning", "No snippet selected.")

    def highlight_syntax(self, language):
        try:
            lexer = get_lexer_by_name(language, stripall=True)
        except ClassNotFound:
            try:
                lexer = get_lexer_for_filename(f"dummy.{language}", stripall=True)
            except ClassNotFound:
                lexer = get_lexer_by_name("text", stripall=True)
        
        formatter = HtmlFormatter(style="monokai")
        highlighted_code = highlight(self.code_editor.toPlainText(), lexer, formatter)
        self.code_editor.setHtml(highlighted_code)

    def change_language(self, language):
        self.highlight_syntax(language)

    def export_snippet(self):
        current_item = self.snippet_list.currentItem()
        if current_item:
            name = current_item.text()
            snippet = self.snippets[name]
            file_name, _ = QFileDialog.getSaveFileName(self, "Export Snippet", f"{name}.{snippet['language'].lower()}", "All Files (*)")
            if file_name:
                with open(file_name, "w") as f:
                    f.write(snippet["code"])
                QMessageBox.information(self, "Success", f"Snippet exported to {file_name}")
        else:
            QMessageBox.warning(self, "Warning", "No snippet selected.")

    def import_snippets(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Snippets", "", "JSON Files (*.json)")
        if file_name:
            try:
                with open(file_name, "r") as f:
                    imported_snippets = json.load(f)
                self.snippets.update(imported_snippets)
                self.save_snippets()
                self.update_snippet_list()
                QMessageBox.information(self, "Success", f"Snippets imported from {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import snippets: {str(e)}")

    def export_all_snippets(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Export All Snippets", "all_snippets.json", "JSON Files (*.json)")
        if file_name:
            with open(file_name, "w") as f:
                json.dump(self.snippets, f, indent=2)
            QMessageBox.information(self, "Success", f"All snippets exported to {file_name}")

    def show_about(self):
        QMessageBox.about(self, "About Code Snippet Manager",
                          "Code Snippet Manager v1.0\n\n"
                          "A simple tool to manage and organize your code snippets.\n"
                          "Created with PySide6 and Pygments.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CodeSnippetManager()
# Added comment
    window.show()
    sys.exit(app.exec())

