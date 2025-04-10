"""
Meal plan model for storing generated meal plans
"""
import json
import os
import uuid
from datetime import datetime

class MealPlan:
    """Meal Plan class to store meal recommendations and nutritional data"""
    
    def __init__(self, user_id, plan_id=None):
        """Initialize meal plan"""
        self.plan_id = plan_id if plan_id else str(uuid.uuid4())
        self.user_id = user_id
        self.created_at = datetime.now().isoformat()
        self.name = f"Meal Plan {datetime.now().strftime('%Y-%m-%d')}"
        self.description = "Custom meal plan"
        self.days = 1  # Number of days in the plan
        self.meals = []  # List of meals
        self.nutritional_summary = {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0,
            "vitamins": {},
            "minerals": {}
        }
        self.daily_targets = {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0
        }
    
    def add_meal(self, meal_type, day=1):
        """Add a new meal to the plan"""
        meal = {
            "id": str(uuid.uuid4()),
            "day": day,
            "type": meal_type,  # breakfast, lunch, dinner, snack
            "foods": [],
            "nutrients": {
                "calories": 0,
                "protein": 0,
                "carbs": 0,
                "fat": 0,
                "fiber": 0
            }
        }
        self.meals.append(meal)
        return meal["id"]
    
    def add_food_to_meal(self, meal_id, food_item, quantity=1.0):
        """Add a food item to a meal"""
        for meal in self.meals:
            if meal["id"] == meal_id:
                # Calculate scaled nutrients based on quantity
                scaled_nutrients = {}
                for nutrient, value in food_item["nutrients"].items():
                    scaled_nutrients[nutrient] = value * quantity
                
                # Add food to meal
                meal["foods"].append({
                    "id": food_item["id"],
                    "name": food_item["name"],
                    "quantity": quantity,
                    "serving_size": food_item["serving_size"],
                    "serving_unit": food_item["serving_unit"],
                    "nutrients": scaled_nutrients
                })
                
                # Update meal nutrients
                meal["nutrients"]["calories"] += scaled_nutrients.get("calories", 0)
                meal["nutrients"]["protein"] += scaled_nutrients.get("protein", 0)
                meal["nutrients"]["carbs"] += scaled_nutrients.get("carbohydrates", 0)
                meal["nutrients"]["fat"] += scaled_nutrients.get("fat", 0)
                meal["nutrients"]["fiber"] += scaled_nutrients.get("fiber", 0)
                
                self._update_nutritional_summary()
                return True
        
        return False
    
    def remove_food_from_meal(self, meal_id, food_index):
        """Remove a food item from a meal"""
        for meal in self.meals:
            if meal["id"] == meal_id and 0 <= food_index < len(meal["foods"]):
                food = meal["foods"][food_index]
                
                # Subtract nutrients from meal
                for nutrient in ["calories", "protein", "carbs", "fat", "fiber"]:
                    meal["nutrients"][nutrient] -= food["nutrients"].get(
                        "carbohydrates" if nutrient == "carbs" else nutrient, 0
                    )
                
                # Remove food
                meal["foods"].pop(food_index)
                self._update_nutritional_summary()
                return True
        
        return False
    
    def remove_meal(self, meal_id):
        """Remove a meal from the plan"""
        for i, meal in enumerate(self.meals):
            if meal["id"] == meal_id:
                self.meals.pop(i)
                self._update_nutritional_summary()
                return True
        
        return False
    
    def _update_nutritional_summary(self):
        """Update the overall nutritional summary of the meal plan"""
        summary = {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0,
            "vitamins": {},
            "minerals": {}
        }
        
        # Sum up nutrients from all meals
        for meal in self.meals:
            summary["calories"] += meal["nutrients"]["calories"]
            summary["protein"] += meal["nutrients"]["protein"]
            summary["carbs"] += meal["nutrients"]["carbs"]
            summary["fat"] += meal["nutrients"]["fat"]
            summary["fiber"] += meal["nutrients"]["fiber"]
            
            # Process foods to collect vitamin and mineral data
            for food in meal["foods"]:
                for nutrient, value in food["nutrients"].items():
                    # Skip macronutrients already handled above
                    if nutrient in ["calories", "protein", "carbohydrates", "fat", "fiber"]:
                        continue
                    
                    # Categorize as vitamin or mineral (simplified)
                    if nutrient.startswith(("vitamin", "vit_")):
                        if nutrient not in summary["vitamins"]:
                            summary["vitamins"][nutrient] = 0
                        summary["vitamins"][nutrient] += value
                    elif nutrient in ["calcium", "iron", "magnesium", "sodium", "potassium", "zinc"]:
                        if nutrient not in summary["minerals"]:
                            summary["minerals"][nutrient] = 0
                        summary["minerals"][nutrient] += value
        
        self.nutritional_summary = summary
    
    def calculate_completion_percentage(self):
        """Calculate how well the meal plan meets nutritional targets"""
        if not any(self.daily_targets.values()):
            return 0
        
        percentages = []
        for nutrient in ["calories", "protein", "carbs", "fat", "fiber"]:
            target = self.daily_targets.get(nutrient, 0)
            if target > 0:
                actual = self.nutritional_summary.get(nutrient, 0)
                # Cap at 100% to avoid over-consumption skewing results
                percent = min(100, (actual / target) * 100)
                percentages.append(percent)
        
        if not percentages:
            return 0
            
        return sum(percentages) / len(percentages)
    
    def to_dict(self):
        """Convert meal plan to dictionary for serialization"""
        return {
            "plan_id": self.plan_id,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "name": self.name,
            "description": self.description,
            "days": self.days,
            "meals": self.meals,
            "nutritional_summary": self.nutritional_summary,
            "daily_targets": self.daily_targets
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create meal plan from dictionary"""
        plan = cls(
            user_id=data["user_id"],
            plan_id=data.get("plan_id")
        )
        plan.created_at = data.get("created_at", plan.created_at)
        plan.name = data.get("name", plan.name)
        plan.description = data.get("description", plan.description)
        plan.days = data.get("days", plan.days)
        plan.meals = data.get("meals", plan.meals)
        plan.nutritional_summary = data.get("nutritional_summary", plan.nutritional_summary)
        plan.daily_targets = data.get("daily_targets", plan.daily_targets)
        
        return plan
    
    def save(self):
        """Save meal plan to JSON file"""
        plans_dir = os.path.join(os.path.expanduser("~"), ".nutrition_planner", "meal_plans")
        os.makedirs(plans_dir, exist_ok=True)
        
        file_path = os.path.join(plans_dir, f"{self.plan_id}.json")
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, plan_id):
        """Load meal plan from JSON file"""
        file_path = os.path.join(os.path.expanduser("~"), ".nutrition_planner", "meal_plans", f"{plan_id}.json")
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return cls.from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    @classmethod
    def get_user_plans(cls, user_id):
        """Get all meal plans for a user"""
        plans_dir = os.path.join(os.path.expanduser("~"), ".nutrition_planner", "meal_plans")
        os.makedirs(plans_dir, exist_ok=True)
        
        plans = []
        for filename in os.listdir(plans_dir):
            if filename.endswith(".json"):
                plan_id = filename.replace(".json", "")
                plan = cls.load(plan_id)
                if plan and plan.user_id == user_id:
                    plans.append(plan)
        
        # Sort by creation date (newest first)
        plans.sort(key=lambda p: p.created_at, reverse=True)
        return plans
