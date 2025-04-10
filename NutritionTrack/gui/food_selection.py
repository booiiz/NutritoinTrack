"""
Food selection dialog for choosing foods to add to a meal
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QComboBox, QListWidget, QListWidgetItem,
    QPushButton, QGroupBox, QFormLayout, QDoubleSpinBox,
    QSplitter, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QCheckBox, QScrollArea, QWidget
)
from PyQt6.QtCore import Qt, QSize

class FoodSelectionDialog(QDialog):
    """Dialog for selecting foods to add to a meal"""
    
    def __init__(self, food_database, user_profile, parent=None):
        super().__init__(parent)
        
        self.food_database = food_database
        self.user_profile = user_profile
        self.selected_foods = []
        
        self.setWindowTitle("Select Foods")
        self.setMinimumSize(800, 600)
        
        self._init_ui()
        self._populate_categories()
        self._update_food_list()
    
    def _init_ui(self):
        """Initialize the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Title label
        title_label = QLabel("Select Foods to Add")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title_label)
        
        # Search and filter bar
        filter_layout = QHBoxLayout()
        
        search_label = QLabel("Search:")
        filter_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter food name to search...")
        self.search_input.textChanged.connect(self._update_food_list)
        filter_layout.addWidget(self.search_input)
        
        category_label = QLabel("Category:")
        filter_layout.addWidget(category_label)
        
        self.category_combo = QComboBox()
        self.category_combo.addItem("All Categories")
        self.category_combo.currentIndexChanged.connect(self._update_food_list)
        filter_layout.addWidget(self.category_combo)
        
        main_layout.addLayout(filter_layout)
        
        # Splitter for foods list and selected foods
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Foods list (left side)
        foods_group = QGroupBox("Available Foods")
        foods_layout = QVBoxLayout()
        
        self.foods_table = QTableWidget()
        self.foods_table.setColumnCount(5)
        self.foods_table.setHorizontalHeaderLabels(["Food", "Calories", "Protein", "Carbs", "Fat"])
        self.foods_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.foods_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.foods_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.foods_table.cellDoubleClicked.connect(self._add_selected_food)
        
        foods_layout.addWidget(self.foods_table)
        
        add_btn = QPushButton("Add Selected Food")
        add_btn.clicked.connect(self._add_selected_food)
        foods_layout.addWidget(add_btn)
        
        foods_group.setLayout(foods_layout)
        splitter.addWidget(foods_group)
        
        # Selected foods (right side)
        selected_group = QGroupBox("Selected Foods")
        selected_layout = QVBoxLayout()
        
        self.selected_table = QTableWidget()
        self.selected_table.setColumnCount(6)
        self.selected_table.setHorizontalHeaderLabels(["Food", "Quantity", "Calories", "Protein", "Carbs", "Fat"])
        self.selected_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        
        selected_layout.addWidget(self.selected_table)
        
        remove_btn = QPushButton("Remove Selected Food")
        remove_btn.clicked.connect(self._remove_selected_food)
        selected_layout.addWidget(remove_btn)
        
        selected_group.setLayout(selected_layout)
        splitter.addWidget(selected_group)
        
        # Set default sizes (60% left, 40% right)
        splitter.setSizes([480, 320])
        
        main_layout.addWidget(splitter)
        
        # Food details panel
        details_group = QGroupBox("Food Details")
        details_layout = QHBoxLayout()
        
        # Nutritional info
        nutrition_layout = QFormLayout()
        
        self.food_name_label = QLabel("No food selected")
        self.food_name_label.setStyleSheet("font-weight: bold;")
        nutrition_layout.addRow("Food:", self.food_name_label)
        
        self.food_category_label = QLabel("-")
        nutrition_layout.addRow("Category:", self.food_category_label)
        
        self.food_calories_label = QLabel("-")
        nutrition_layout.addRow("Calories:", self.food_calories_label)
        
        self.food_protein_label = QLabel("-")
        nutrition_layout.addRow("Protein:", self.food_protein_label)
        
        self.food_carbs_label = QLabel("-")
        nutrition_layout.addRow("Carbohydrates:", self.food_carbs_label)
        
        self.food_fat_label = QLabel("-")
        nutrition_layout.addRow("Fat:", self.food_fat_label)
        
        details_layout.addLayout(nutrition_layout)
        
        # Quantity selector
        quantity_layout = QFormLayout()
        
        self.quantity_spin = QDoubleSpinBox()
        self.quantity_spin.setRange(0.1, 10.0)
        self.quantity_spin.setSingleStep(0.5)
        self.quantity_spin.setValue(1.0)
        self.quantity_spin.setDecimals(1)
        quantity_layout.addRow("Quantity:", self.quantity_spin)
        
        self.serving_size_label = QLabel("-")
        quantity_layout.addRow("Serving Size:", self.serving_size_label)
        
        details_layout.addLayout(quantity_layout)
        
        details_group.setLayout(details_layout)
        main_layout.addWidget(details_group)
        
        # Bottom buttons
        buttons_layout = QHBoxLayout()
        
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(ok_btn)
        
        main_layout.addLayout(buttons_layout)
        
        # Connect signals
        self.foods_table.itemSelectionChanged.connect(self._update_food_details)
    
    def _populate_categories(self):
        """Populate the category dropdown with available categories"""
        categories = self.food_database.get_categories()
        for category in sorted(categories):
            formatted_category = category.replace("_", " ").title()
            self.category_combo.addItem(formatted_category, category)
    
    def _update_food_list(self):
        """Update the food list based on search and filter criteria"""
        search_query = self.search_input.text().strip()
        
        category_index = self.category_combo.currentIndex()
        if category_index == 0:  # "All Categories"
            category = None
        else:
            category = self.category_combo.itemData(category_index)
        
        # Get matching foods
        if category:
            foods = self.food_database.get_foods_by_category(category)
        else:
            foods = []
            for cat in self.food_database.get_categories():
                foods.extend(self.food_database.get_foods_by_category(cat))
        
        # Filter by search query if needed
        if search_query:
            foods = [f for f in foods if search_query.lower() in f["name"].lower()]
        
        # Update the table
        self.foods_table.setRowCount(len(foods))
        
        for i, food in enumerate(foods):
            # Food name
            name_item = QTableWidgetItem(food["name"])
            name_item.setData(Qt.ItemDataRole.UserRole, food["id"])
            self.foods_table.setItem(i, 0, name_item)
            
            # Calories
            calories = food["nutrients"].get("calories", 0)
            calories_item = QTableWidgetItem(f"{calories:.0f} kcal")
            self.foods_table.setItem(i, 1, calories_item)
            
            # Protein
            protein = food["nutrients"].get("protein", 0)
            protein_item = QTableWidgetItem(f"{protein:.1f} g")
            self.foods_table.setItem(i, 2, protein_item)
            
            # Carbs
            carbs = food["nutrients"].get("carbohydrates", 0)
            carbs_item = QTableWidgetItem(f"{carbs:.1f} g")
            self.foods_table.setItem(i, 3, carbs_item)
            
            # Fat
            fat = food["nutrients"].get("fat", 0)
            fat_item = QTableWidgetItem(f"{fat:.1f} g")
            self.foods_table.setItem(i, 4, fat_item)
        
        # Clear selection and details
        self.foods_table.clearSelection()
        self._clear_food_details()
    
    def _update_food_details(self):
        """Update the food details panel with the selected food"""
        selected_rows = self.foods_table.selectedItems()
        if not selected_rows:
            self._clear_food_details()
            return
        
        # Get the food ID from the first column
        food_id = self.foods_table.item(selected_rows[0].row(), 0).data(Qt.ItemDataRole.UserRole)
        food = self.food_database.get_food(food_id)
        
        if not food:
            self._clear_food_details()
            return
        
        # Update labels
        self.food_name_label.setText(food["name"])
        self.food_category_label.setText(food["category"].replace("_", " ").title())
        
        self.food_calories_label.setText(f"{food['nutrients'].get('calories', 0):.0f} kcal")
        self.food_protein_label.setText(f"{food['nutrients'].get('protein', 0):.1f} g")
        self.food_carbs_label.setText(f"{food['nutrients'].get('carbohydrates', 0):.1f} g")
        self.food_fat_label.setText(f"{food['nutrients'].get('fat', 0):.1f} g")
        
        self.serving_size_label.setText(f"{food['serving_size']} ({food['serving_unit']})")
    
    def _clear_food_details(self):
        """Clear the food details panel"""
        self.food_name_label.setText("No food selected")
        self.food_category_label.setText("-")
        self.food_calories_label.setText("-")
        self.food_protein_label.setText("-")
        self.food_carbs_label.setText("-")
        self.food_fat_label.setText("-")
        self.serving_size_label.setText("-")
    
    def _add_selected_food(self):
        """Add the selected food to the selected foods list"""
        selected_rows = self.foods_table.selectedItems()
        if not selected_rows:
            return
        
        # Get the food ID from the first column
        food_id = self.foods_table.item(selected_rows[0].row(), 0).data(Qt.ItemDataRole.UserRole)
        food = self.food_database.get_food(food_id)
        
        if not food:
            return
        
        # Get quantity
        quantity = self.quantity_spin.value()
        
        # Add to selected foods
        self.selected_foods.append({
            "food": food,
            "quantity": quantity
        })
        
        # Update selected foods table
        self._update_selected_foods_table()
    
    def _remove_selected_food(self):
        """Remove the selected food from the selected foods list"""
        selected_rows = self.selected_table.selectedItems()
        if not selected_rows:
            return
        
        # Get the index from the selected row
        index = selected_rows[0].row()
        if 0 <= index < len(self.selected_foods):
            self.selected_foods.pop(index)
            self._update_selected_foods_table()
    
    def _update_selected_foods_table(self):
        """Update the selected foods table"""
        self.selected_table.setRowCount(len(self.selected_foods))
        
        for i, food_data in enumerate(self.selected_foods):
            food = food_data["food"]
            quantity = food_data["quantity"]
            
            # Food name
            name_item = QTableWidgetItem(food["name"])
            self.selected_table.setItem(i, 0, name_item)
            
            # Quantity
            quantity_text = f"{quantity} {food['serving_unit']}"
            quantity_item = QTableWidgetItem(quantity_text)
            self.selected_table.setItem(i, 1, quantity_item)
            
            # Calculate scaled nutrients
            calories = food["nutrients"].get("calories", 0) * quantity
            protein = food["nutrients"].get("protein", 0) * quantity
            carbs = food["nutrients"].get("carbohydrates", 0) * quantity
            fat = food["nutrients"].get("fat", 0) * quantity
            
            # Calories
            calories_item = QTableWidgetItem(f"{calories:.0f} kcal")
            self.selected_table.setItem(i, 2, calories_item)
            
            # Protein
            protein_item = QTableWidgetItem(f"{protein:.1f} g")
            self.selected_table.setItem(i, 3, protein_item)
            
            # Carbs
            carbs_item = QTableWidgetItem(f"{carbs:.1f} g")
            self.selected_table.setItem(i, 4, carbs_item)
            
            # Fat
            fat_item = QTableWidgetItem(f"{fat:.1f} g")
            self.selected_table.setItem(i, 5, fat_item)
    
    def get_selected_foods(self):
        """Get the list of selected foods"""
        return self.selected_foods
