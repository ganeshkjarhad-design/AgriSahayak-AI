# AgriSahayak AI
AI-Based Crop Disease Detection, Agricultural Worker Recommendation and Farm Assistance System

## Features
1. Farmer and worker registration/login (demo authentication).
2. Crop leaf disease prediction using a transfer-learning image classifier.
3. Agricultural worker search and recommendation.
4. Worker booking.
5. Dashboard and basic analytics.
6. SQLite database for easy college-project setup.

## Project structure
- app.py - Flask web application
- train_model.py - model training
- schema.sql - database schema and sample data
- templates/ - HTML pages
- static/style.css - UI styling
- model/ - trained model and class names (created after training)
- data/ - optional local dataset

## Setup
Python 3.11/3.12 is recommended.

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Train the AI model
Download the PlantVillage dataset. The TensorFlow Dataset documentation describes 54,303 images in 38 categories.
For the easiest local training route, place the class folders under:
data/PlantVillage/<class_name>/*.jpg

Then:
```bash
python train_model.py
```
The script creates:
- model/agrisaahayak_model.keras
- model/class_names.json

For a laptop demonstration, you can train on a smaller selected subset first.

## Safety
The disease model is an academic decision-support prototype, not a substitute for an agricultural officer or product label. Do not hard-code pesticide dosage recommendations. Treatment information in the database should be reviewed against current official/local agricultural guidance and product labels.
