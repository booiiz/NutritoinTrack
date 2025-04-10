"""
Main window for the Nutrition and Diet Planning System
"""
import sys
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QStackedWidget, QMessageBox,
    QSplitter, QStatusBar, QToolBar, QFileDialog, 
    QApplication
)
from PyQt6.QtGui import QAction, QIcon, QFont
from PyQt6.QtCore import Qt, QSize, QSettings

from models.user_profile import UserProfile
from models.food_database import FoodDatabase
from services.rule_engine import RuleEngine
from services.meal_planner import MealPlanner
from services.nutrition_calculator import NutritionCalculator
from services.report_generator import ReportGenerator

from gui.profile_form import ProfileForm
from gui.meal_plan_display import MealPlanDisplay
from gui.food_selection import FoodSelectionDialog
from gui.report_view import ReportView
from gui.theme import Theme

class MainWindow(QMainWindow):
    """Main Application Window"""
    
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Nutrition and Diet Planning System")
        self.setMinimumSize(1200, 800)
        
        # Initialize models and services
        self.food_database = FoodDatabase()
        self.rule_engine = RuleEngine()
        self.meal_planner = MealPlanner(self.food_database, self.rule_engine)
        self.report_generator = ReportGenerator()
        
        # State variables
        self.current_profile = None
        self.current_meal_plan = None
        self.nutrition_targets = None
        
        # Initialize UI
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the user interface"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(self.central_widget)
        
        # Create stacked widget for main content
        self.stacked_widget = QStackedWidget()
        
        # Create pages for stacked widget
        self.welcome_page = self._create_welcome_page()
        self.profile_page = ProfileForm()
        self.meal_plan_page = MealPlanDisplay()
        self.report_page = ReportView()
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.addWidget(self.profile_page)
        self.stacked_widget.addWidget(self.meal_plan_page)
        self.stacked_widget.addWidget(self.report_page)
        
        # Add stacked widget to main layout
        main_layout.addWidget(self.stacked_widget)
        
        # Set up status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Welcome to the Nutrition and Diet Planning System")
        
        # Set up toolbar
        self._setup_toolbar()
        
        # Connect signals
        self._connect_signals()
        
        # Start with welcome page
        self.stacked_widget.setCurrentIndex(0)
    
    def _create_welcome_page(self):
        """Create the welcome page widget"""
        welcome_widget = QWidget()
        welcome_widget.setObjectName("welcomePage")
        layout = QVBoxLayout(welcome_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Add title label
        title_label = QLabel("Nutrition and Diet Planning System")
        title_label.setObjectName("welcomeTitle")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Add description label
        desc_label = QLabel(
            "A smart application to help you create personalized diet plans based on your "
            "health conditions, dietary preferences, and nutritional requirements."
        )
        desc_label.setObjectName("welcomeDescription")
        desc_font = QFont()
        desc_font.setPointSize(12)
        desc_label.setFont(desc_font)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Add spacer
        layout.addSpacing(60)
        
        # Create buttons container - center buttons
        buttons_container = QWidget()
        buttons_container.setObjectName("welcomeButtonsContainer")
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_layout.setSpacing(20)
        
        # New Profile button
        new_profile_btn = QPushButton("Create New Profile")
        new_profile_btn.setObjectName("welcomeButton")
        new_profile_btn.setMinimumSize(QSize(220, 60))
        new_profile_btn.clicked.connect(self.create_new_profile)
        buttons_layout.addWidget(new_profile_btn)
        
        # Load Profile button
        load_profile_btn = QPushButton("Load Existing Profile")
        load_profile_btn.setObjectName("welcomeButton")
        load_profile_btn.setMinimumSize(QSize(220, 60))
        load_profile_btn.clicked.connect(self.load_existing_profile)
        buttons_layout.addWidget(load_profile_btn)
        
        # Add buttons to layout
        layout.addWidget(buttons_container)
        
        # Add spacing
        layout.addSpacing(40)
        
        # Create features container with shadow and border
        features_container = QWidget()
        features_container.setObjectName("featuresContainer")
        features_layout = QVBoxLayout(features_container)
        
        # Features title
        features_title = QLabel("Features")
        features_title.setObjectName("featuresTitle")
        features_title_font = QFont()
        features_title_font.setPointSize(16)
        features_title_font.setBold(True)
        features_title.setFont(features_title_font)
        features_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        features_layout.addWidget(features_title)
        
        # Add some features description
        features = [
            "Create and manage user profiles with health conditions and dietary preferences",
            "Calculate your daily nutritional requirements",
            "Generate personalized meal plans",
            "Analyze and visualize your nutritional intake",
            "Create detailed nutrition reports"
        ]
        
        for feature in features:
            feature_item = QLabel(f"• {feature}")
            feature_item.setObjectName("featureItem")
            feature_item.setWordWrap(True)
            features_layout.addWidget(feature_item)
        
        # Add features container to main layout
        layout.addWidget(features_container)
        
        # Add spacer at the bottom
        layout.addStretch()
        
        # Apply additional styling
        welcome_widget.setStyleSheet("""
            #welcomeTitle {
                color: palette(highlight);
                margin-bottom: 10px;
            }
            
            #welcomeDescription {
                margin-bottom: 20px;
            }
            
            #welcomeButton {
                font-size: 14px;
                font-weight: bold;
            }
            
            #featuresContainer {
                background-color: palette(base);
                border-radius: 10px;
                padding: 20px;
                border: 1px solid palette(mid);
            }
            
            #featuresTitle {
                color: palette(highlight);
                margin-bottom: 15px;
            }
            
            #featureItem {
                padding: 5px 0;
                font-size: 14px;
            }
        """)
        
        return welcome_widget
    
    def _setup_toolbar(self):
        """Set up the application toolbar"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Home action
        home_action = QAction("Home", self)
        home_action.setStatusTip("Go to the welcome page")
        home_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        toolbar.addAction(home_action)
        
        # Profile action
        profile_action = QAction("Profile", self)
        profile_action.setStatusTip("View or edit user profile")
        profile_action.triggered.connect(self.show_profile_page)
        toolbar.addAction(profile_action)
        
        # Meal Plan action
        meal_plan_action = QAction("Meal Plan", self)
        meal_plan_action.setStatusTip("View or generate meal plans")
        meal_plan_action.triggered.connect(self.show_meal_plan_page)
        toolbar.addAction(meal_plan_action)
        
        # Report action
        report_action = QAction("Reports", self)
        report_action.setStatusTip("View nutrition reports")
        report_action.triggered.connect(self.show_report_page)
        toolbar.addAction(report_action)
        
        # Add separator
        toolbar.addSeparator()
        
        # Generate Meal Plan action
        generate_plan_action = QAction("Generate Meal Plan", self)
        generate_plan_action.setStatusTip("Generate a new meal plan")
        generate_plan_action.triggered.connect(self.generate_meal_plan)
        toolbar.addAction(generate_plan_action)
        
        # Add separator
        toolbar.addSeparator()
        
        # Theme Toggle action
        theme_action = QAction("Toggle Theme", self)
        theme_action.setStatusTip("Toggle between light and dark themes")
        theme_action.triggered.connect(self.toggle_theme)
        toolbar.addAction(theme_action)
        
        # Add separator
        toolbar.addSeparator()
        
        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        toolbar.addAction(exit_action)
    
    def _connect_signals(self):
        """Connect signals between widgets"""
        # Connect profile form signals
        self.profile_page.profile_saved.connect(self.on_profile_saved)
        
        # Connect meal plan display signals
        self.meal_plan_page.regenerate_meal_requested.connect(self.regenerate_meal)
        self.meal_plan_page.add_food_requested.connect(self.show_food_selection)
        self.meal_plan_page.remove_food_requested.connect(self.remove_food_from_meal)
        self.meal_plan_page.generate_report_requested.connect(self.generate_report)
    
    def create_new_profile(self):
        """Create a new user profile"""
        self.current_profile = UserProfile()
        self.profile_page.set_profile(self.current_profile)
        self.stacked_widget.setCurrentWidget(self.profile_page)
        self.status_bar.showMessage("Creating new user profile")
    
    def load_existing_profile(self):
        """Load an existing user profile"""
        profiles = UserProfile.get_all_profiles()
        
        if not profiles:
            QMessageBox.information(
                self, "No Profiles Found", 
                "No existing profiles found. Please create a new profile."
            )
            self.create_new_profile()
            return
        
        # For simplicity, just load the first profile
        # In a real app, this would show a dialog to select a profile
        self.current_profile = profiles[0]
        self.profile_page.set_profile(self.current_profile)
        self.stacked_widget.setCurrentWidget(self.profile_page)
        self.status_bar.showMessage(f"Loaded profile: {self.current_profile.name}")
    
    def on_profile_saved(self, profile):
        """Handle profile saved event"""
        self.current_profile = profile
        self.status_bar.showMessage(f"Profile saved: {profile.name}")
        
        # Calculate nutrition targets
        self.nutrition_targets = NutritionCalculator.calculate_nutrition_targets(profile)
        
        # Show meal plan page
        self.show_meal_plan_page()
    
    def show_profile_page(self):
        """Show the profile page"""
        if not self.current_profile:
            QMessageBox.information(
                self, "No Profile Selected", 
                "Please create or load a profile first."
            )
            return
        
        self.profile_page.set_profile(self.current_profile)
        self.stacked_widget.setCurrentWidget(self.profile_page)
        self.status_bar.showMessage("Viewing user profile")
    
    def show_meal_plan_page(self):
        """Show the meal plan page"""
        if not self.current_profile:
            QMessageBox.information(
                self, "No Profile Selected", 
                "Please create or load a profile first."
            )
            return
        
        if not self.current_meal_plan:
            self.generate_meal_plan()
        
        self.meal_plan_page.set_meal_plan(self.current_meal_plan, self.nutrition_targets)
        self.stacked_widget.setCurrentWidget(self.meal_plan_page)
        self.status_bar.showMessage("Viewing meal plan")
    
    def show_report_page(self):
        """Show the report page"""
        if not self.current_profile or not self.current_meal_plan:
            QMessageBox.information(
                self, "No Data Available", 
                "Please create a profile and generate a meal plan first."
            )
            return
        
        # Generate a report
        report = self.report_generator.generate_full_report(
            self.current_meal_plan, 
            self.nutrition_targets,
            self.current_profile
        )
        
        # Set the report in the report view
        self.report_page.set_report(report)
        
        # Show the report page
        self.stacked_widget.setCurrentWidget(self.report_page)
        self.status_bar.showMessage("Viewing nutrition report")
    
    def generate_meal_plan(self):
        """Generate a new meal plan"""
        if not self.current_profile:
            QMessageBox.information(
                self, "No Profile Selected", 
                "Please create or load a profile first."
            )
            return
        
        # Generate a meal plan
        self.current_meal_plan = self.meal_planner.generate_meal_plan(self.current_profile)
        
        # Save the meal plan
        self.current_meal_plan.save()
        
        # Show the meal plan
        self.meal_plan_page.set_meal_plan(self.current_meal_plan, self.nutrition_targets)
        self.stacked_widget.setCurrentWidget(self.meal_plan_page)
        self.status_bar.showMessage("Generated new meal plan")
    
    def regenerate_meal(self, meal_id):
        """Regenerate a single meal in the current meal plan"""
        if not self.current_meal_plan:
            return
        
        # Regenerate the meal
        self.current_meal_plan = self.meal_planner.regenerate_meal(
            self.current_meal_plan, 
            self.current_profile, 
            meal_id
        )
        
        # Save the updated meal plan
        self.current_meal_plan.save()
        
        # Update the meal plan display
        self.meal_plan_page.set_meal_plan(self.current_meal_plan, self.nutrition_targets)
        self.status_bar.showMessage("Regenerated meal")
    
    def show_food_selection(self, meal_id):
        """Show food selection dialog"""
        dialog = FoodSelectionDialog(self.food_database, self.current_profile, self)
        if dialog.exec():
            selected_foods = dialog.get_selected_foods()
            for food_data in selected_foods:
                # Add food to meal
                self.current_meal_plan.add_food_to_meal(
                    meal_id, 
                    food_data["food"], 
                    food_data["quantity"]
                )
            
            # Save the updated meal plan
            self.current_meal_plan.save()
            
            # Update the meal plan display
            self.meal_plan_page.set_meal_plan(self.current_meal_plan, self.nutrition_targets)
            self.status_bar.showMessage("Added foods to meal")
    
    def remove_food_from_meal(self, meal_id, food_index):
        """Remove a food from a meal"""
        if not self.current_meal_plan:
            return
        
        # Remove the food
        self.current_meal_plan.remove_food_from_meal(meal_id, food_index)
        
        # Save the updated meal plan
        self.current_meal_plan.save()
        
        # Update the meal plan display
        self.meal_plan_page.set_meal_plan(self.current_meal_plan, self.nutrition_targets)
        self.status_bar.showMessage("Removed food from meal")
    
    def generate_report(self):
        """Generate a nutrition report"""
        self.show_report_page()
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        settings = QSettings()
        current_theme = settings.value("app/dark_theme", True, type=bool)
        
        # Toggle theme
        new_theme = not current_theme
        settings.setValue("app/dark_theme", new_theme)
        
        # Apply new theme
        if new_theme:
            Theme.apply_dark_theme(QApplication.instance())
            self.status_bar.showMessage("Dark theme applied")
        else:
            Theme.apply_light_theme(QApplication.instance())
            self.status_bar.showMessage("Light theme applied")
