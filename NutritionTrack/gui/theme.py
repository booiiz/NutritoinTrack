"""
Theme management for the Nutrition and Diet Planning System
"""
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt

class Theme:
    """Class for managing application themes"""
    
    @staticmethod
    def apply_dark_theme(app):
        """Apply dark theme to the application"""
        # Set dark palette
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        
        # Apply palette
        app.setPalette(palette)
        
        # Apply stylesheet for modern look
        app.setStyleSheet("""
            QMainWindow, QDialog {
                background-color: #353535;
            }
            
            QWidget {
                color: #ffffff;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            
            QLabel {
                color: #ffffff;
            }
            
            QGroupBox {
                border: 1px solid #5c5c5c;
                border-radius: 5px;
                margin-top: 1em;
                padding-top: 10px;
                font-weight: bold;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            
            QPushButton {
                background-color: #2a82da;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #3a92ea;
            }
            
            QPushButton:pressed {
                background-color: #1a72ca;
            }
            
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #5c5c5c;
                border-radius: 4px;
                padding: 5px;
                min-height: 20px;
            }
            
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border: 1px solid #2a82da;
            }
            
            QComboBox::drop-down {
                border: 0px;
                width: 20px;
            }
            
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: white;
                selection-background-color: #2a82da;
            }
            
            QTableWidget {
                background-color: #2d2d2d;
                alternate-background-color: #353535;
                gridline-color: #5c5c5c;
                color: white;
                selection-background-color: #2a82da;
                selection-color: white;
                border-radius: 4px;
                border: 1px solid #5c5c5c;
            }
            
            QTableWidget::item {
                padding: 4px;
            }
            
            QTableWidget QHeaderView::section {
                background-color: #444444;
                color: white;
                padding: 4px;
                border: 1px solid #5c5c5c;
                font-weight: bold;
            }
            
            QScrollBar:vertical {
                border: none;
                background: #2d2d2d;
                width: 10px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background: #5c5c5c;
                min-height: 20px;
                border-radius: 5px;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            
            QScrollBar:horizontal {
                border: none;
                background: #2d2d2d;
                height: 10px;
                margin: 0px;
            }
            
            QScrollBar::handle:horizontal {
                background: #5c5c5c;
                min-width: 20px;
                border-radius: 5px;
            }
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
                width: 0px;
            }
            
            QProgressBar {
                border: 1px solid #5c5c5c;
                border-radius: 4px;
                text-align: center;
                background-color: #2d2d2d;
                height: 15px;
            }
            
            QProgressBar::chunk {
                border-radius: 4px;
            }
            
            QListWidget {
                background-color: #2d2d2d;
                border-radius: 4px;
                border: 1px solid #5c5c5c;
                color: white;
                padding: 5px;
            }
            
            QListWidget::item:selected {
                background-color: #2a82da;
                color: white;
            }
            
            QToolBar {
                background-color: #444444;
                spacing: 5px;
                border: 1px solid #5c5c5c;
            }
            
            QStatusBar {
                background-color: #444444;
                color: white;
            }
        """)
    
    @staticmethod
    def apply_light_theme(app):
        """Apply light theme to the application"""
        # Reset to default palette
        app.setPalette(QPalette())
        
        # Apply stylesheet for modern look
        app.setStyleSheet("""
            QMainWindow, QDialog {
                background-color: #f5f5f5;
            }
            
            QWidget {
                color: #333333;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            
            QGroupBox {
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 1em;
                padding-top: 10px;
                font-weight: bold;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #1a88e7;
            }
            
            QPushButton:pressed {
                background-color: #0068c7;
            }
            
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                background-color: white;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
                min-height: 20px;
            }
            
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border: 1px solid #0078d7;
            }
            
            QComboBox::drop-down {
                border: 0px;
                width: 20px;
            }
            
            QComboBox QAbstractItemView {
                background-color: white;
                color: #333333;
                selection-background-color: #0078d7;
                selection-color: white;
            }
            
            QTableWidget {
                background-color: white;
                alternate-background-color: #f9f9f9;
                gridline-color: #dddddd;
                color: #333333;
                selection-background-color: #0078d7;
                selection-color: white;
                border-radius: 4px;
                border: 1px solid #cccccc;
            }
            
            QTableWidget::item {
                padding: 4px;
            }
            
            QTableWidget QHeaderView::section {
                background-color: #e6e6e6;
                color: #333333;
                padding: 4px;
                border: 1px solid #cccccc;
                font-weight: bold;
            }
            
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background: #c1c1c1;
                min-height: 20px;
                border-radius: 5px;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            
            QScrollBar:horizontal {
                border: none;
                background: #f0f0f0;
                height: 10px;
                margin: 0px;
            }
            
            QScrollBar::handle:horizontal {
                background: #c1c1c1;
                min-width: 20px;
                border-radius: 5px;
            }
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
                width: 0px;
            }
            
            QProgressBar {
                border: 1px solid #cccccc;
                border-radius: 4px;
                text-align: center;
                background-color: white;
                height: 15px;
            }
            
            QProgressBar::chunk {
                border-radius: 4px;
            }
            
            QListWidget {
                background-color: white;
                border-radius: 4px;
                border: 1px solid #cccccc;
                color: #333333;
                padding: 5px;
            }
            
            QListWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
            
            QToolBar {
                background-color: #e6e6e6;
                spacing: 5px;
                border: 1px solid #cccccc;
            }
            
            QStatusBar {
                background-color: #e6e6e6;
                color: #333333;
            }
        """)