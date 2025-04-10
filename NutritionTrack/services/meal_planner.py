"""
Meal planner service for generating meal plans based on user profile and constraints
"""
import random
from models.meal_plan import MealPlan
from services.nutrition_calculator import NutritionCalculator

class MealPlanner:
    """Meal planner to generate and customize meal plans"""
    
    def __init__(self, food_database, rule_engine):
        """Initialize meal planner with food database and rule engine"""
        self.food_database = food_database
        self.rule_engine = rule_engine
    
    def generate_meal_plan(self, user_profile, days=1):
        """
        Generate a complete meal plan based on user profile
        Returns a MealPlan object
        """
        # Create a new meal plan
        meal_plan = MealPlan(user_profile.user_id)
        meal_plan.name = f"{user_profile.diet_type.capitalize()} Meal Plan"
        meal_plan.description = f"Custom meal plan based on {user_profile.name}'s profile"
        meal_plan.days = days
        
        # Calculate nutrition targets
        nutrition_targets = NutritionCalculator.calculate_nutrition_targets(user_profile)
        
        # Set daily targets in meal plan
        meal_plan.daily_targets = {
            "calories": nutrition_targets["calories"],
            "protein": nutrition_targets["protein"],
            "carbs": nutrition_targets["carbs"],
            "fat": nutrition_targets["fat"],
            "fiber": nutrition_targets["fiber"]
        }
        
        # Get meal distribution (how to split calories across meals)
        meal_distribution = self._get_meal_distribution(user_profile.meal_count)
        
        # Generate meals for each day
        for day in range(1, days + 1):
            # Create meals for each meal type
            for meal_type, percentage in meal_distribution.items():
                meal_id = meal_plan.add_meal(meal_type, day)
                
                # Calculate target calories for this meal
                meal_calories = nutrition_targets["calories"] * (percentage / 100)
                
                # Generate food items for this meal
                self._generate_meal_foods(
                    meal_plan,
                    meal_id,
                    user_profile,
                    meal_calories,
                    meal_type
                )
        
        return meal_plan
    
    def _get_meal_distribution(self, meal_count):
        """
        Determine how to distribute calories across meals
        Returns dict of meal types and their percentage of daily calories
        """
        if meal_count == 3:
            return {
                "breakfast": 25,
                "lunch": 35,
                "dinner": 40
            }
        elif meal_count == 5:
            return {
                "breakfast": 20,
                "morning_snack": 10,
                "lunch": 30,
                "afternoon_snack": 10,
                "dinner": 30
            }
        elif meal_count == 6:
            return {
                "breakfast": 20,
                "morning_snack": 10,
                "lunch": 25,
                "afternoon_snack": 10,
                "dinner": 25,
                "evening_snack": 10
            }
        else:  # Default to 3 meals
            return {
                "breakfast": 25,
                "lunch": 35,
                "dinner": 40
            }
    
    def _generate_meal_foods(self, meal_plan, meal_id, user_profile, target_calories, meal_type):
        """
        Generate food items for a single meal
        Adds foods to the specified meal in the meal plan
        """
        # Get diet recommendations based on user profile
        diet_recommendations = self.rule_engine.get_recommendations(user_profile)
        
        # Get food categories suitable for this meal type
        suitable_categories = self._get_suitable_categories(meal_type)
        
        # Get serving recommendations from diet rules
        serving_recommendations = {}
        for rec in diet_recommendations:
            if rec["type"] == "diet" and "servings" in rec:
                for serving in rec["servings"]:
                    category = serving["category"]
                    serving_recommendations[category] = serving
        
        # Initialize tracking variables
        current_calories = 0
        added_foods = []
        attempts = 0
        max_attempts = 50  # Prevent infinite loops
        
        # Keep adding foods until we reach target calories or max attempts
        while current_calories < target_calories and attempts < max_attempts:
            attempts += 1
            
            # Choose a food category weighted by how many servings we still need
            category = self._choose_food_category(suitable_categories, serving_recommendations, added_foods)
            
            # Get foods in this category that meet user constraints
            category_foods = self.food_database.get_foods_by_category(category)
            suitable_foods = []
            
            for food in category_foods:
                # Check if food meets dietary constraints
                allowed, _ = self.rule_engine.evaluate_food_constraints(food, user_profile)
                if allowed:
                    suitable_foods.append(food)
            
            if not suitable_foods:
                continue
            
            # Choose a random suitable food
            food = random.choice(suitable_foods)
            
            # Determine appropriate quantity
            calories_needed = target_calories - current_calories
            food_calories = food["nutrients"].get("calories", 0)
            
            if food_calories > 0:
                # Start with a reasonable portion and adjust if necessary
                base_quantity = 1.0
                
                # For small calorie items, increase quantity to be meaningful
                if food_calories < 50:
                    base_quantity = 2.0
                
                # If this would exceed our target by a lot, reduce quantity
                if food_calories * base_quantity > calories_needed * 1.5:
                    base_quantity = max(0.5, calories_needed / food_calories)
                
                # Add the food to the meal
                meal_plan.add_food_to_meal(meal_id, food, quantity=base_quantity)
                
                # Update tracking variables
                current_calories += food_calories * base_quantity
                added_foods.append(food["category"])
            
            # Avoid adding too many of the same category
            if added_foods.count(food["category"]) >= 2:
                suitable_categories = [c for c in suitable_categories if c != food["category"]]
        
        return added_foods
    
    def _get_suitable_categories(self, meal_type):
        """
        Get food categories suitable for a specific meal type
        Returns list of category names
        """
        all_categories = self.food_database.get_categories()
        
        # Define typical categories for each meal type
        meal_type_categories = {
            "breakfast": ["fruits", "grains", "dairy", "proteins"],
            "morning_snack": ["fruits", "dairy", "proteins"],
            "lunch": ["grains", "proteins", "vegetables", "dairy", "fruits"],
            "afternoon_snack": ["fruits", "vegetables", "dairy", "proteins"],
            "dinner": ["proteins", "vegetables", "grains", "dairy"],
            "evening_snack": ["dairy", "fruits", "proteins"]
        }
        
        # Return appropriate categories or all if meal type not recognized
        return meal_type_categories.get(meal_type, all_categories)
    
    def _choose_food_category(self, categories, serving_recommendations, added_foods):
        """
        Choose a food category weighted by serving recommendations and what's already added
        """
        if not categories:
            return None
        
        # Count how many of each category we've already added
        category_counts = {}
        for category in categories:
            category_counts[category] = added_foods.count(category)
        
        # Calculate weights based on how many more servings we need
        weights = {}
        for category in categories:
            recommendation = serving_recommendations.get(category, {})
            min_servings = recommendation.get("min_servings", 1)
            max_servings = recommendation.get("max_servings", 3)
            current_count = category_counts.get(category, 0)
            
            if current_count >= max_servings:
                weights[category] = 0  # Don't add more if we've hit the max
            elif current_count < min_servings:
                weights[category] = 5  # High weight if we're under minimum
            else:
                weights[category] = 2  # Medium weight if we're in the range
        
        # Filter to categories with non-zero weights
        valid_categories = [c for c in categories if weights.get(c, 0) > 0]
        
        if not valid_categories:
            # If no valid categories based on weights, just return a random one
            return random.choice(categories)
        
        # Choose a category based on weights
        total_weight = sum(weights.get(c, 1) for c in valid_categories)
        r = random.uniform(0, total_weight)
        cumulative_weight = 0
        
        for category in valid_categories:
            cumulative_weight += weights.get(category, 1)
            if r <= cumulative_weight:
                return category
        
        # Fallback to a random choice
        return random.choice(valid_categories)
    
    def adjust_meal_plan(self, meal_plan, user_profile, adjustments):
        """
        Adjust an existing meal plan based on user feedback
        adjustments is a list of dictionaries with:
        - meal_id: ID of the meal to adjust
        - action: "remove_food", "add_food", "replace_meal", etc.
        - parameters: additional parameters for the action
        
        Returns the updated meal plan
        """
        if not adjustments:
            return meal_plan
        
        for adjustment in adjustments:
            action = adjustment.get("action")
            meal_id = adjustment.get("meal_id")
            
            if action == "remove_food":
                food_index = adjustment.get("food_index")
                if meal_id and food_index is not None:
                    meal_plan.remove_food_from_meal(meal_id, food_index)
            
            elif action == "add_food":
                food_id = adjustment.get("food_id")
                quantity = adjustment.get("quantity", 1.0)
                
                if meal_id and food_id:
                    food = self.food_database.get_food(food_id)
                    if food:
                        meal_plan.add_food_to_meal(meal_id, food, quantity)
            
            elif action == "replace_meal":
                meal_type = adjustment.get("meal_type")
                target_calories = adjustment.get("target_calories")
                
                if meal_id and meal_type and target_calories:
                    # Remove the old meal
                    meal_plan.remove_meal(meal_id)
                    
                    # Add a new meal
                    new_meal_id = meal_plan.add_meal(meal_type)
                    
                    # Generate foods for the new meal
                    self._generate_meal_foods(
                        meal_plan,
                        new_meal_id,
                        user_profile,
                        target_calories,
                        meal_type
                    )
        
        # Update nutritional summary
        meal_plan._update_nutritional_summary()
        return meal_plan
    
    def regenerate_meal(self, meal_plan, user_profile, meal_id):
        """
        Regenerate a single meal in the meal plan
        Returns the updated meal plan
        """
        # Find the meal to regenerate
        meal_to_regenerate = None
        for meal in meal_plan.meals:
            if meal["id"] == meal_id:
                meal_to_regenerate = meal
                break
        
        if not meal_to_regenerate:
            return meal_plan
        
        # Get the meal details
        meal_type = meal_to_regenerate["type"]
        day = meal_to_regenerate["day"]
        
        # Estimate target calories based on the meal's expected proportion
        meal_distribution = self._get_meal_distribution(len(set(m["type"] for m in meal_plan.meals)))
        meal_percentage = meal_distribution.get(meal_type, 30)  # Default to 30% if not found
        target_calories = meal_plan.daily_targets["calories"] * (meal_percentage / 100)
        
        # Remove the old meal
        meal_plan.remove_meal(meal_id)
        
        # Add a new meal
        new_meal_id = meal_plan.add_meal(meal_type, day)
        
        # Generate foods for the new meal
        self._generate_meal_foods(
            meal_plan,
            new_meal_id,
            user_profile,
            target_calories,
            meal_type
        )
        
        # Update nutritional summary
        meal_plan._update_nutritional_summary()
        return meal_plan
