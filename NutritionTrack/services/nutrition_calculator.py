"""
Nutrition calculator service for calculating BMR, TDEE, and nutrient requirements
"""
import math

class NutritionCalculator:
    """Nutrition Calculator to determine caloric and nutrient requirements"""
    
    # Activity level multipliers
    ACTIVITY_MULTIPLIERS = {
        "sedentary": 1.2,       # Little or no exercise
        "light": 1.375,         # Light exercise 1-3 days/week
        "moderate": 1.55,       # Moderate exercise 3-5 days/week
        "active": 1.725,        # Active - hard exercise 6-7 days/week
        "very_active": 1.9      # Very active - hard daily exercise & physical job
    }
    
    # Weight goal adjustments (calories)
    WEIGHT_GOAL_ADJUSTMENTS = {
        "lose": -500,           # Caloric deficit for weight loss
        "maintain": 0,          # Maintain current weight
        "gain": 500             # Caloric surplus for weight gain
    }
    
    @staticmethod
    def calculate_bmr(gender, weight_kg, height_cm, age):
        """
        Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation
        - gender: 'male' or 'female'
        - weight_kg: weight in kilograms
        - height_cm: height in centimeters
        - age: age in years
        """
        if gender.lower() == 'male':
            return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:  # female or other
            return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    
    @staticmethod
    def calculate_tdee(bmr, activity_level):
        """
        Calculate Total Daily Energy Expenditure (TDEE)
        - bmr: Basal Metabolic Rate
        - activity_level: activity level from ACTIVITY_MULTIPLIERS keys
        """
        multiplier = NutritionCalculator.ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)
        return bmr * multiplier
    
    @staticmethod
    def calculate_calorie_target(tdee, weight_goal):
        """
        Calculate daily calorie target based on TDEE and weight goal
        - tdee: Total Daily Energy Expenditure
        - weight_goal: goal from WEIGHT_GOAL_ADJUSTMENTS keys
        """
        adjustment = NutritionCalculator.WEIGHT_GOAL_ADJUSTMENTS.get(weight_goal, 0)
        return max(1200, tdee + adjustment)  # Ensure minimum healthy calorie intake
    
    @staticmethod
    def calculate_macronutrient_targets(calorie_target, diet_type="balanced"):
        """
        Calculate macronutrient targets based on calorie target and diet type
        Returns protein, carbs, fat in grams
        """
        # Default macronutrient distribution (balanced diet)
        protein_pct = 0.30  # 30% of calories from protein
        carbs_pct = 0.45    # 45% of calories from carbs
        fat_pct = 0.25      # 25% of calories from fat
        
        # Adjust based on diet type
        if diet_type == "keto":
            protein_pct = 0.25
            carbs_pct = 0.05
            fat_pct = 0.70
        elif diet_type == "low_carb":
            protein_pct = 0.35
            carbs_pct = 0.20
            fat_pct = 0.45
        elif diet_type == "high_protein":
            protein_pct = 0.40
            carbs_pct = 0.40
            fat_pct = 0.20
        elif diet_type == "vegan" or diet_type == "vegetarian":
            protein_pct = 0.25
            carbs_pct = 0.55
            fat_pct = 0.20
        
        # Calculate grams of each macronutrient
        # Protein and carbs = 4 calories per gram, fat = 9 calories per gram
        protein_g = (calorie_target * protein_pct) / 4
        carbs_g = (calorie_target * carbs_pct) / 4
        fat_g = (calorie_target * fat_pct) / 9
        fiber_g = 14 * (calorie_target / 1000)  # ~14g per 1000 calories
        
        return {
            "protein": math.ceil(protein_g),
            "carbs": math.ceil(carbs_g),
            "fat": math.ceil(fat_g),
            "fiber": math.ceil(fiber_g)
        }
    
    @staticmethod
    def calculate_micronutrient_targets(age, gender, pregnancy=False, lactation=False):
        """
        Calculate daily micronutrient targets based on age and gender
        Returns dictionary of recommended vitamins and minerals
        
        This is a simplified version and should be expanded with a complete
        reference table of DRIs (Dietary Reference Intakes)
        """
        # Base target values (simplified)
        targets = {
            "vitamins": {
                "vitamin_a": 900 if gender == "male" else 700,  # mcg RAE
                "vitamin_c": 90 if gender == "male" else 75,    # mg
                "vitamin_d": 15,                                # mcg
                "vitamin_e": 15,                                # mg
                "vitamin_k": 120 if gender == "male" else 90,   # mcg
                "vitamin_b6": 1.3,                              # mg
                "vitamin_b12": 2.4,                             # mcg
                "folate": 400,                                  # mcg DFE
            },
            "minerals": {
                "calcium": 1000,                                # mg
                "iron": 8 if gender == "male" else 18,          # mg
                "magnesium": 400 if gender == "male" else 310,  # mg
                "zinc": 11 if gender == "male" else 8,          # mg
                "potassium": 3400 if gender == "male" else 2600,# mg
                "sodium": 1500,                                 # mg
            }
        }
        
        # Adjust for age
        if age > 50:
            targets["minerals"]["calcium"] = 1200  # mg
            if gender == "female":
                targets["minerals"]["iron"] = 8  # mg (postmenopausal)
        
        # Adjust for pregnancy or lactation
        if gender == "female" and pregnancy:
            targets["vitamins"]["folate"] = 600  # mcg DFE
            targets["minerals"]["iron"] = 27     # mg
        elif gender == "female" and lactation:
            targets["vitamins"]["vitamin_a"] = 1300  # mcg RAE
            targets["vitamins"]["vitamin_c"] = 120   # mg
        
        return targets
    
    @staticmethod
    def calculate_nutrition_targets(user_profile):
        """
        Calculate complete nutrition targets based on user profile
        Returns dictionary with all calorie and nutrient targets
        """
        # Calculate BMR and TDEE
        bmr = NutritionCalculator.calculate_bmr(
            user_profile.gender,
            user_profile.weight,
            user_profile.height,
            user_profile.age
        )
        
        tdee = NutritionCalculator.calculate_tdee(bmr, user_profile.activity_level)
        
        # Calculate calorie target based on weight goal
        calorie_target = NutritionCalculator.calculate_calorie_target(tdee, user_profile.weight_goal)
        
        # Calculate macronutrient targets
        macros = NutritionCalculator.calculate_macronutrient_targets(calorie_target, user_profile.diet_type)
        
        # Calculate micronutrient targets
        micros = NutritionCalculator.calculate_micronutrient_targets(user_profile.age, user_profile.gender)
        
        # Combine all targets
        targets = {
            "calories": calorie_target,
            "protein": macros["protein"],
            "carbs": macros["carbs"],
            "fat": macros["fat"],
            "fiber": macros["fiber"],
            "vitamins": micros["vitamins"],
            "minerals": micros["minerals"],
            # Additional calculated values for reference
            "bmr": bmr,
            "tdee": tdee
        }
        
        return targets
    
    @staticmethod
    def analyze_nutrient_intake(meal_plan, targets):
        """
        Analyze current nutrient intake versus targets
        Returns dictionary with analysis results and recommendations
        """
        # Get current intake from meal plan
        current = meal_plan.nutritional_summary
        
        # Calculate percentages of targets met
        analysis = {
            "targets_met": {},
            "deficiencies": [],
            "excesses": [],
            "recommendations": []
        }
        
        # Check macronutrients
        for nutrient in ["calories", "protein", "carbs", "fat", "fiber"]:
            target_value = targets.get(nutrient, 0)
            current_value = current.get(nutrient, 0)
            
            if target_value > 0:
                percentage = (current_value / target_value) * 100
                analysis["targets_met"][nutrient] = percentage
                
                # Check for significant deficiencies or excesses
                if percentage < 80:
                    analysis["deficiencies"].append({
                        "nutrient": nutrient,
                        "current": current_value,
                        "target": target_value,
                        "percentage": percentage
                    })
                elif percentage > 120:
                    analysis["excesses"].append({
                        "nutrient": nutrient,
                        "current": current_value,
                        "target": target_value,
                        "percentage": percentage
                    })
        
        # Generate recommendations based on analysis
        if analysis["deficiencies"]:
            for deficiency in analysis["deficiencies"]:
                nutrient = deficiency["nutrient"]
                if nutrient == "calories":
                    analysis["recommendations"].append(
                        "Increase overall food intake to meet calorie requirements."
                    )
                elif nutrient == "protein":
                    analysis["recommendations"].append(
                        "Add more protein-rich foods like lean meats, fish, eggs, or plant proteins."
                    )
                elif nutrient == "carbs":
                    analysis["recommendations"].append(
                        "Include more whole grains, fruits, and vegetables for healthy carbohydrates."
                    )
                elif nutrient == "fat":
                    analysis["recommendations"].append(
                        "Add healthy fats from sources like avocados, nuts, seeds, and olive oil."
                    )
                elif nutrient == "fiber":
                    analysis["recommendations"].append(
                        "Increase fiber intake with more whole grains, legumes, fruits, and vegetables."
                    )
        
        if analysis["excesses"]:
            for excess in analysis["excesses"]:
                nutrient = excess["nutrient"]
                if nutrient == "calories":
                    analysis["recommendations"].append(
                        "Reduce overall food intake to avoid exceeding your calorie target."
                    )
                elif nutrient == "fat":
                    analysis["recommendations"].append(
                        "Consider reducing high-fat foods, particularly saturated fats."
                    )
        
        return analysis
