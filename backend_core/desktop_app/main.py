import sys
import requests
import webbrowser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLabel, QMessageBox,
                             QTabWidget, QLineEdit, QDialog, QListWidget, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

API_BASE = "http://127.0.0.1:8000"

<<<<<<< HEAD
=======
# --- STYLESHEET ---
>>>>>>> 005a5118d8a91a8356cf366e6e2799e5ca399b87
STYLESHEET = """
QMainWindow {
    background-color: #2b2b2b;
}
QWidget {
    color: #e0e0e0;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}
QTabWidget::pane {
    border: 1px solid #444;
    background: #333;
    border-radius: 4px;
}
QTabBar::tab {
    background: #444;
    color: #bbb;
    padding: 10px 20px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background: #007bff;
    color: white;
    font-weight: bold;
}
QPushButton {
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #0056b3;
}
QPushButton:disabled {
    background-color: #555;
    color: #888;
}
QLineEdit {
    padding: 8px;
    border: 1px solid #555;
    border-radius: 4px;
    background-color: #333;
    color: white;
}
QLineEdit:focus {
    border: 1px solid #007bff;
}
QListWidget {
    background-color: #333;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 5px;
}
QListWidget::item {
    padding: 10px;
    border-bottom: 1px solid #444;
}
QListWidget::item:selected {
    background-color: #007bff;
    color: white;
    border-radius: 2px;
}
QTableWidget {
    background-color: #333;
    gridline-color: #555;
    border: 1px solid #555;
}
QHeaderView::section {
    background-color: #444;
    padding: 5px;
    border: 1px solid #555;
    color: white;
    font-weight: bold;
}
QLabel#title {
    font-size: 24px;
    font-weight: bold;
    color: #007bff;
    margin-bottom: 20px;
}
QLabel#stats {
    background-color: #333;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #555;
    font-weight: bold;
}
"""

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setFixedSize(350, 250)
        self.setStyleSheet(STYLESHEET)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("Chemical Visualizer")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        layout.addWidget(self.username)
        
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)
        
        self.btn_login = QPushButton("Login")
        self.btn_login.clicked.connect(self.handle_login)
        layout.addWidget(self.btn_login)
        
        self.setLayout(layout)
        self.token = None

    def handle_login(self):
        username = self.username.text()
        password = self.password.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        try:
            resp = requests.post(f"{API_BASE}/api-token-auth/", data={
                'username': username, 'password': password
            })
            
            if resp.status_code == 200:
                self.token = resp.json()['token']
                self.accept()
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid credentials. Please try again.")
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Could not connect to server: {str(e)}")

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # Dark theme for Matplotlib
        with plt.style.context('dark_background'):
            self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#2b2b2b')
            self.axes = self.fig.add_subplot(111)
            self.axes.set_facecolor('#333333')
        super(MplCanvas, self).__init__(self.fig)

class MainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.headers = {'Authorization': f'Token {self.token}'}
        self.current_analysis_id = None
        
        self.setWindowTitle("Chemical Analysis Platform")
        self.setGeometry(100, 100, 1100, 750)
        self.setStyleSheet(STYLESHEET)

        # Main Layout
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Setup Tabs
        self.setup_dashboard_tab()
        self.setup_history_tab()
        self.setup_data_tab()
        
        # Initial Load
        self.refresh_history()

    def setup_dashboard_tab(self):
        self.dashboard_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header Controls
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #333; border-radius: 8px; padding: 10px;")
        header_layout = QHBoxLayout(header_frame)
        
        self.btn_upload = QPushButton("Upload New CSV")
        self.btn_upload.setIcon(QIcon.fromTheme("document-open"))
        self.btn_upload.clicked.connect(self.upload_file)
        
        self.btn_pdf = QPushButton("Download PDF Report")
        self.btn_pdf.setIcon(QIcon.fromTheme("document-save"))
        self.btn_pdf.setEnabled(False)
        self.btn_pdf.clicked.connect(self.download_pdf)
        
        header_layout.addWidget(self.btn_upload)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_pdf)
        
        layout.addWidget(header_frame)
        
        # Statistics
        self.stats_label = QLabel("Welcome! Upload a CSV file to begin analysis.")
        self.stats_label.setObjectName("stats")
        self.stats_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.stats_label)
        
        # Chart
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.setSizePolicy(5, 7) # Expanding
        layout.addWidget(self.canvas)
        
        self.dashboard_tab.setLayout(layout)
        self.tabs.addTab(self.dashboard_tab, "Analytics Dashboard")

    def setup_history_tab(self):
        self.history_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        top_bar = QHBoxLayout()
        lbl = QLabel("Recent Analysis History")
        lbl.setStyleSheet("font-size: 18px; color: white;")
        
        self.btn_refresh = QPushButton("Refresh List")
        self.btn_refresh.setFixedWidth(150)
        self.btn_refresh.clicked.connect(self.refresh_history)
        
        top_bar.addWidget(lbl)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_refresh)
        layout.addLayout(top_bar)
        
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.load_history_item)
        layout.addWidget(self.history_list)
        
        self.history_tab.setLayout(layout)
        self.tabs.addTab(self.history_tab, "History")

    def setup_data_tab(self):
        self.data_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.data_table = QTableWidget()
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.data_table.verticalHeader().setVisible(False)
        layout.addWidget(self.data_table)
        
        self.data_tab.setLayout(layout)
        self.tabs.addTab(self.data_tab, "Raw Data Inspector")

    def upload_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Select CSV', '', 'CSV Files (*.csv)')
        if fname:
            self.stats_label.setText("Processing file...")
            QApplication.processEvents()
            
            try:
                files = {'file': open(fname, 'rb')}
                resp = requests.post(f"{API_BASE}/api/upload/", headers=self.headers, files=files)
                
                if resp.status_code == 200:
                    data = resp.json()
                    self.update_dashboard(data)
                    self.refresh_history()
                    self.load_raw_data(data['id'])
                else:
                    QMessageBox.warning(self, "Upload Failed", f"Server responded with: {resp.status_code}")
                    self.stats_label.setText("Ready")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Upload error: {str(e)}")
                self.stats_label.setText("Ready")

    def update_dashboard(self, data):
        summary = data.get('summary', data)
        self.current_analysis_id = data.get('id')
        self.btn_pdf.setEnabled(True)
        
        # Colorized HTML text
        text = (f"<div style='text-align:center'>"
                f"<span style='font-size:18px; color:#007bff'>Analysis #{data.get('id')}</span><br><br>"
                f"<table width='100%' style='font-size:16px'>"
                f"<tr><td>Total Equipment:</td><td><b>{summary.get('total_count')}</b></td>"
                f"<td>Avg Pressure:</td><td><b>{summary.get('avg_pressure')} Pa</b></td>"
                f"<td>Avg Temperature:</td><td><b>{summary.get('avg_temp')} °C</b></td></tr>"
                f"</table></div>")
        self.stats_label.setText(text)
        
        # Update Chart
        self.canvas.axes.clear()
        tc = summary.get('type_counts', {})
        colors = ['#007bff', '#28a745', '#dc3545', '#ffc107', '#17a2b8']
        
        bars = self.canvas.axes.bar(tc.keys(), tc.values(), color=colors[:len(tc)])
        self.canvas.axes.set_title(f"Equipment Distribution (ID: {data.get('id')})", color='white', fontsize=14)
        self.canvas.axes.tick_params(colors='white')
        
        # Set spines color
        for spine in self.canvas.axes.spines.values():
            spine.set_color('#555')
            
        self.canvas.draw()
        
        # Switch focus
        self.tabs.setCurrentIndex(0)

    def download_pdf(self):
        if self.current_analysis_id:
            try:
                url = f"{API_BASE}/api/analysis/{self.current_analysis_id}/pdf/"
                resp = requests.get(url, headers=self.headers)
                
                if resp.status_code == 200:
                    fname, _ = QFileDialog.getSaveFileName(self, 'Save PDF', 
                                                           f'Analysis_{self.current_analysis_id}.pdf', 
                                                           'PDF Files (*.pdf)')
                    if fname:
                        with open(fname, 'wb') as f:
                            f.write(resp.content)
                        QMessageBox.information(self, "Download Complete", "PDF report saved successfully.")
                else:
                    QMessageBox.warning(self, "Download Failed", f"Status: {resp.status_code}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def refresh_history(self):
        try:
            resp = requests.get(f"{API_BASE}/api/history/", headers=self.headers)
            if resp.status_code == 200:
                self.history_list.clear()
                self.history_data = resp.json()
                for item in self.history_data:
                    date_str = item['uploaded_at'].split("T")[0]
                    time_str = item['uploaded_at'].split("T")[1][:5]
                    display = f" Analysis #{item['id']}  |  📅 {date_str} {time_str}  |  📊 {item['summary']['total_count']} items"
                    self.history_list.addItem(display)
        except Exception as e:
            print(f"History error: {e}")

    def load_history_item(self, item):
        idx = self.history_list.row(item)
        data = self.history_data[idx]
        self.update_dashboard(data)
        self.load_raw_data(data['id'])

    def load_raw_data(self, aid):
        try:
            resp = requests.get(f"{API_BASE}/api/analysis/{aid}/data/", headers=self.headers)
            if resp.status_code == 200:
                rows = resp.json()
                if not rows: return
                
                cols = list(rows[0].keys())
                self.data_table.setColumnCount(len(cols))
                self.data_table.setRowCount(len(rows))
                self.data_table.setHorizontalHeaderLabels(cols)
                
                for r, row_data in enumerate(rows):
                    for c, col in enumerate(cols):
                        val = str(row_data.get(col, ""))
                        item = QTableWidgetItem(val)
                        item.setTextAlignment(Qt.AlignCenter)
                        self.data_table.setItem(r, c, item)
        except Exception as e:
            print(f"Data error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    import matplotlib.pyplot as plt
    
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        window = MainWindow(login.token)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)