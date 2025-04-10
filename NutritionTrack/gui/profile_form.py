"""
Profile form for creating and editing user profiles
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QComboBox, QDoubleSpinBox, QSpinBox, QFormLayout, 
    QPushButton, QGroupBox, QScrollArea, QCheckBox,
    QListWidget, QListWidgetItem, QGridLayout, QSizePolicy,
    QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from models.user_profile import UserProfile

class ProfileForm(QWidget):
    """User profile form for creating and editing user profiles"""
    
    # Signal emitted when profile is saved
    profile_saved = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        
        # Current profile being edited
        self.profile = None
        
        # Initialize UI
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)
        
        # Create scroll content widget
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)
        
        # Form layout for scroll content
        form_layout = QVBoxLayout(scroll_content)
        
        # Title label
        title_label = QLabel("User Profile")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(title_label)
        
        # Personal details group
        personal_group = QGroupBox("Personal Details")
        personal_layout = QFormLayout()
        
        # Name field
        self.name_edit = QLineEdit()
        personal_layout.addRow("Name:", self.name_edit)
        
        # Age field
        self.age_spin = QSpinBox()
        self.age_spin.setRange(1, 120)
        personal_layout.addRow("Age:", self.age_spin)
        
        # Gender field
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        personal_layout.addRow("Gender:", self.gender_combo)
        
        # Weight field
        self.weight_spin = QDoubleSpinBox()
        self.weight_spin.setRange(20.0, 300.0)
        self.weight_spin.setSuffix(" kg")
        self.weight_spin.setDecimals(1)
        personal_layout.addRow("Weight:", self.weight_spin)
        
        # Height field
        self.height_spin = QDoubleSpinBox()
        self.height_spin.setRange(50.0, 250.0)
        self.height_spin.setSuffix(" cm")
        self.height_spin.setDecimals(1)
        personal_layout.addRow("Height:", self.height_spin)
        
        # Activity level field
        self.activity_combo = QComboBox()
        self.activity_combo.addItems([
            "Sedentary (little or no exercise)",
            "Light (exercise 1-3 days/week)",
            "Moderate (exercise 3-5 days/week)",
            "Active (exercise 6-7 days/week)",
            "Very Active (hard daily exercise & physical job)"
        ])
        personal_layout.addRow("Activity Level:", self.activity_combo)
        
        # Add computed BMI
        self.bmi_label = QLabel()
        personal_layout.addRow("BMI:", self.bmi_label)
        
        # Connect signals for BMI calculation
        self.weight_spin.valueChanged.connect(self._update_bmi)
        self.height_spin.valueChanged.connect(self._update_bmi)
        
        personal_group.setLayout(personal_layout)
        form_layout.addWidget(personal_group)
        
        # Health information group
        health_group = QGroupBox("Health Information")
        health_layout = QFormLayout()
        
        # Target weight field
        self.target_weight_spin = QDoubleSpinBox()
        self.target_weight_spin.setRange(20.0, 300.0)
        self.target_weight_spin.setSuffix(" kg")
        self.target_weight_spin.setDecimals(1)
        health_layout.addRow("Target Weight:", self.target_weight_spin)
        
        # Weight goal field
        self.weight_goal_combo = QComboBox()
        self.weight_goal_combo.addItems(["Lose weight", "Maintain weight", "Gain weight"])
        health_layout.addRow("Weight Goal:", self.weight_goal_combo)
        
        # Medical conditions group
        medical_label = QLabel("Medical Conditions:")
        health_layout.addRow(medical_label)
        
        medical_grid = QGridLayout()
        
        self.diabetes_check = QCheckBox("Diabetes")
        self.hypertension_check = QCheckBox("Hypertension")
        self.heart_disease_check = QCheckBox("Heart Disease")
        self.high_cholesterol_check = QCheckBox("High Cholesterol")
        self.kidney_disease_check = QCheckBox("Kidney Disease")
        self.liver_disease_check = QCheckBox("Liver Disease")
        
        medical_grid.addWidget(self.diabetes_check, 0, 0)
        medical_grid.addWidget(self.hypertension_check, 0, 1)
        medical_grid.addWidget(self.heart_disease_check, 1, 0)
        medical_grid.addWidget(self.high_cholesterol_check, 1, 1)
        medical_grid.addWidget(self.kidney_disease_check, 2, 0)
        medical_grid.addWidget(self.liver_disease_check, 2, 1)
        
        health_layout.addRow(medical_grid)
        
        # Allergies field
        allergies_label = QLabel("Allergies:")
        health_layout.addRow(allergies_label)
        
        allergies_grid = QGridLayout()
        
        self.gluten_check = QCheckBox("Gluten")
        self.lactose_check = QCheckBox("Lactose/Dairy")
        self.nuts_check = QCheckBox("Nuts")
        self.shellfish_check = QCheckBox("Shellfish")
        self.egg_check = QCheckBox("Eggs")
        self.soy_check = QCheckBox("Soy")
        
        allergies_grid.addWidget(self.gluten_check, 0, 0)
        allergies_grid.addWidget(self.lactose_check, 0, 1)
        allergies_grid.addWidget(self.nuts_check, 1, 0)
        allergies_grid.addWidget(self.shellfish_check, 1, 1)
        allergies_grid.addWidget(self.egg_check, 2, 0)
        allergies_grid.addWidget(self.soy_check, 2, 1)
        
        health_layout.addRow(allergies_grid)
        
        health_group.setLayout(health_layout)
        form_layout.addWidget(health_group)
        
        # Dietary preferences group
        diet_group = QGroupBox("Dietary Preferences")
        diet_layout = QFormLayout()
        
        # Diet type field
        self.diet_type_combo = QComboBox()
        self.diet_type_combo.addItems([
            "Balanced", "Vegetarian", "Vegan", "Keto", "Low Carb",
            "High Protein", "Mediterranean", "Paleo"
        ])
        diet_layout.addRow("Diet Type:", self.diet_type_combo)
        
        # Meal count field
        self.meal_count_combo = QComboBox()
        self.meal_count_combo.addItems(["3 meals per day", "5 meals per day", "6 meals per day"])
        diet_layout.addRow("Meals per Day:", self.meal_count_combo)
        
        # Food preferences
        diet_layout.addRow(QLabel("Food Preferences:"))
        
        # Liked foods
        self.liked_foods_list = QListWidget()
        self.liked_foods_list.setMaximumHeight(100)
        diet_layout.addRow("Liked Foods:", self.liked_foods_list)
        
        liked_foods_input = QHBoxLayout()
        self.liked_food_edit = QLineEdit()
        add_liked_btn = QPushButton("Add")
        add_liked_btn.clicked.connect(self._add_liked_food)
        remove_liked_btn = QPushButton("Remove")
        remove_liked_btn.clicked.connect(self._remove_liked_food)
        
        liked_foods_input.addWidget(self.liked_food_edit)
        liked_foods_input.addWidget(add_liked_btn)
        liked_foods_input.addWidget(remove_liked_btn)
        diet_layout.addRow("", liked_foods_input)
        
        # Disliked foods
        self.disliked_foods_list = QListWidget()
        self.disliked_foods_list.setMaximumHeight(100)
        diet_layout.addRow("Disliked Foods:", self.disliked_foods_list)
        
        disliked_foods_input = QHBoxLayout()
        self.disliked_food_edit = QLineEdit()
        add_disliked_btn = QPushButton("Add")
        add_disliked_btn.clicked.connect(self._add_disliked_food)
        remove_disliked_btn = QPushButton("Remove")
        remove_disliked_btn.clicked.connect(self._remove_disliked_food)
        
        disliked_foods_input.addWidget(self.disliked_food_edit)
        disliked_foods_input.addWidget(add_disliked_btn)
        disliked_foods_input.addWidget(remove_disliked_btn)
        diet_layout.addRow("", disliked_foods_input)
        
        diet_group.setLayout(diet_layout)
        form_layout.addWidget(diet_group)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save Profile")
        self.save_btn.clicked.connect(self._save_profile)
        
        self.reset_btn = QPushButton("Reset Form")
        self.reset_btn.clicked.connect(self._reset_form)
        
        buttons_layout.addWidget(self.reset_btn)
        buttons_layout.addWidget(self.save_btn)
        
        form_layout.addLayout(buttons_layout)
    
    def set_profile(self, profile):
        """Set the profile to edit"""
        self.profile = profile
        self._populate_form()
    
    def _populate_form(self):
        """Populate form with profile data"""
        if not self.profile:
            self._reset_form()
            return
        
        # Set personal details
        self.name_edit.setText(self.profile.name)
        self.age_spin.setValue(self.profile.age)
        
        gender_index = 0
        if self.profile.gender.lower() == "female":
            gender_index = 1
        elif self.profile.gender.lower() == "other":
            gender_index = 2
        self.gender_combo.setCurrentIndex(gender_index)
        
        self.weight_spin.setValue(self.profile.weight)
        self.height_spin.setValue(self.profile.height)
        
        activity_index = {
            "sedentary": 0,
            "light": 1,
            "moderate": 2,
            "active": 3,
            "very_active": 4
        }.get(self.profile.activity_level, 0)
        self.activity_combo.setCurrentIndex(activity_index)
        
        # Update BMI display
        self._update_bmi()
        
        # Set health information
        self.target_weight_spin.setValue(self.profile.target_weight)
        
        weight_goal_index = {
            "lose": 0,
            "maintain": 1,
            "gain": 2
        }.get(self.profile.weight_goal, 1)
        self.weight_goal_combo.setCurrentIndex(weight_goal_index)
        
        # Set medical conditions
        self.diabetes_check.setChecked("diabetes" in self.profile.medical_conditions)
        self.hypertension_check.setChecked("hypertension" in self.profile.medical_conditions)
        self.heart_disease_check.setChecked("heart_disease" in self.profile.medical_conditions)
        self.high_cholesterol_check.setChecked("high_cholesterol" in self.profile.medical_conditions)
        self.kidney_disease_check.setChecked("kidney_disease" in self.profile.medical_conditions)
        self.liver_disease_check.setChecked("liver_disease" in self.profile.medical_conditions)
        
        # Set allergies
        self.gluten_check.setChecked("gluten" in self.profile.allergies)
        self.lactose_check.setChecked("dairy" in self.profile.allergies)
        self.nuts_check.setChecked("nuts" in self.profile.allergies)
        self.shellfish_check.setChecked("shellfish" in self.profile.allergies)
        self.egg_check.setChecked("eggs" in self.profile.allergies)
        self.soy_check.setChecked("soy" in self.profile.allergies)
        
        # Set dietary preferences
        diet_type_index = {
            "balanced": 0,
            "vegetarian": 1,
            "vegan": 2,
            "keto": 3,
            "low_carb": 4,
            "high_protein": 5,
            "mediterranean": 6,
            "paleo": 7
        }.get(self.profile.diet_type.lower(), 0)
        self.diet_type_combo.setCurrentIndex(diet_type_index)
        
        meal_count_index = {
            3: 0,
            5: 1,
            6: 2
        }.get(self.profile.meal_count, 0)
        self.meal_count_combo.setCurrentIndex(meal_count_index)
        
        # Set food preferences
        self.liked_foods_list.clear()
        for food in self.profile.food_preferences.get("liked", []):
            self.liked_foods_list.addItem(food)
        
        self.disliked_foods_list.clear()
        for food in self.profile.food_preferences.get("disliked", []):
            self.disliked_foods_list.addItem(food)
    
    def _update_bmi(self):
        """Update BMI display based on current weight and height values"""
        weight = self.weight_spin.value()
        height = self.height_spin.value() / 100  # convert to meters
        
        if height > 0 and weight > 0:
            bmi = weight / (height * height)
            
            # BMI category
            category = "Unknown"
            if bmi < 18.5:
                category = "Underweight"
            elif bmi < 25:
                category = "Normal weight"
            elif bmi < 30:
                category = "Overweight"
            else:
                category = "Obese"
            
            self.bmi_label.setText(f"{bmi:.1f} ({category})")
        else:
            self.bmi_label.setText("N/A")
    
    def _add_liked_food(self):
        """Add a food to the liked foods list"""
        food = self.liked_food_edit.text().strip()
        if food:
            self.liked_foods_list.addItem(food)
            self.liked_food_edit.clear()
    
    def _remove_liked_food(self):
        """Remove selected food from liked foods list"""
        selected_items = self.liked_foods_list.selectedItems()
        for item in selected_items:
            self.liked_foods_list.takeItem(self.liked_foods_list.row(item))
    
    def _add_disliked_food(self):
        """Add a food to the disliked foods list"""
        food = self.disliked_food_edit.text().strip()
        if food:
            self.disliked_foods_list.addItem(food)
            self.disliked_food_edit.clear()
    
    def _remove_disliked_food(self):
        """Remove selected food from disliked foods list"""
        selected_items = self.disliked_foods_list.selectedItems()
        for item in selected_items:
            self.disliked_foods_list.takeItem(self.disliked_foods_list.row(item))
    
    def _reset_form(self):
        """Reset the form to default values"""
        self.name_edit.clear()
        self.age_spin.setValue(30)
        self.gender_combo.setCurrentIndex(0)
        self.weight_spin.setValue(70.0)
        self.height_spin.setValue(170.0)
        self.activity_combo.setCurrentIndex(0)
        
        self.target_weight_spin.setValue(70.0)
        self.weight_goal_combo.setCurrentIndex(1)
        
        self.diabetes_check.setChecked(False)
        self.hypertension_check.setChecked(False)
        self.heart_disease_check.setChecked(False)
        self.high_cholesterol_check.setChecked(False)
        self.kidney_disease_check.setChecked(False)
        self.liver_disease_check.setChecked(False)
        
        self.gluten_check.setChecked(False)
        self.lactose_check.setChecked(False)
        self.nuts_check.setChecked(False)
        self.shellfish_check.setChecked(False)
        self.egg_check.setChecked(False)
        self.soy_check.setChecked(False)
        
        self.diet_type_combo.setCurrentIndex(0)
        self.meal_count_combo.setCurrentIndex(0)
        
        self.liked_foods_list.clear()
        self.disliked_foods_list.clear()
        
        self._update_bmi()
    
    def _save_profile(self):
        """Save the profile with form data"""
        if not self.profile:
            self.profile = UserProfile()
        
        # Validate basic required fields
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter your name.")
            return
        
        if self.age_spin.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid age.")
            return
        
        if self.weight_spin.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid weight.")
            return
        
        if self.height_spin.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid height.")
            return
        
        # Set personal details
        self.profile.name = self.name_edit.text().strip()
        self.profile.age = self.age_spin.value()
        self.profile.gender = self.gender_combo.currentText().lower()
        self.profile.weight = self.weight_spin.value()
        self.profile.height = self.height_spin.value()
        
        activity_levels = ["sedentary", "light", "moderate", "active", "very_active"]
        self.profile.activity_level = activity_levels[self.activity_combo.currentIndex()]
        
        # Set health information
        self.profile.target_weight = self.target_weight_spin.value()
        
        weight_goals = ["lose", "maintain", "gain"]
        self.profile.weight_goal = weight_goals[self.weight_goal_combo.currentIndex()]
        
        # Set medical conditions
        self.profile.medical_conditions = []
        if self.diabetes_check.isChecked():
            self.profile.medical_conditions.append("diabetes")
        if self.hypertension_check.isChecked():
            self.profile.medical_conditions.append("hypertension")
        if self.heart_disease_check.isChecked():
            self.profile.medical_conditions.append("heart_disease")
        if self.high_cholesterol_check.isChecked():
            self.profile.medical_conditions.append("high_cholesterol")
        if self.kidney_disease_check.isChecked():
            self.profile.medical_conditions.append("kidney_disease")
        if self.liver_disease_check.isChecked():
            self.profile.medical_conditions.append("liver_disease")
        
        # Set allergies
        self.profile.allergies = []
        if self.gluten_check.isChecked():
            self.profile.allergies.append("gluten")
        if self.lactose_check.isChecked():
            self.profile.allergies.append("dairy")
        if self.nuts_check.isChecked():
            self.profile.allergies.append("nuts")
        if self.shellfish_check.isChecked():
            self.profile.allergies.append("shellfish")
        if self.egg_check.isChecked():
            self.profile.allergies.append("eggs")
        if self.soy_check.isChecked():
            self.profile.allergies.append("soy")
        
        # Set dietary preferences
        diet_types = ["balanced", "vegetarian", "vegan", "keto", "low_carb",
                      "high_protein", "mediterranean", "paleo"]
        self.profile.diet_type = diet_types[self.diet_type_combo.currentIndex()]
        
        meal_counts = [3, 5, 6]
        self.profile.meal_count = meal_counts[self.meal_count_combo.currentIndex()]
        
        # Set food preferences
        liked_foods = []
        for i in range(self.liked_foods_list.count()):
            liked_foods.append(self.liked_foods_list.item(i).text())
        
        disliked_foods = []
        for i in range(self.disliked_foods_list.count()):
            disliked_foods.append(self.disliked_foods_list.item(i).text())
        
        self.profile.food_preferences = {
            "liked": liked_foods,
            "disliked": disliked_foods
        }
        
        # Save profile
        self.profile.save()
        
        # Emit signal that profile was saved
        self.profile_saved.emit(self.profile)
