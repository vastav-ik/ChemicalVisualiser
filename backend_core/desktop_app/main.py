import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QVBoxLayout, QWidget, QFileDialog, QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Analyzer (Desktop)")
        self.setGeometry(100, 100, 900, 700)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("⚗️ Chemical Equipment Visualizer")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.btn = QPushButton("Upload CSV & Analyze")
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff; color: white; padding: 10px; font-size: 16px; border-radius: 5px;
            }
            QPushButton:hover { background-color: #0056b3; }
        """)
        self.btn.clicked.connect(self.upload_file)
        layout.addWidget(self.btn)

        self.stats_label = QLabel("Ready to analyze...")
        self.stats_label.setStyleSheet("font-size: 14px; background: #f0f0f0; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.stats_label)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.canvas)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def upload_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)')
        
        if fname:
            self.stats_label.setText("Uploading and analyzing... Please wait.")
            
            try:
                url = 'http://127.0.0.1:8000/api/upload/'
                files = {'file': open(fname, 'rb')}
                
                response = requests.post(url, files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    self.update_ui(data)
                else:
                    self.stats_label.setText(f"Error: Server returned {response.status_code}")
                    QMessageBox.warning(self, "Error", "Upload failed. Check terminal for details.")

            except requests.exceptions.ConnectionError:
                self.stats_label.setText("Error: Could not connect to Django.")
                QMessageBox.critical(self, "Connection Error", "Is the Django server running on port 8000?")
            except Exception as e:
                self.stats_label.setText(f"Error: {str(e)}")

    def update_ui(self, data):
        stats_text = (f"<b>Results:</b><br>"
                      f"Total Equipment: {data.get('total_count', 0)}<br>"
                      f"Avg Pressure: {data.get('avg_pressure', 0)} Pa<br>"
                      f"Avg Temperature: {data.get('avg_temp', 0)} °C")
        self.stats_label.setText(stats_text)
        
        self.canvas.axes.clear()
        
        type_counts = data.get('type_counts', {})
        types = list(type_counts.keys())
        counts = list(type_counts.values())

        bars = self.canvas.axes.bar(types, counts, color=['#4bc0c0', '#36a2eb', '#ff6384'])
        
        self.canvas.axes.set_title("Equipment Type Distribution")
        self.canvas.axes.set_ylabel("Count")
        self.canvas.axes.grid(axis='y', linestyle='--', alpha=0.7)
        
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())