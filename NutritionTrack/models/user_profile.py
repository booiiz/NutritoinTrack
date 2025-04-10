"""
User profile model for storing user information, preferences, and health conditions
"""
import json
import os
import uuid
from datetime import datetime

class UserProfile:
    """User profile class to store personal details, preferences, and health conditions"""
    
    def __init__(self, user_id=None):
        """Initialize user profile with default values"""
        self.user_id = user_id if user_id else str(uuid.uuid4())
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        
        # Personal details
        self.name = ""
        self.age = 0
        self.gender = ""  # "male", "female", "other"
        self.weight = 0.0  # in kg
        self.height = 0.0  # in cm
        self.activity_level = "sedentary"  # sedentary, light, moderate, active, very_active
        
        # Health information
        self.target_weight = 0.0  # in kg
        self.weight_goal = "maintain"  # lose, maintain, gain
        self.medical_conditions = []  # list of conditions like "diabetes", "hypertension", etc.
        self.allergies = []  # list of food allergies
        
        # Dietary preferences
        self.diet_type = "balanced"  # vegan, vegetarian, keto, balanced, etc.
        self.food_preferences = {
            "liked": [],
            "disliked": []
        }
        self.meal_count = 3  # number of meals per day
    
    def calculate_bmi(self):
        """Calculate Body Mass Index"""
        if self.height > 0 and self.weight > 0:
            # BMI = weight(kg) / height(m)²
            height_m = self.height / 100
            return self.weight / (height_m * height_m)
        return 0
    
    def get_bmi_category(self):
        """Return BMI category based on calculated BMI"""
        bmi = self.calculate_bmi()
        if bmi == 0:
            return "Unknown"
        elif bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def to_dict(self):
        """Convert user profile to dictionary for serialization"""
        return {
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": datetime.now().isoformat(),
            "personal_details": {
                "name": self.name,
                "age": self.age,
                "gender": self.gender,
                "weight": self.weight,
                "height": self.height,
                "activity_level": self.activity_level
            },
            "health_information": {
                "target_weight": self.target_weight,
                "weight_goal": self.weight_goal,
                "medical_conditions": self.medical_conditions,
                "allergies": self.allergies
            },
            "dietary_preferences": {
                "diet_type": self.diet_type,
                "food_preferences": self.food_preferences,
                "meal_count": self.meal_count
            }
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create user profile from dictionary"""
        profile = cls(user_id=data.get("user_id"))
        profile.created_at = data.get("created_at", profile.created_at)
        profile.updated_at = data.get("updated_at", profile.updated_at)
        
        personal = data.get("personal_details", {})
        profile.name = personal.get("name", profile.name)
        profile.age = personal.get("age", profile.age)
        profile.gender = personal.get("gender", profile.gender)
        profile.weight = personal.get("weight", profile.weight)
        profile.height = personal.get("height", profile.height)
        profile.activity_level = personal.get("activity_level", profile.activity_level)
        
        health = data.get("health_information", {})
        profile.target_weight = health.get("target_weight", profile.target_weight)
        profile.weight_goal = health.get("weight_goal", profile.weight_goal)
        profile.medical_conditions = health.get("medical_conditions", profile.medical_conditions)
        profile.allergies = health.get("allergies", profile.allergies)
        
        dietary = data.get("dietary_preferences", {})
        profile.diet_type = dietary.get("diet_type", profile.diet_type)
        profile.food_preferences = dietary.get("food_preferences", profile.food_preferences)
        profile.meal_count = dietary.get("meal_count", profile.meal_count)
        
        return profile
    
    def save(self):
        """Save user profile to JSON file"""
        profiles_dir = os.path.join(os.path.expanduser("~"), ".nutrition_planner", "profiles")
        os.makedirs(profiles_dir, exist_ok=True)
        
        file_path = os.path.join(profiles_dir, f"{self.user_id}.json")
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, user_id):
        """Load user profile from JSON file"""
        file_path = os.path.join(os.path.expanduser("~"), ".nutrition_planner", "profiles", f"{user_id}.json")
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return cls.from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    @classmethod
    def get_all_profiles(cls):
        """Get all available user profiles"""
        profiles_dir = os.path.join(os.path.expanduser("~"), ".nutrition_planner", "profiles")
        os.makedirs(profiles_dir, exist_ok=True)
        
        profiles = []
        for filename in os.listdir(profiles_dir):
            if filename.endswith(".json"):
                user_id = filename.replace(".json", "")
                profile = cls.load(user_id)
                if profile:
                    profiles.append(profile)
        
        return profiles
