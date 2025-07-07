import sys
import socket
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QColor, QPalette
from concurrent.futures import ThreadPoolExecutor

# Signal handler
class SignalEmitter(QObject):
    log_signal = pyqtSignal(str)

class PortScanner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Port Scanner")
        self.setGeometry(200, 100, 600, 500)
        self.setStyleSheet(self.dark_theme_stylesheet())

        self.signals = SignalEmitter()
        self.signals.log_signal.connect(self.log)
        self.executor = ThreadPoolExecutor(max_workers=100)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.ip_input = QLineEdit()
        self.setup_input(self.ip_input, "Enter Target IP or Domain")

        self.start_port_input = QLineEdit()
        self.setup_input(self.start_port_input, "Start Port")

        self.end_port_input = QLineEdit()
        self.setup_input(self.end_port_input, "End Port")

        port_layout = QHBoxLayout()
        port_layout.addWidget(self.start_port_input)
        port_layout.addWidget(self.end_port_input)

        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self.start_scan)
        self.scan_button.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.setup_output(self.output)

        layout.addWidget(QLabel("🎯 Target"))
        layout.addWidget(self.ip_input)
        layout.addWidget(QLabel("🔍 Port Range"))
        layout.addLayout(port_layout)
        layout.addWidget(self.scan_button)
        layout.addWidget(QLabel("📋 Scan Output"))
        layout.addWidget(self.output)

        self.setLayout(layout)

    def setup_input(self, widget, placeholder):
        widget.setPlaceholderText(placeholder)
        widget.setStyleSheet("""
            QLineEdit {
                background-color: rgba(200, 200, 200, 0.1);
                color: white;
                padding: 8px;
                border: 1px solid #555;
                border-radius: 8px;
                font-size: 14px;
            }
        """)

    def setup_output(self, widget):
        widget.setStyleSheet("""
            QTextEdit {
                background-color: rgba(200, 200, 200, 0.1);
                color: #0f0;
                padding: 8px;
                border: 1px solid #555;
                border-radius: 8px;
                font-family: Consolas, monospace;
                font-size: 13px;
            }
        """)

    def dark_theme_stylesheet(self):
        return """
            QWidget {
                background-color: #111;
                color: white;
                font-family: Segoe UI, sans-serif;
                font-size: 14px;
            }
            QLabel {
                color: #aaa;
                font-weight: bold;
            }
        """

    def log(self, message):
        self.output.append(message)

    def scan_port(self, host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                self.signals.log_signal.emit(f"[OPEN] Port {port} ({service})")
            sock.close()
        except Exception as e:
            self.signals.log_signal.emit(f"[!] Error on port {port}: {str(e)}")

    def start_scan(self):
        self.output.clear()
        target = self.ip_input.text()
        try:
            start_port = int(self.start_port_input.text())
            end_port = int(self.end_port_input.text())
        except ValueError:
            self.log("⚠️ Invalid port range. Use numbers only.")
            return

        self.log(f"\n🔎 Scanning {target} from port {start_port} to {end_port}...\n")

        for port in range(start_port, end_port + 1):
            self.executor.submit(self.scan_port, target, port)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scanner = PortScanner()
    scanner.show()
    sys.exit(app.exec_())
