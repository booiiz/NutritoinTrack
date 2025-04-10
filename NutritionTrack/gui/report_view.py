"""
Report view for displaying nutrition reports and visualizations
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QGroupBox, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QSplitter, QSizePolicy, QFileDialog
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap

class ReportView(QWidget):
    """Widget for displaying nutrition reports and visualizations"""
    
    def __init__(self):
        super().__init__()
        
        self.report = None
        
        # Initialize UI
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Title and action bar
        title_bar = QHBoxLayout()
        
        self.title_label = QLabel("Nutrition Report")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        title_bar.addWidget(self.title_label)
        
        title_bar.addStretch()
        
        self.export_btn = QPushButton("Export Report")
        self.export_btn.clicked.connect(self._export_report)
        title_bar.addWidget(self.export_btn)
        
        main_layout.addLayout(title_bar)
        
        # Create scroll area for report content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # Create scroll content widget
        self.report_content = QWidget()
        scroll_area.setWidget(self.report_content)
        
        # Layout for report content
        self.report_layout = QVBoxLayout(self.report_content)
        
        # Add scroll area to main layout
        main_layout.addWidget(scroll_area)
    
    def set_report(self, report):
        """Set the report to display"""
        self.report = report
        
        # Update UI with report data
        self._update_display()
    
    def _update_display(self):
        """Update the display with current report data"""
        if not self.report:
            return
        
        # Clear previous content
        self._clear_report_content()
        
        # Update title
        self.title_label.setText(f"Nutrition Report: {self.report.get('meal_plan_name', 'Meal Plan')}")
        
        # Add user information if available
        if "user" in self.report:
            self._add_user_info_section()
        
        # Add summary section
        self._add_summary_section()
        
        # Add charts
        self._add_charts_section()
        
        # Add recommendations section
        self._add_recommendations_section()
        
        # Add meals overview
        self._add_meals_overview_section()
    
    def _clear_report_content(self):
        """Clear all widgets from the report layout"""
        while self.report_layout.count():
            item = self.report_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def _add_user_info_section(self):
        """Add user information section to the report"""
        user = self.report.get("user", {})
        if not user:
            return
        
        # Create group box
        user_group = QGroupBox("User Information")
        user_layout = QFormLayout()
        
        # Add user details
        name_label = QLabel(user.get("name", "-"))
        user_layout.addRow("Name:", name_label)
        
        age_gender = f"{user.get('age', '-')} years, {user.get('gender', '-').title()}"
        age_gender_label = QLabel(age_gender)
        user_layout.addRow("Age & Gender:", age_gender_label)
        
        height_weight = f"{user.get('height', '-')} cm, {user.get('weight', '-')} kg"
        height_weight_label = QLabel(height_weight)
        user_layout.addRow("Height & Weight:", height_weight_label)
        
        bmi_label = QLabel(f"{user.get('bmi', '-'):.1f} ({user.get('bmi_category', '-')})")
        user_layout.addRow("BMI:", bmi_label)
        
        diet_label = QLabel(user.get('diet_type', '-').title())
        user_layout.addRow("Diet Type:", diet_label)
        
        activity_label = QLabel(user.get('activity_level', '-').replace('_', ' ').title())
        user_layout.addRow("Activity Level:", activity_label)
        
        user_group.setLayout(user_layout)
        self.report_layout.addWidget(user_group)
    
    def _add_summary_section(self):
        """Add nutritional summary section to the report"""
        summary = self.report.get("summary", {})
        if not summary:
            return
        
        # Create group box
        summary_group = QGroupBox("Nutritional Summary")
        summary_layout = QVBoxLayout()
        
        # Add completion percentage
        completion = summary.get("completion_percentage", 0)
        completion_label = QLabel(f"Overall Plan Completion: {completion:.1f}%")
        completion_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        completion_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(completion_label)
        
        # Add nutrient summary table
        nutrient_summary = QTableWidget()
        nutrient_summary.setColumnCount(4)
        nutrient_summary.setHorizontalHeaderLabels(["Nutrient", "Target", "Actual", "% of Target"])
        nutrient_summary.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        nutrient_data = summary.get("nutrient_summary", {})
        nutrient_summary.setRowCount(len(nutrient_data))
        
        for i, (nutrient, data) in enumerate(nutrient_data.items()):
            # Nutrient name
            name_item = QTableWidgetItem(nutrient.capitalize())
            nutrient_summary.setItem(i, 0, name_item)
            
            # Target
            target = data.get("target", 0)
            unit = "kcal" if nutrient == "calories" else "g"
            target_item = QTableWidgetItem(f"{target:.1f} {unit}")
            nutrient_summary.setItem(i, 1, target_item)
            
            # Actual
            actual = data.get("actual", 0)
            actual_item = QTableWidgetItem(f"{actual:.1f} {unit}")
            nutrient_summary.setItem(i, 2, actual_item)
            
            # Percentage
            percentage = data.get("percentage", 0)
            percentage_item = QTableWidgetItem(f"{percentage:.1f}%")
            
            # Color code based on status
            status = data.get("status", "")
            if status == "deficient":
                percentage_item.setBackground(Qt.GlobalColor.red)
                percentage_item.setForeground(Qt.GlobalColor.white)
            elif status == "below_target":
                percentage_item.setBackground(Qt.GlobalColor.yellow)
            elif status == "on_target":
                percentage_item.setBackground(Qt.GlobalColor.green)
            elif status == "above_target":
                percentage_item.setBackground(Qt.GlobalColor.cyan)
            elif status == "excess":
                percentage_item.setBackground(Qt.GlobalColor.magenta)
            
            nutrient_summary.setItem(i, 3, percentage_item)
        
        summary_layout.addWidget(nutrient_summary)
        
        # Add meal stats
        meal_stats_label = QLabel(
            f"<b>Meal Statistics:</b> {summary.get('total_meals', 0)} meals with "
            f"{summary.get('total_foods', 0)} total food items"
        )
        meal_stats_label.setTextFormat(Qt.TextFormat.RichText)
        summary_layout.addWidget(meal_stats_label)
        
        summary_group.setLayout(summary_layout)
        self.report_layout.addWidget(summary_group)
    
    def _add_charts_section(self):
        """Add charts section to the report"""
        charts = self.report.get("charts", {})
        if not charts:
            return
        
        # Create group box
        charts_group = QGroupBox("Nutritional Analysis")
        charts_layout = QVBoxLayout()
        
        # Add macronutrient distribution chart
        if "macronutrients" in charts:
            macro_label = QLabel("Macronutrient Distribution")
            macro_label.setStyleSheet("font-weight: bold;")
            macro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            charts_layout.addWidget(macro_label)
            
            macro_pixmap = QPixmap(charts["macronutrients"])
            macro_img = QLabel()
            macro_img.setPixmap(macro_pixmap)
            macro_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
            charts_layout.addWidget(macro_img)
        
        # Add nutrient targets chart
        if "nutrient_targets" in charts:
            targets_label = QLabel("Nutrient Targets vs. Actual")
            targets_label.setStyleSheet("font-weight: bold;")
            targets_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            charts_layout.addWidget(targets_label)
            
            targets_pixmap = QPixmap(charts["nutrient_targets"])
            targets_img = QLabel()
            targets_img.setPixmap(targets_pixmap)
            targets_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
            charts_layout.addWidget(targets_img)
        
        # Add meal distribution chart
        if "meal_distribution" in charts:
            meal_label = QLabel("Calorie Distribution Across Meals")
            meal_label.setStyleSheet("font-weight: bold;")
            meal_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            charts_layout.addWidget(meal_label)
            
            meal_pixmap = QPixmap(charts["meal_distribution"])
            meal_img = QLabel()
            meal_img.setPixmap(meal_pixmap)
            meal_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
            charts_layout.addWidget(meal_img)
        
        charts_group.setLayout(charts_layout)
        self.report_layout.addWidget(charts_group)
    
    def _add_recommendations_section(self):
        """Add recommendations section to the report"""
        summary = self.report.get("summary", {})
        nutrient_data = summary.get("nutrient_summary", {})
        
        if not nutrient_data:
            return
        
        # Create group box
        recommendations_group = QGroupBox("Recommendations")
        recommendations_layout = QVBoxLayout()
        
        # Generate recommendations based on nutrient data
        recommendations = []
        
        for nutrient, data in nutrient_data.items():
            status = data.get("status", "")
            percentage = data.get("percentage", 0)
            
            if status == "deficient":
                if nutrient == "calories":
                    recommendations.append(
                        "Increase your overall calorie intake. Consider adding more energy-dense "
                        "foods like nuts, seeds, avocados, and healthy oils."
                    )
                elif nutrient == "protein":
                    recommendations.append(
                        "Increase your protein intake. Good sources include lean meats, fish, eggs, "
                        "dairy, legumes, tofu, and plant-based protein powders."
                    )
                elif nutrient == "carbs":
                    recommendations.append(
                        "Increase your carbohydrate intake. Focus on complex carbs like whole grains, "
                        "starchy vegetables, fruits, and legumes."
                    )
                elif nutrient == "fat":
                    recommendations.append(
                        "Increase your healthy fat intake. Good sources include avocados, nuts, seeds, "
                        "olive oil, and fatty fish."
                    )
                elif nutrient == "fiber":
                    recommendations.append(
                        "Increase your fiber intake. Good sources include whole grains, fruits, vegetables, "
                        "legumes, nuts, and seeds."
                    )
            elif status == "excess":
                if nutrient == "calories":
                    recommendations.append(
                        "Reduce your overall calorie intake. Focus on nutrient-dense, lower-calorie foods "
                        "like vegetables, fruits, lean proteins, and whole grains."
                    )
                elif nutrient == "fat":
                    recommendations.append(
                        "Reduce your fat intake, particularly saturated and trans fats. Limit fried foods, "
                        "fatty meats, full-fat dairy, and processed foods."
                    )
        
        # Add general recommendations if none are specific
        if not recommendations:
            if summary.get("completion_percentage", 0) >= 90:
                recommendations.append(
                    "Your meal plan is well-balanced and meets your nutritional requirements. "
                    "Continue with this approach for optimal health."
                )
            else:
                recommendations.append(
                    "Consider adjusting your meal plan to better meet your nutritional targets. "
                    "Focus on adding more variety and balancing your macronutrients."
                )
        
        # Add recommendations to layout
        for i, rec in enumerate(recommendations):
            rec_label = QLabel(f"{i+1}. {rec}")
            rec_label.setWordWrap(True)
            recommendations_layout.addWidget(rec_label)
        
        # Add general nutrition tips
        tips_label = QLabel(
            "<b>General Tips:</b>"
            "<ul>"
            "<li>Stay hydrated by drinking plenty of water throughout the day</li>"
            "<li>Eat a variety of colorful fruits and vegetables for a range of nutrients</li>"
            "<li>Choose whole foods over processed foods when possible</li>"
            "<li>Pay attention to portion sizes to maintain appropriate calorie intake</li>"
            "<li>Consider taking a multivitamin if your diet is restricted</li>"
            "</ul>"
        )
        tips_label.setTextFormat(Qt.TextFormat.RichText)
        tips_label.setWordWrap(True)
        recommendations_layout.addWidget(tips_label)
        
        recommendations_group.setLayout(recommendations_layout)
        self.report_layout.addWidget(recommendations_group)
    
    def _add_meals_overview_section(self):
        """Add meals overview section to the report"""
        # This would typically show a summary of the meals in the plan
        # For simplicity, we'll just add a placeholder message
        meals_group = QGroupBox("Meal Plan Overview")
        meals_layout = QVBoxLayout()
        
        meals_label = QLabel(
            "This report provides an analysis of your current meal plan. For detailed meal "
            "information and food items, please refer to the Meal Plan tab."
        )
        meals_label.setWordWrap(True)
        meals_layout.addWidget(meals_label)
        
        meals_group.setLayout(meals_layout)
        self.report_layout.addWidget(meals_group)
    
    def _export_report(self):
        """Export the report to a file (HTML or PDF)"""
        # For simplicity, we'll just show a message box
        # In a real app, this would generate an HTML or PDF file
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Report", "", "HTML Files (*.html);;PDF Files (*.pdf)"
        )
        
        if not file_path:
            return
        
        # Just a placeholder - in a real app, we would generate the file
        with open(file_path, 'w') as f:
            f.write("<html><body>\n")
            f.write(f"<h1>Nutrition Report: {self.report.get('meal_plan_name', 'Meal Plan')}</h1>\n")
            f.write("<p>This is a placeholder for the exported report.</p>\n")
            f.write("</body></html>\n")
