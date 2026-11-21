from contextlib import nullcontext
import json
import socket
import random 
from schema import BuildingType, InputPayload, RandomEvent, Forecast, BuildingLoad

def generate_test_data_for_hour() -> InputPayload:
    # Generate a random event
    match random.randint(1, 5):
        case 1:
            myRandomEvent: RandomEvent = "none"   
        case 2:
            myRandomEvent: RandomEvent = "battery_failure"   
        case 3:
            myRandomEvent: RandomEvent = "cloudy_weather" 
        case 4:
            myRandomEvent: RandomEvent = "generator_failure"   
        case 5: 
            myRandomEvent: RandomEvent = "grid_failure" 

    # Generate a forecast (cloudy or not cloudy)
    match random.randint(1, 2):
        case 1:
            myRandomForecast: Forecast = "cloudy"
        case 2: 
            myRandomForecast: Forecast = "not cloudy"   

    myRandomBuilding: BuildingType
    myBuildingLoadList: list[BuildingLoad] = []

    # Generate a building payload
    for i in range(random.randint(7, 10)):
        match random.randint(1, 5):
            case 1:
                myRandomBuilding = "laboratory"
            case 2:
                myRandomBuilding = "lecture_hall" 
            case 3:
                myRandomBuilding = "library"
            case 4:
                myRandomBuilding = "student_centre" 
            case 5: 
                myRandomBuilding = "student_residence"
        myBuildingLoadList.append({
            "buildingType": myRandomBuilding,
            "load": random.randint(5, 70)
        })

    # Generate a random price for the electrical grid
    myGridPrice = round(random.uniform(0.50, 2.00), 2)

    myInputPayload: InputPayload = {
        "random_event": myRandomEvent,
        "forecast": myRandomForecast,
        "buildingLoads": myBuildingLoadList,
        "grid_price": myGridPrice
    }

    return myInputPayload;

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(("127.0.0.1", 8800))
    server.listen()

    while True:
        (clientsocket, address) = server.accept()
        with clientsocket:
            print(f"Connected by {address}")
            while True:
                hour_info: InputPayload = generate_test_data_for_hour() # Generate test data to store in this dictionary
                clientsocket.sendall(json.dumps(hour_info).encode("utf-8"))