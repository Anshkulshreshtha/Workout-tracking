import requests
from datetime import datetime
import os

GENDER = "Male"
WEIGHT_kg = 70
HEIGHT_cm = 164
AGE = 21

APP_ID = os.environ["b3d8693c"]
API_KEY = os.environ["b8fbc3ada0fdf5a895147928a46ad078"]

Exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = "https://api.sheety.co/9e3ed31a301a2ff0cff2f3cbc868697d/workoutTracking/workouts"


exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_kg,
    "height_cm": HEIGHT_cm,
    "age": AGE
}

response = requests.post(Exercise_endpoint, json=parameters, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

bearer_headers = {
    "Authorization": f"Bearer {os.environ[API_KEY]}"
}

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=bearer_headers)

    print(sheet_response.text)

