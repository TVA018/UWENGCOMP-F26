from contextlib import nullcontext
import json
import socket
import random 
from schema import BuildingType, InputPayload, RandomEvent, Forecast, BuildingLoad

def generate_test_data_for_hour() -> InputPayload:
    match random.randint(1, 5):
        case 1:
            randomEvent: RandomEvent = "none"   
        case 2:
            randomEvent: RandomEvent = "battery_failure"   
        case 3:
            randomEvent: RandomEvent = "cloudy_weather" 
        case 4:
            randomEvent: RandomEvent = "generator_failure"   
        case 5: 
            randomEvent: RandomEvent = "grid_failure" 

    match random.randint(1, 2):
        case 1:
            randomForecast: Forecast = "cloudy"
        case 2: 
            randomForecast: Forecast = "not cloudy"   

    myRandomBuilding: BuildingType
    myBuildingLoadList: list[BuildingLoad] = []

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

    gridCost = round(random.uniform(0.50, 2.00), 2)

    myInputPayload: InputPayload = {
        "random_event": randomEvent,
        "forecast": randomForecast,
        "buildingLoads": myBuildingLoadList,
        "grid_price": gridCost
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