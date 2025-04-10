"""
Rule Engine for applying dietary rules and constraints
"""
import json
import os

class RuleEngine:
    """Rule engine for applying dietary rules and constraints to meal planning"""
    
    def __init__(self):
        """Initialize rule engine with rules from file"""
        self.rules = []
        self.load_rules()
    
    def load_rules(self):
        """Load rules from JSON file"""
        # First check if user has custom rules
        user_rules_path = os.path.join(os.path.expanduser("~"), ".nutrition_planner", "diet_rules.json")
        
        # Default rules path
        default_rules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "diet_rules.json")
        
        try:
            # Try loading user rules first
            if os.path.exists(user_rules_path):
                with open(user_rules_path, 'r') as f:
                    self.rules = json.load(f)
            # If no user rules, load default
            else:
                with open(default_rules_path, 'r') as f:
                    self.rules = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If no rules are found or they're invalid, create basic rules
            self.rules = self._create_default_rules()
            self.save_rules()
    
    def _create_default_rules(self):
        """Create default rules if none are found"""
        return {
            "diet_types": {
                "balanced": {
                    "description": "A balanced diet with a healthy mix of all food groups",
                    "constraints": [],
                    "recommendations": [
                        {"category": "fruits", "min_servings": 2, "max_servings": 4},
                        {"category": "vegetables", "min_servings": 3, "max_servings": 5},
                        {"category": "grains", "min_servings": 3, "max_servings": 8},
                        {"category": "proteins", "min_servings": 2, "max_servings": 3},
                        {"category": "dairy", "min_servings": 2, "max_servings": 3},
                        {"category": "fats_oils", "min_servings": 1, "max_servings": 3}
                    ]
                },
                "vegetarian": {
                    "description": "Diet excluding meat but includes dairy and eggs",
                    "constraints": [
                        {"condition": "category", "value": "proteins", "constraint": "restrict", 
                         "subcategory": "meat", "message": "Meat is not allowed in a vegetarian diet"}
                    ],
                    "recommendations": [
                        {"category": "fruits", "min_servings": 2, "max_servings": 4},
                        {"category": "vegetables", "min_servings": 4, "max_servings": 6},
                        {"category": "grains", "min_servings": 4, "max_servings": 8},
                        {"category": "proteins", "subcategory": "plant_based", "min_servings": 3, "max_servings": 5},
                        {"category": "dairy", "min_servings": 2, "max_servings": 3},
                        {"category": "fats_oils", "min_servings": 1, "max_servings": 3}
                    ]
                },
                "vegan": {
                    "description": "Diet excluding all animal products",
                    "constraints": [
                        {"condition": "category", "value": "proteins", "constraint": "restrict", 
                         "subcategory": "animal", "message": "Animal proteins are not allowed in a vegan diet"},
                        {"condition": "category", "value": "dairy", "constraint": "restrict", 
                         "message": "Dairy is not allowed in a vegan diet"}
                    ],
                    "recommendations": [
                        {"category": "fruits", "min_servings": 3, "max_servings": 5},
                        {"category": "vegetables", "min_servings": 5, "max_servings": 8},
                        {"category": "grains", "min_servings": 4, "max_servings": 8},
                        {"category": "proteins", "subcategory": "plant_based", "min_servings": 4, "max_servings": 6},
                        {"category": "fats_oils", "min_servings": 2, "max_servings": 4}
                    ]
                },
                "keto": {
                    "description": "High-fat, low-carb diet",
                    "constraints": [
                        {"condition": "nutrient", "value": "carbohydrates", "constraint": "max", 
                         "amount": 50, "unit": "g", "message": "Keto diet requires limiting carbs to 50g or less"}
                    ],
                    "recommendations": [
                        {"category": "fruits", "min_servings": 0, "max_servings": 1, 
                         "note": "Choose low-carb berries only"},
                        {"category": "vegetables", "min_servings": 3, "max_servings": 5, 
                         "note": "Focus on leafy greens and low-carb vegetables"},
                        {"category": "grains", "min_servings": 0, "max_servings": 0, 
                         "note": "Grains are generally avoided on keto"},
                        {"category": "proteins", "min_servings": 3, "max_servings": 5},
                        {"category": "dairy", "min_servings": 2, "max_servings": 4, 
                         "note": "Choose full-fat options"},
                        {"category": "fats_oils", "min_servings": 4, "max_servings": 8}
                    ]
                },
                "low_carb": {
                    "description": "Diet with reduced carbohydrate intake",
                    "constraints": [
                        {"condition": "nutrient", "value": "carbohydrates", "constraint": "max", 
                         "amount": 100, "unit": "g", "message": "Low-carb diet requires limiting carbs to 100g or less"}
                    ],
                    "recommendations": [
                        {"category": "fruits", "min_servings": 1, "max_servings": 2},
                        {"category": "vegetables", "min_servings": 4, "max_servings": 6},
                        {"category": "grains", "min_servings": 1, "max_servings": 2, 
                         "note": "Choose whole grains only"},
                        {"category": "proteins", "min_servings": 3, "max_servings": 5},
                        {"category": "dairy", "min_servings": 2, "max_servings": 3},
                        {"category": "fats_oils", "min_servings": 2, "max_servings": 5}
                    ]
                }
            },
            "medical_conditions": {
                "diabetes": {
                    "description": "Recommendations for managing diabetes",
                    "constraints": [
                        {"condition": "nutrient", "value": "sugars", "constraint": "min", 
                         "message": "Limit foods with added sugars for diabetes management"},
                        {"condition": "glycemic_index", "value": "high", "constraint": "restrict", 
                         "message": "Avoid high glycemic index foods for diabetes management"}
                    ],
                    "recommendations": [
                        {"advice": "Choose complex carbohydrates over simple sugars"},
                        {"advice": "Spread carbohydrate intake throughout the day"},
                        {"advice": "Include fiber-rich foods to help manage blood sugar"},
                        {"advice": "Monitor portion sizes carefully"}
                    ]
                },
                "hypertension": {
                    "description": "Recommendations for managing high blood pressure",
                    "constraints": [
                        {"condition": "nutrient", "value": "sodium", "constraint": "max", 
                         "amount": 1500, "unit": "mg", 
                         "message": "Limit sodium to 1500mg per day for hypertension management"}
                    ],
                    "recommendations": [
                        {"advice": "Follow the DASH diet approach"},
                        {"advice": "Include potassium-rich foods to help counter sodium effects"},
                        {"advice": "Limit alcohol consumption"},
                        {"advice": "Choose fresh foods over processed foods which tend to be high in sodium"}
                    ]
                },
                "high_cholesterol": {
                    "description": "Recommendations for managing high cholesterol",
                    "constraints": [
                        {"condition": "nutrient", "value": "saturated_fat", "constraint": "max", 
                         "percentage": 5, "of": "calories", 
                         "message": "Limit saturated fat to less than 5% of daily calories for cholesterol management"}
                    ],
                    "recommendations": [
                        {"advice": "Choose lean proteins and low-fat dairy"},
                        {"advice": "Increase soluble fiber intake"},
                        {"advice": "Include plant sterols/stanols in your diet"},
                        {"advice": "Replace saturated fats with unsaturated fats like olive oil and nuts"}
                    ]
                }
            },
            "allergies": {
                "gluten": {
                    "description": "Gluten allergy/intolerance",
                    "constraints": [
                        {"condition": "contains", "value": "gluten", "constraint": "restrict", 
                         "message": "Avoid gluten-containing foods"}
                    ],
                    "alternative_foods": [
                        {"avoid": "wheat bread", "alternative": "gluten-free bread"},
                        {"avoid": "wheat pasta", "alternative": "rice or corn pasta"},
                        {"avoid": "regular oats", "alternative": "certified gluten-free oats"}
                    ]
                },
                "dairy": {
                    "description": "Dairy allergy/intolerance",
                    "constraints": [
                        {"condition": "contains", "value": "dairy", "constraint": "restrict", 
                         "message": "Avoid dairy-containing foods"}
                    ],
                    "alternative_foods": [
                        {"avoid": "cow's milk", "alternative": "almond milk, soy milk, oat milk"},
                        {"avoid": "cheese", "alternative": "dairy-free cheese alternatives"},
                        {"avoid": "yogurt", "alternative": "coconut or soy yogurt"}
                    ]
                },
                "nuts": {
                    "description": "Nut allergies",
                    "constraints": [
                        {"condition": "contains", "value": "nuts", "constraint": "restrict", 
                         "message": "Avoid foods containing nuts"}
                    ],
                    "alternative_foods": [
                        {"avoid": "peanut butter", "alternative": "sunflower seed butter"},
                        {"avoid": "almond flour", "alternative": "seed-based flours or coconut flour"},
                        {"avoid": "nut milks", "alternative": "oat milk, rice milk, or hemp milk"}
                    ]
                }
            }
        }
    
    def save_rules(self):
        """Save rules to JSON file in user's directory"""
        user_data_dir = os.path.join(os.path.expanduser("~"), ".nutrition_planner")
        os.makedirs(user_data_dir, exist_ok=True)
        
        file_path = os.path.join(user_data_dir, "diet_rules.json")
        with open(file_path, 'w') as f:
            json.dump(self.rules, f, indent=2)
    
    def get_diet_rules(self, diet_type):
        """Get rules for a specific diet type"""
        return self.rules.get("diet_types", {}).get(diet_type, {})
    
    def get_medical_condition_rules(self, condition):
        """Get rules for a specific medical condition"""
        return self.rules.get("medical_conditions", {}).get(condition, {})
    
    def get_allergy_rules(self, allergy):
        """Get rules for a specific allergy"""
        return self.rules.get("allergies", {}).get(allergy, {})
    
    def evaluate_food_constraints(self, food_item, user_profile):
        """
        Evaluate if a food item violates any constraints based on user profile
        Returns (allowed, constraint_message)
        """
        allowed = True
        constraint_message = None
        
        # Check diet type constraints
        diet_rules = self.get_diet_rules(user_profile.diet_type)
        if diet_rules:
            for constraint in diet_rules.get("constraints", []):
                if constraint["condition"] == "category" and constraint["value"] == food_item["category"]:
                    if "subcategory" in constraint and "subcategory" in food_item:
                        if constraint["subcategory"] == food_item["subcategory"] and constraint["constraint"] == "restrict":
                            allowed = False
                            constraint_message = constraint.get("message", f"This food is not allowed in a {user_profile.diet_type} diet")
                    elif constraint["constraint"] == "restrict":
                        allowed = False
                        constraint_message = constraint.get("message", f"This food is not allowed in a {user_profile.diet_type} diet")
                
                elif constraint["condition"] == "nutrient" and constraint["value"] in food_item["nutrients"]:
                    nutrient_value = food_item["nutrients"][constraint["value"]]
                    if constraint["constraint"] == "max" and nutrient_value > constraint.get("amount", 0):
                        allowed = False
                        constraint_message = constraint.get("message", f"This food exceeds the {constraint['value']} limit for a {user_profile.diet_type} diet")
        
        # Check medical condition constraints
        for condition in user_profile.medical_conditions:
            condition_rules = self.get_medical_condition_rules(condition)
            if condition_rules:
                for constraint in condition_rules.get("constraints", []):
                    if constraint["condition"] == "nutrient" and constraint["value"] in food_item["nutrients"]:
                        nutrient_value = food_item["nutrients"][constraint["value"]]
                        if constraint["constraint"] == "max" and nutrient_value > constraint.get("amount", 0):
                            allowed = False
                            constraint_message = constraint.get("message", f"This food exceeds the {constraint['value']} limit recommended for {condition}")
                    
                    elif constraint["condition"] == "glycemic_index" and "glycemic_index" in food_item:
                        if constraint["value"] == food_item["glycemic_index"] and constraint["constraint"] == "restrict":
                            allowed = False
                            constraint_message = constraint.get("message", f"This food has a high glycemic index, which is not recommended for {condition}")
        
        # Check allergy constraints
        for allergy in user_profile.allergies:
            allergy_rules = self.get_allergy_rules(allergy)
            if allergy_rules:
                for constraint in allergy_rules.get("constraints", []):
                    if constraint["condition"] == "contains" and "contains" in food_item:
                        allergens = food_item.get("contains", [])
                        if constraint["value"] in allergens and constraint["constraint"] == "restrict":
                            allowed = False
                            constraint_message = constraint.get("message", f"This food contains {constraint['value']}, which you are allergic to")
        
        return allowed, constraint_message
    
    def get_food_alternatives(self, food_item, user_profile):
        """Get alternatives for a food based on user profile constraints"""
        alternatives = []
        
        # Check for alternatives based on allergies
        for allergy in user_profile.allergies:
            allergy_rules = self.get_allergy_rules(allergy)
            if allergy_rules:
                for alt in allergy_rules.get("alternative_foods", []):
                    if alt["avoid"].lower() in food_item["name"].lower():
                        alternatives.append({
                            "avoid": alt["avoid"],
                            "alternative": alt["alternative"],
                            "reason": f"Due to {allergy} allergy"
                        })
        
        return alternatives
    
    def get_recommendations(self, user_profile):
        """Get diet recommendations based on user profile"""
        recommendations = []
        
        # Get diet type recommendations
        diet_rules = self.get_diet_rules(user_profile.diet_type)
        if diet_rules:
            recommendations.append({
                "type": "diet",
                "name": user_profile.diet_type,
                "description": diet_rules.get("description", ""),
                "servings": diet_rules.get("recommendations", [])
            })
        
        # Get medical condition recommendations
        for condition in user_profile.medical_conditions:
            condition_rules = self.get_medical_condition_rules(condition)
            if condition_rules:
                recommendations.append({
                    "type": "medical_condition",
                    "name": condition,
                    "description": condition_rules.get("description", ""),
                    "advice": [rec["advice"] for rec in condition_rules.get("recommendations", [])]
                })
        
        return recommendations
