import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt

class FileEditorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("File Size Editor")
        self.setFixedSize(600, 600)
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Label for selected file
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: white; font-size: 14px;")
        self.file_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.file_label)

        # Upload button
        upload_btn = QPushButton("Upload File")
        upload_btn.setStyleSheet("""
            background-color: grey;
            color: black;
            padding: 10px;
            font-size: 14px;
        """)
        upload_btn.clicked.connect(self.select_file)
        layout.addWidget(upload_btn)

        # Input for target size
        self.size_input = QLineEdit()
        self.size_input.setPlaceholderText("Enter target size in KB")
        self.size_input.setStyleSheet("""
            background-color: rgba(128, 128, 128, 0.2);
            color: white;
            border: 1px solid grey;
            padding: 10px;
            font-size: 14px;
        """)
        layout.addWidget(self.size_input)

        # Shrink button
        shrink_btn = QPushButton("Shrink File")
        shrink_btn.setStyleSheet("""
            background-color: #444;
            color: white;
            padding: 10px;
            font-size: 14px;
        """)
        shrink_btn.clicked.connect(self.shrink_file)
        layout.addWidget(shrink_btn)

        # Increase button
        increase_btn = QPushButton("Increase File")
        increase_btn.setStyleSheet("""
            background-color: #888;
            color: black;
            padding: 10px;
            font-size: 14px;
        """)
        increase_btn.clicked.connect(self.increase_file)
        layout.addWidget(increase_btn)

        self.setLayout(layout)
        self.file_path = None

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if path:
            self.file_path = path
            self.file_label.setText(f"Selected: {os.path.basename(path)}")

    def get_target_size(self):
        try:
            target_kb = int(self.size_input.text())
            return target_kb * 1024
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")
            return None

    def shrink_file(self):
        if not self.file_path:
            QMessageBox.warning(self, "No File", "Please select a file.")
            return

        target_size = self.get_target_size()
        if target_size is None:
            return

        current_size = os.path.getsize(self.file_path)
        if current_size <= target_size:
            QMessageBox.information(self, "Already Small", "File is already smaller than target size.")
            return

        with open(self.file_path, "rb") as f:
            data = f.read(target_size)

        with open(self.file_path, "wb") as f:
            f.write(data)

        QMessageBox.information(self, "Success", f"File shrunk to {target_size // 1024} KB.")

    def increase_file(self):
        if not self.file_path:
            QMessageBox.warning(self, "No File", "Please select a file.")
            return

        target_size = self.get_target_size()
        if target_size is None:
            return

        current_size = os.path.getsize(self.file_path)
        if current_size >= target_size:
            QMessageBox.information(self, "Already Big", "File is already larger than target size.")
            return

        padding_size = target_size - current_size
        with open(self.file_path, "ab") as f:
            f.write(b"\x00" * padding_size)

        QMessageBox.information(self, "Success", f"File increased to {target_size // 1024} KB.")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = FileEditorGUI()
    window.show()
    sys.exit(app.exec_())
