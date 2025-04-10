"""
Report generator service for creating nutrition reports and summaries
"""
import os
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
import numpy as np
import pandas as pd

class ReportGenerator:
    """Report generator to create nutrition reports and visualizations"""
    
    def __init__(self):
        """Initialize report generator"""
        # Set matplotlib to use a non-interactive backend
        matplotlib.use('Agg')
    
    def generate_meal_plan_summary(self, meal_plan, nutrition_targets):
        """
        Generate a summary of the meal plan
        Returns a dictionary with summary statistics and metrics
        """
        # Get nutritional data from meal plan
        current = meal_plan.nutritional_summary
        
        # Calculate percentages of targets met
        summary = {
            "plan_id": meal_plan.plan_id,
            "plan_name": meal_plan.name,
            "created_at": meal_plan.created_at,
            "total_meals": len(meal_plan.meals),
            "meal_types": list(set(meal["type"] for meal in meal_plan.meals)),
            "total_foods": sum(len(meal["foods"]) for meal in meal_plan.meals),
            "nutrient_summary": {},
            "completion_percentage": meal_plan.calculate_completion_percentage()
        }
        
        # Calculate nutrient percentages
        for nutrient in ["calories", "protein", "carbs", "fat", "fiber"]:
            target_value = nutrition_targets.get(nutrient, 0)
            current_value = current.get(nutrient, 0)
            
            if target_value > 0:
                percentage = (current_value / target_value) * 100
                summary["nutrient_summary"][nutrient] = {
                    "target": round(target_value, 1),
                    "actual": round(current_value, 1),
                    "percentage": round(percentage, 1),
                    "status": self._get_status(percentage)
                }
        
        return summary
    
    def _get_status(self, percentage):
        """Determine status based on percentage of target met"""
        if percentage < 70:
            return "deficient"
        elif percentage < 90:
            return "below_target"
        elif percentage <= 110:
            return "on_target"
        elif percentage <= 130:
            return "above_target"
        else:
            return "excess"
    
    def generate_macronutrient_chart(self, meal_plan, file_name="macronutrients.png"):
        """
        Generate a pie chart showing macronutrient distribution
        Returns the file path of the generated chart
        """
        # Create directory for reports
        reports_dir = os.path.join(os.path.expanduser("~"), ".nutrition_planner", "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        # Get macronutrient data
        nutrients = meal_plan.nutritional_summary
        protein_calories = nutrients.get("protein", 0) * 4  # 4 calories per gram
        carbs_calories = nutrients.get("carbs", 0) * 4      # 4 calories per gram
        fat_calories = nutrients.get("fat", 0) * 9          # 9 calories per gram
        
        total_calories = protein_calories + carbs_calories + fat_calories
        if total_calories == 0:
            total_calories = 1  # Prevent division by zero
        
        # Calculate percentages
        protein_pct = (protein_calories / total_calories) * 100
        carbs_pct = (carbs_calories / total_calories) * 100
        fat_pct = (fat_calories / total_calories) * 100
        
        # Create pie chart
        labels = ['Protein', 'Carbohydrates', 'Fat']
        sizes = [protein_pct, carbs_pct, fat_pct]
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        explode = (0.1, 0, 0)  # explode 1st slice (Protein)
        
        plt.figure(figsize=(10, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title(f'Macronutrient Distribution for {meal_plan.name}')
        
        # Add legend with gram values
        legend_labels = [
            f'Protein: {nutrients.get("protein", 0):.1f}g ({protein_pct:.1f}%)',
            f'Carbs: {nutrients.get("carbs", 0):.1f}g ({carbs_pct:.1f}%)',
            f'Fat: {nutrients.get("fat", 0):.1f}g ({fat_pct:.1f}%)'
        ]
        plt.legend(legend_labels, loc="best")
        
        # Save the chart
        file_path = os.path.join(reports_dir, file_name)
        plt.savefig(file_path)
        plt.close()
        
        return file_path
    
    def generate_nutrient_targets_chart(self, meal_plan, nutrition_targets, file_name="nutrient_targets.png"):
        """
        Generate a bar chart comparing actual nutrient intake to targets
        Returns the file path of the generated chart
        """
        # Create directory for reports
        reports_dir = os.path.join(os.path.expanduser("~"), ".nutrition_planner", "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        # Get nutrient data
        nutrients = ["calories", "protein", "carbs", "fat", "fiber"]
        target_values = [nutrition_targets.get(n, 0) for n in nutrients]
        actual_values = [meal_plan.nutritional_summary.get(n, 0) for n in nutrients]
        
        # Create percentage data
        percentages = []
        for i, target in enumerate(target_values):
            if target > 0:
                percentages.append(min(150, (actual_values[i] / target) * 100))
            else:
                percentages.append(0)
        
        # Create bar chart
        bar_width = 0.35
        index = np.arange(len(nutrients))
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create target bars (100%)
        target_bars = ax.bar(index, [100] * len(nutrients), bar_width,
                             label='Target (100%)', color='lightgray')
        
        # Create actual bars with color based on percentage
        colors = []
        for pct in percentages:
            if pct < 70:
                colors.append('#ff9999')  # red - deficient
            elif pct < 90:
                colors.append('#ffcc99')  # orange - below target
            elif pct <= 110:
                colors.append('#99ff99')  # green - on target
            elif pct <= 130:
                colors.append('#ffff99')  # yellow - above target
            else:
                colors.append('#ff9999')  # red - excess
        
        actual_bars = ax.bar(index + bar_width, percentages, bar_width,
                             label='Actual (%)', color=colors)
        
        # Add labels and formatting
        ax.set_xlabel('Nutrients')
        ax.set_ylabel('Percentage of Target (%)')
        ax.set_title(f'Nutrient Targets vs. Actual for {meal_plan.name}')
        ax.set_xticks(index + bar_width / 2)
        
        # Format x-tick labels with actual values
        x_tick_labels = []
        for i, nutrient in enumerate(nutrients):
            label = nutrient.capitalize()
            if nutrient == "calories":
                unit = "kcal"
            else:
                unit = "g"
            label += f"\nTarget: {target_values[i]:.1f}{unit}"
            label += f"\nActual: {actual_values[i]:.1f}{unit}"
            x_tick_labels.append(label)
        
        ax.set_xticklabels(x_tick_labels)
        
        # Add a horizontal line at 100%
        ax.axhline(y=100, color='black', linestyle='--', alpha=0.3)
        
        # Add percentages on top of the bars
        for i, pct in enumerate(percentages):
            ax.text(index[i] + bar_width * 1.5, pct + 3, f'{pct:.1f}%', 
                    ha='center', va='bottom', fontsize=9)
        
        ax.legend()
        
        # Set y-axis limit with some headroom
        ax.set_ylim(0, max(max(percentages) + 20, 120))
        
        # Save the chart
        file_path = os.path.join(reports_dir, file_name)
        plt.savefig(file_path)
        plt.close()
        
        return file_path
    
    def generate_meal_distribution_chart(self, meal_plan, file_name="meal_distribution.png"):
        """
        Generate a bar chart showing calorie distribution across meals
        Returns the file path of the generated chart
        """
        # Create directory for reports
        reports_dir = os.path.join(os.path.expanduser("~"), ".nutrition_planner", "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        # Group meals by type and calculate calories
        meal_types = {}
        for meal in meal_plan.meals:
            meal_type = meal["type"]
            calories = meal["nutrients"]["calories"]
            
            if meal_type not in meal_types:
                meal_types[meal_type] = 0
            meal_types[meal_type] += calories
        
        # Convert to lists for plotting
        types = list(meal_types.keys())
        calories = list(meal_types.values())
        
        # Calculate percentages
        total_calories = sum(calories)
        percentages = [(c / total_calories) * 100 if total_calories > 0 else 0 for c in calories]
        
        # Sort by meal order
        meal_order = ["breakfast", "morning_snack", "lunch", "afternoon_snack", "dinner", "evening_snack"]
        sorted_data = []
        
        for meal_type in meal_order:
            if meal_type in meal_types:
                index = types.index(meal_type)
                sorted_data.append((meal_type, calories[index], percentages[index]))
        
        # For any meal types not in the standard order
        for i, meal_type in enumerate(types):
            if meal_type not in meal_order:
                sorted_data.append((meal_type, calories[i], percentages[i]))
        
        # Unpack sorted data
        types = [item[0] for item in sorted_data]
        calories = [item[1] for item in sorted_data]
        percentages = [item[2] for item in sorted_data]
        
        # Create better labels
        labels = [t.replace('_', ' ').title() for t in types]
        
        # Create bar chart
        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, calories, color='skyblue')
        
        # Add values on top of bars
        for i, (bar, pct) in enumerate(zip(bars, percentages)):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 20,
                     f'{calories[i]:.0f} cal ({pct:.1f}%)',
                     ha='center', va='bottom', fontsize=9)
        
        plt.xlabel('Meal Type')
        plt.ylabel('Calories')
        plt.title(f'Calorie Distribution Across Meals for {meal_plan.name}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the chart
        file_path = os.path.join(reports_dir, file_name)
        plt.savefig(file_path)
        plt.close()
        
        return file_path
    
    def generate_full_report(self, meal_plan, nutrition_targets, user_profile=None):
        """
        Generate a complete nutrition report including all charts and summary
        Returns a dictionary with report data and chart file paths
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_id = f"report_{timestamp}"
        
        report = {
            "report_id": report_id,
            "timestamp": datetime.now().isoformat(),
            "meal_plan_id": meal_plan.plan_id,
            "meal_plan_name": meal_plan.name,
            "summary": self.generate_meal_plan_summary(meal_plan, nutrition_targets),
            "charts": {}
        }
        
        # Generate charts with unique filenames based on report_id
        report["charts"]["macronutrients"] = self.generate_macronutrient_chart(
            meal_plan, f"{report_id}_macronutrients.png"
        )
        
        report["charts"]["nutrient_targets"] = self.generate_nutrient_targets_chart(
            meal_plan, nutrition_targets, f"{report_id}_nutrient_targets.png"
        )
        
        report["charts"]["meal_distribution"] = self.generate_meal_distribution_chart(
            meal_plan, f"{report_id}_meal_distribution.png"
        )
        
        # Add user profile data if provided
        if user_profile:
            report["user"] = {
                "name": user_profile.name,
                "age": user_profile.age,
                "gender": user_profile.gender,
                "weight": user_profile.weight,
                "height": user_profile.height,
                "bmi": user_profile.calculate_bmi(),
                "bmi_category": user_profile.get_bmi_category(),
                "diet_type": user_profile.diet_type,
                "activity_level": user_profile.activity_level
            }
        
        return report
    
    def generate_food_category_distribution(self, meal_plan, file_name="food_categories.png"):
        """
        Generate a chart showing distribution of food categories in the meal plan
        Returns the file path of the generated chart
        """
        # Create directory for reports
        reports_dir = os.path.join(os.path.expanduser("~"), ".nutrition_planner", "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        # Collect all food categories
        categories = {}
        
        for meal in meal_plan.meals:
            for food in meal["foods"]:
                category = food.get("category", "Other")
                if category not in categories:
                    categories[category] = 0
                categories[category] += 1
        
        # Create chart
        plt.figure(figsize=(10, 6))
        
        # Sort categories by count
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        labels = [item[0].replace('_', ' ').title() for item in sorted_categories]
        counts = [item[1] for item in sorted_categories]
        
        # Create pie chart
        plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90,
                shadow=True, wedgeprops={'edgecolor': 'black'})
        
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title(f'Food Category Distribution for {meal_plan.name}')
        
        # Save the chart
        file_path = os.path.join(reports_dir, file_name)
        plt.savefig(file_path)
        plt.close()
        
        return file_path
