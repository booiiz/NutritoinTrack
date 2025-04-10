"""
Meal plan display widget for viewing and modifying meal plans
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QGroupBox, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QSplitter, QSizePolicy, QProgressBar, QMenu
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QAction, QColor

class MealPlanDisplay(QWidget):
    """Widget for displaying and interacting with meal plans"""
    
    # Signals for meal plan actions
    regenerate_meal_requested = pyqtSignal(str)  # Emits meal_id
    add_food_requested = pyqtSignal(str)  # Emits meal_id
    remove_food_requested = pyqtSignal(str, int)  # Emits meal_id, food_index
    generate_report_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.meal_plan = None
        self.nutrition_targets = None
        
        # Initialize UI
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Title and action bar
        title_bar = QHBoxLayout()
        
        self.title_label = QLabel("Meal Plan")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        title_bar.addWidget(self.title_label)
        
        title_bar.addStretch()
        
        self.new_plan_btn = QPushButton("New Plan")
        self.new_plan_btn.clicked.connect(self._request_new_plan)
        title_bar.addWidget(self.new_plan_btn)
        
        self.report_btn = QPushButton("Generate Report")
        self.report_btn.clicked.connect(self.generate_report_requested.emit)
        title_bar.addWidget(self.report_btn)
        
        main_layout.addLayout(title_bar)
        
        # Create a splitter for nutrition summary and meal details
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Nutrition summary panel (left side)
        self.nutrition_panel = QWidget()
        nutrition_layout = QVBoxLayout(self.nutrition_panel)
        
        # Summary box
        summary_group = QGroupBox("Nutrition Summary")
        summary_layout = QFormLayout()
        
        # Nutrition progress bars
        self.calories_bar = QProgressBar()
        self.calories_bar.setTextVisible(True)
        summary_layout.addRow("Calories:", self.calories_bar)
        
        self.protein_bar = QProgressBar()
        self.protein_bar.setTextVisible(True)
        summary_layout.addRow("Protein:", self.protein_bar)
        
        self.carbs_bar = QProgressBar()
        self.carbs_bar.setTextVisible(True)
        summary_layout.addRow("Carbs:", self.carbs_bar)
        
        self.fat_bar = QProgressBar()
        self.fat_bar.setTextVisible(True)
        summary_layout.addRow("Fat:", self.fat_bar)
        
        self.fiber_bar = QProgressBar()
        self.fiber_bar.setTextVisible(True)
        summary_layout.addRow("Fiber:", self.fiber_bar)
        
        # Overall completion
        self.completion_label = QLabel("Plan Completion: 0%")
        summary_layout.addRow(self.completion_label)
        
        summary_group.setLayout(summary_layout)
        nutrition_layout.addWidget(summary_group)
        
        # Add nutritional information box
        nutrition_info_group = QGroupBox("Nutritional Information")
        nutrition_info_layout = QVBoxLayout()
        
        self.nutrition_info_label = QLabel(
            "This meal plan provides a balanced distribution of nutrients to meet your daily needs."
        )
        self.nutrition_info_label.setWordWrap(True)
        nutrition_info_layout.addWidget(self.nutrition_info_label)
        
        nutrition_tips = QLabel(
            "<b>Tips:</b><ul>"
            "<li>Aim to eat a variety of colorful foods</li>"
            "<li>Stay hydrated by drinking plenty of water</li>"
            "<li>Try to maintain regular meal times</li>"
            "<li>Consider portion sizes to avoid overeating</li>"
            "</ul>"
        )
        nutrition_tips.setTextFormat(Qt.TextFormat.RichText)
        nutrition_tips.setWordWrap(True)
        nutrition_info_layout.addWidget(nutrition_tips)
        
        nutrition_info_group.setLayout(nutrition_info_layout)
        nutrition_layout.addWidget(nutrition_info_group)
        
        # Add stretch to fill any remaining space
        nutrition_layout.addStretch()
        
        # Meal details panel (right side)
        self.meal_details_scroll = QScrollArea()
        self.meal_details_scroll.setWidgetResizable(True)
        self.meal_details_widget = QWidget()
        self.meal_details_layout = QVBoxLayout(self.meal_details_widget)
        self.meal_details_scroll.setWidget(self.meal_details_widget)
        
        # Add widgets to splitter
        splitter.addWidget(self.nutrition_panel)
        splitter.addWidget(self.meal_details_scroll)
        
        # Set initial sizes (40% left, 60% right)
        splitter.setSizes([400, 600])
        
        main_layout.addWidget(splitter)
    
    def set_meal_plan(self, meal_plan, nutrition_targets):
        """Set the meal plan to display"""
        self.meal_plan = meal_plan
        self.nutrition_targets = nutrition_targets
        
        # Update UI with meal plan data
        self._update_display()
    
    def _update_display(self):
        """Update the display with current meal plan data"""
        if not self.meal_plan or not self.nutrition_targets:
            return
        
        # Update title
        self.title_label.setText(self.meal_plan.name)
        
        # Update nutrition summary
        nutrients = self.meal_plan.nutritional_summary
        targets = self.nutrition_targets
        
        # Update progress bars
        self._update_progress_bar(
            self.calories_bar, 
            nutrients.get("calories", 0), 
            targets.get("calories", 1),
            f"{nutrients.get('calories', 0):.0f} / {targets.get('calories', 0):.0f} kcal"
        )
        
        self._update_progress_bar(
            self.protein_bar, 
            nutrients.get("protein", 0), 
            targets.get("protein", 1),
            f"{nutrients.get('protein', 0):.1f} / {targets.get('protein', 0):.1f} g"
        )
        
        self._update_progress_bar(
            self.carbs_bar, 
            nutrients.get("carbs", 0), 
            targets.get("carbs", 1),
            f"{nutrients.get('carbs', 0):.1f} / {targets.get('carbs', 0):.1f} g"
        )
        
        self._update_progress_bar(
            self.fat_bar, 
            nutrients.get("fat", 0), 
            targets.get("fat", 1),
            f"{nutrients.get('fat', 0):.1f} / {targets.get('fat', 0):.1f} g"
        )
        
        self._update_progress_bar(
            self.fiber_bar, 
            nutrients.get("fiber", 0), 
            targets.get("fiber", 1),
            f"{nutrients.get('fiber', 0):.1f} / {targets.get('fiber', 0):.1f} g"
        )
        
        # Update completion label
        completion = self.meal_plan.calculate_completion_percentage()
        self.completion_label.setText(f"Plan Completion: {completion:.1f}%")
        
        # Update nutritional information
        self._update_nutrition_info()
        
        # Clear and recreate meal widgets
        self._clear_meal_widgets()
        self._create_meal_widgets()
    
    def _update_progress_bar(self, bar, value, target, text_format=None):
        """Update a progress bar with the given value and target"""
        if target <= 0:
            percentage = 0
        else:
            percentage = min(100, int((value / target) * 100))
        
        bar.setValue(percentage)
        
        # Set color based on percentage
        if percentage < 70:
            bar.setStyleSheet("QProgressBar::chunk { background-color: #ff9999; }")  # Red - deficient
        elif percentage < 90:
            bar.setStyleSheet("QProgressBar::chunk { background-color: #ffcc99; }")  # Orange - below target
        elif percentage <= 110:
            bar.setStyleSheet("QProgressBar::chunk { background-color: #99ff99; }")  # Green - on target
        elif percentage <= 130:
            bar.setStyleSheet("QProgressBar::chunk { background-color: #ffff99; }")  # Yellow - above target
        else:
            bar.setStyleSheet("QProgressBar::chunk { background-color: #ff9999; }")  # Red - excess
        
        # Set custom text if provided
        if text_format:
            bar.setFormat(text_format)
    
    def _update_nutrition_info(self):
        """Update the nutrition information text based on meal plan analysis"""
        if not self.meal_plan or not self.nutrition_targets:
            return
        
        completion = self.meal_plan.calculate_completion_percentage()
        
        # Generate appropriate message based on completion
        if completion < 50:
            message = (
                "This meal plan is currently <b>below</b> your nutritional needs. "
                "Consider adding more foods to meet your daily requirements."
            )
        elif completion < 80:
            message = (
                "This meal plan provides <b>most</b> of your nutritional needs, "
                "but could be improved to better meet your targets."
            )
        elif completion <= 110:
            message = (
                "This meal plan provides a <b>balanced</b> distribution of nutrients "
                "and meets your daily needs well."
            )
        else:
            message = (
                "This meal plan <b>exceeds</b> some of your nutritional targets. "
                "Consider adjusting portions to align better with your goals."
            )
        
        self.nutrition_info_label.setText(message)
    
    def _clear_meal_widgets(self):
        """Clear all meal widgets from the layout"""
        while self.meal_details_layout.count():
            item = self.meal_details_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def _create_meal_widgets(self):
        """Create widgets for each meal in the plan"""
        if not self.meal_plan:
            return
        
        # Sort meals by day and type
        meal_order = ["breakfast", "morning_snack", "lunch", "afternoon_snack", "dinner", "evening_snack"]
        
        # Group meals by day
        meals_by_day = {}
        for meal in self.meal_plan.meals:
            day = meal["day"]
            if day not in meals_by_day:
                meals_by_day[day] = []
            meals_by_day[day].append(meal)
        
        # Add each day's meals
        for day in sorted(meals_by_day.keys()):
            # Add day header if we have multiple days
            if len(meals_by_day) > 1:
                day_label = QLabel(f"Day {day}")
                day_label.setStyleSheet("font-size: 16px; font-weight: bold;")
                self.meal_details_layout.addWidget(day_label)
            
            # Sort meals by type
            sorted_meals = sorted(
                meals_by_day[day], 
                key=lambda m: meal_order.index(m["type"]) if m["type"] in meal_order else 99
            )
            
            # Add each meal
            for meal in sorted_meals:
                self._add_meal_widget(meal)
        
        # Add stretch to fill remaining space
        self.meal_details_layout.addStretch()
    
    def _add_meal_widget(self, meal):
        """Add a widget for a specific meal"""
        # Create meal group box
        meal_title = meal["type"].replace("_", " ").title()
        meal_group = QGroupBox(meal_title)
        meal_layout = QVBoxLayout()
        
        # Add meal summary
        summary_layout = QHBoxLayout()
        
        calories = meal["nutrients"]["calories"]
        protein = meal["nutrients"]["protein"]
        carbs = meal["nutrients"]["carbs"]
        fat = meal["nutrients"]["fat"]
        
        summary_label = QLabel(
            f"Calories: <b>{calories:.0f} kcal</b> | "
            f"Protein: {protein:.1f}g | "
            f"Carbs: {carbs:.1f}g | "
            f"Fat: {fat:.1f}g"
        )
        summary_label.setTextFormat(Qt.TextFormat.RichText)
        summary_layout.addWidget(summary_label)
        
        summary_layout.addStretch()
        
        # Add action buttons
        regenerate_btn = QPushButton("Regenerate")
        regenerate_btn.setProperty("meal_id", meal["id"])
        regenerate_btn.clicked.connect(
            lambda: self.regenerate_meal_requested.emit(meal["id"])
        )
        summary_layout.addWidget(regenerate_btn)
        
        add_food_btn = QPushButton("Add Food")
        add_food_btn.setProperty("meal_id", meal["id"])
        add_food_btn.clicked.connect(
            lambda: self.add_food_requested.emit(meal["id"])
        )
        summary_layout.addWidget(add_food_btn)
        
        meal_layout.addLayout(summary_layout)
        
        # Create food table
        food_table = QTableWidget()
        food_table.setColumnCount(5)
        food_table.setHorizontalHeaderLabels(["Food", "Quantity", "Calories", "Protein", "Actions"])
        food_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        food_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        food_table.setRowCount(len(meal["foods"]))
        
        # Fill food table
        for i, food in enumerate(meal["foods"]):
            # Food name
            name_item = QTableWidgetItem(food["name"])
            food_table.setItem(i, 0, name_item)
            
            # Quantity
            quantity_text = f"{food['quantity']} {food['serving_unit']}"
            quantity_item = QTableWidgetItem(quantity_text)
            food_table.setItem(i, 1, quantity_item)
            
            # Calories
            calories = food["nutrients"].get("calories", 0)
            calories_item = QTableWidgetItem(f"{calories:.0f} kcal")
            food_table.setItem(i, 2, calories_item)
            
            # Protein
            protein = food["nutrients"].get("protein", 0)
            protein_item = QTableWidgetItem(f"{protein:.1f} g")
            food_table.setItem(i, 3, protein_item)
            
            # Actions (remove button)
            remove_btn = QPushButton("Remove")
            remove_btn.setProperty("meal_id", meal["id"])
            remove_btn.setProperty("food_index", i)
            remove_btn.clicked.connect(
                lambda checked, meal_id=meal["id"], index=i: 
                self.remove_food_requested.emit(meal_id, index)
            )
            food_table.setCellWidget(i, 4, remove_btn)
        
        meal_layout.addWidget(food_table)
        meal_group.setLayout(meal_layout)
        
        self.meal_details_layout.addWidget(meal_group)
    
    def _request_new_plan(self):
        """Request generation of a new meal plan"""
        # This just emits the same signal as the "Generate Meal Plan" action in the main window
        self.generate_report_requested.emit()
