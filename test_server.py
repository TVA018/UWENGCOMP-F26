from contextlib import nullcontext
import json
import socket
import random 
import pre_made_tests
from schema import BuildingType, InputPayload, RandomEvent, Forecast, BuildingLoad, ReturnPayload
import socketconfig

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
            "type": myRandomBuilding,
            "load": random.randint(5, 70)
        })

    # Generate a random price for the electrical grid
    myGridPrice = round(random.uniform(0.50, 2.00), 2)

    myInputPayload: InputPayload = {
        "random_event": myRandomEvent,
        "forecast": myRandomForecast,
        "loads": myBuildingLoadList,
        "grid_cost": myGridPrice
    }

    return myInputPayload;

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((socketconfig.HOST, socketconfig.PORT))
    server.listen()

    (clientsocket, address) = server.accept()
    total = 0
    with clientsocket:
        print(f"Connected by {address}")
        for input_payload in pre_made_tests.tests:
            grid_cost = input_payload["grid_cost"]
            clientsocket.sendall(json.dumps(input_payload).encode("utf-8"))

            client_payload: ReturnPayload = json.loads(clientsocket.recv(1024))

            total += client_payload["generator"]
            total += grid_cost * sum(allocation["grid"] for allocation in client_payload["buildings"])

    print(f"{total:.2f}")