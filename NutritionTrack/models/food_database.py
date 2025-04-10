"""
Food database model for storing nutritional information about foods
"""
import json
import os
import pandas as pd

class FoodDatabase:
    """Food database class to manage food items and their nutritional information"""
    
    def __init__(self):
        """Initialize food database"""
        self.foods = {}
        self.load_database()
    
    def load_database(self):
        """Load food database from JSON file"""
        # First check if user has a custom database
        user_db_path = os.path.join(os.path.expanduser("~"), ".nutrition_planner", "food_database.json")
        
        # Default database path
        default_db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "food_database.json")
        
        try:
            # Try loading user database first
            if os.path.exists(user_db_path):
                with open(user_db_path, 'r') as f:
                    self.foods = json.load(f)
            # If no user database, load default
            else:
                with open(default_db_path, 'r') as f:
                    self.foods = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If no database is found or it's invalid, create an empty one
            self.foods = {
                "categories": {
                    "fruits": [],
                    "vegetables": [],
                    "grains": [],
                    "proteins": [],
                    "dairy": [],
                    "fats_oils": [],
                    "beverages": [],
                    "other": []
                },
                "items": {}
            }
            # Save the new database
            self.save_database()
    
    def save_database(self):
        """Save food database to JSON file in user's directory"""
        user_data_dir = os.path.join(os.path.expanduser("~"), ".nutrition_planner")
        os.makedirs(user_data_dir, exist_ok=True)
        
        file_path = os.path.join(user_data_dir, "food_database.json")
        with open(file_path, 'w') as f:
            json.dump(self.foods, f, indent=2)
    
    def add_food(self, food_id, name, category, nutrients, serving_size="100g", serving_unit="g"):
        """Add a new food item to the database"""
        if category not in self.foods["categories"]:
            self.foods["categories"][category] = []
        
        if food_id not in self.foods["categories"][category]:
            self.foods["categories"][category].append(food_id)
        
        self.foods["items"][food_id] = {
            "name": name,
            "category": category,
            "serving_size": serving_size,
            "serving_unit": serving_unit,
            "nutrients": nutrients
        }
        
        self.save_database()
    
    def get_food(self, food_id):
        """Get a food item by ID"""
        return self.foods["items"].get(food_id)
    
    def search_foods(self, query, category=None):
        """Search for food items by name or category"""
        results = []
        query = query.lower()
        
        for food_id, food in self.foods["items"].items():
            if category and food["category"] != category:
                continue
            
            if query in food["name"].lower():
                results.append({
                    "id": food_id,
                    **food
                })
        
        return results
    
    def get_categories(self):
        """Get list of all food categories"""
        return list(self.foods["categories"].keys())
    
    def get_foods_by_category(self, category):
        """Get all foods in a category"""
        if category not in self.foods["categories"]:
            return []
        
        return [
            {"id": food_id, **self.foods["items"][food_id]}
            for food_id in self.foods["categories"][category]
            if food_id in self.foods["items"]
        ]
    
    def to_dataframe(self):
        """Convert food database to pandas DataFrame for analysis"""
        foods_list = []
        
        for food_id, food in self.foods["items"].items():
            food_data = {
                "food_id": food_id,
                "name": food["name"],
                "category": food["category"],
                "serving_size": food["serving_size"],
                "serving_unit": food["serving_unit"]
            }
            
            # Add nutrients
            for nutrient, value in food["nutrients"].items():
                food_data[nutrient] = value
            
            foods_list.append(food_data)
        
        return pd.DataFrame(foods_list)
    
    def import_from_csv(self, file_path):
        """Import food data from CSV file"""
        try:
            df = pd.read_csv(file_path)
            required_columns = ["food_id", "name", "category"]
            
            if not all(col in df.columns for col in required_columns):
                raise ValueError("CSV missing required columns: food_id, name, category")
            
            # Process each row
            for _, row in df.iterrows():
                food_id = str(row["food_id"])
                name = row["name"]
                category = row["category"]
                
                # Extract nutrients - assuming all non-metadata columns are nutrients
                nutrients = {}
                for col in df.columns:
                    if col not in ["food_id", "name", "category", "serving_size", "serving_unit"]:
                        nutrients[col] = row[col]
                
                # Get serving info if available
                serving_size = row.get("serving_size", "100g")
                serving_unit = row.get("serving_unit", "g")
                
                self.add_food(food_id, name, category, nutrients, serving_size, serving_unit)
            
            return True
        except Exception as e:
            print(f"Error importing CSV: {e}")
            return False
