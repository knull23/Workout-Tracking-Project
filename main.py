import requests
import datetime
import os

GENDER = "M"
WEIGHT_KG = 85
HEIGHT_CM = 182
AGE = 19

APP_ID = os.environ["NT_APP_ID"]
API_KEY = os.environ["NT_API_KEY"]
exercise_endpoint = os.environ["NT_EXERCISE_ENDPOINT"]
spreadsheets_endpoint = os.environ["NT_SHEET_ENDPOINT"]
USERNAME = os.environ["NT_USERNAME"]
PASSWORD = os.environ["NT_PASSWORD"]

exercise_text = input("Tell me which exercise you did: ")

today = datetime.datetime.now()
today_date = today.strftime("%d/%m/%Y")

time = datetime.datetime.now()
today_time = time.strftime("%X")

exercise_params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

response = requests.post(exercise_endpoint, json=exercise_params, headers=headers)
result = response.json()

for exercise in result["exercises"]:
    sheet_params = {
        "workout": {
            "date": today_date,
            "time": today_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(
        spreadsheets_endpoint,
        json=sheet_params,
        auth=(USERNAME, PASSWORD)
    )
    print(sheet_response.text)
