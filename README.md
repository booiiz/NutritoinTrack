# NutritoinTrack

# Nutrition and Diet Planning System

A smart application designed to help users manage their diet and nutrition needs. This Python-based system with a modern PyQt6 GUI provides personalized meal planning, nutrition tracking, and diet recommendations based on user profiles and dietary requirements.

## Features

- **User Profiles**: Create and manage profiles with health conditions, dietary preferences, and nutrition goals
- **Meal Planning**: Generate customized meal plans based on dietary needs and preferences
- **Food Database**: Comprehensive database of foods with detailed nutritional information
- **Diet Rules Engine**: Smart diet recommendations based on health conditions and dietary restrictions
- **Nutrition Calculation**: Calculate personalized BMR, TDEE, and nutrient requirements
- **Interactive Reports**: Visualize nutrition data with charts and detailed analysis
- **Dark/Light Theme**: Modern UI with theme switching support

## Screenshots

*[Screenshots will be added here]*

## Installation

### Prerequisites

- Python 3.8+
- PyQt6
- pandas
- numpy
- matplotlib

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/nutrition-diet-planner.git
   cd nutrition-diet-planner
   ```

2. Install the required dependencies:
   ```
   pip install PyQt6 pandas numpy matplotlib
   ```

3. Run the application:
   ```
   python main.py
   ```

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **System Dependencies**: 
  - libxkbcommon
  - fontconfig
  - dbus

## Usage Guide

1. **Create a Profile**: Start by creating a new user profile or loading an existing one
2. **Generate Meal Plan**: The system will create a meal plan based on your profile data
3. **Customize Meals**: Add or remove foods from meals as needed
4. **View Reports**: Generate nutrition reports to visualize your intake against targets

## Project Structure

- **models/**: Data models for user profiles, food database, and meal plans
- **services/**: Core services including meal planning, nutrition calculation, and reporting
- **gui/**: User interface components built with PyQt6
- **data/**: Food database and diet rules in JSON format

## Features in Detail

### User Profile Management

The system allows for detailed user profiles including:
- Personal information (age, gender, height, weight)
- Activity level and weight goals
- Health conditions and allergies
- Dietary preferences and restrictions

### Diet Types Supported

- Balanced
- Vegetarian
- Vegan
- Keto
- Low Carb
- High Protein
- Mediterranean
- Paleo

### Medical Conditions Supported

- Diabetes
- Hypertension
- High Cholesterol
- Heart Disease
- Kidney Disease
- Liver Disease

## Development

This project is structured to be modular and extensible. You can contribute by:

- Adding new foods to the database
- Implementing additional diet rules
- Enhancing the UI components
- Improving meal planning algorithms

## License

[MIT License](LICENSE)

## Acknowledgements

- Food database compiled from multiple nutrition data sources
- Diet rules based on established nutritional guidelines and research
