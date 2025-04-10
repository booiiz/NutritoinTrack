#!/usr/bin/env python3
"""
Nutrition and Diet Planning System - Main Application
"""
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings
from gui.main_window import MainWindow
from gui.theme import Theme

def main():
    """Main application entry point"""
    # Create application directory if it doesn't exist
    os.makedirs(os.path.join(os.path.expanduser("~"), ".nutrition_planner"), exist_ok=True)
    
    # Create Qt Application
    app = QApplication(sys.argv)
    app.setApplicationName("Nutrition and Diet Planning System")
    app.setOrganizationName("NutritionPlanner")
    
    # Load settings
    settings = QSettings()
    use_dark_theme = settings.value("app/dark_theme", True, type=bool)
    
    # Apply theme
    if use_dark_theme:
        Theme.apply_dark_theme(app)
    else:
        Theme.apply_light_theme(app)
    
    # Create and show the main window
    main_window = MainWindow()
    main_window.show()
    
    # Start the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
