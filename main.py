import json
import socket

import schema
import socketconfig
SOLAR_CAPACITY = 200
BATTERY_CAPACITY = 100
GENERATOR_PRICE = 1.0

def process(input_payload: schema.InputPayload, current_battery: int, hour: int) -> schema.ReturnPayload:
	"""Calculates the electricity allocation"""
	solarUnitsLeft = SOLAR_CAPACITY
	batteryUnitsLeft = current_battery
	totalLoad = 0
	nonSolar = 0
 
	SOLAR_WORK = True
	BATTERY_WORK = True
	GRID_WORK = True
	GENERATOR_WORK = True

	randomEvent = input_payload.get("random_event")
	buildingLoads = input_payload.get("loads")
	gridPrice = input_payload.get("grid_cost") 
 
	returnPayload : schema.ReturnPayload = {
		"buildings": [],
		"generator": 0
	} 

	for x in range(len(buildingLoads)):
		elecAlloc : schema.ElectricityAllocation = {
						"battery": 0,
						"grid": 0,
						"solar": 0
					}

		returnPayload.get("buildings").append(elecAlloc)

	# UPDATE STATUS
	match randomEvent:
		case "battery_failure":
			BATTERY_WORK = False
		case "cloudy_weather":
			SOLAR_WORK = False
		case "generator_failure":
			GENERATOR_WORK = False
		case "grid_failure":
			GRID_WORK = False

	# CALCULATE TOTAL LOAD
	for load in buildingLoads:
		totalLoad += load.get("load")

	tracker = buildingLoads
	if SOLAR_WORK:
		# LOOP FOR SOLAR
		for index, buildingLoad in enumerate(buildingLoads):
			buildingType = buildingLoad.get("type")
			# lecture halls can't use solar 
			if buildingType == "lecture_hall":
				nonSolar += 1
				continue

			load = buildingLoad.get("load")
			# allocate solar energy and update tracker
			if solarUnitsLeft > load:
				solarUnitsLeft -= load
				tracker[index].update({"load" : 0})
				returnPayload.get("buildings")[index].update({"solar" : load})
			elif solarUnitsLeft == 0:
				break
			else:
				tracker[index].update({"load" : load - solarUnitsLeft})
				returnPayload.get("buildings")[index].update({"solar" : solarUnitsLeft})
				solarUnitsLeft = 0		

	# LOOP FOR BATTERY + GRID
	for index, buildingLoad in enumerate(tracker):
		load = tracker[index].get("load")
		if gridPrice > GENERATOR_PRICE and batteryUnitsLeft > 0:
			if load != 0:
				if BATTERY_WORK:
					if batteryUnitsLeft > load:
						tracker[index].update({"load" : 0})
						returnPayload.get("buildings")[index].update({"battery" : load})
						batteryUnitsLeft -= load
					else:
						tracker[index].update({"load" : load - batteryUnitsLeft})
						returnPayload.get("buildings")[index].update({"battery" : batteryUnitsLeft})
						batteryUnitsLeft = 0
		else:
			if GRID_WORK:
				if load != 0:
					returnPayload.get("buildings")[index].update({"grid" : load})
					tracker[index].update({"load" : 0})

	if GENERATOR_WORK and (hour < 23):
		returnPayload.update({"generator" : BATTERY_CAPACITY - batteryUnitsLeft})
 
	return returnPayload

def run_client():
	battery = 0
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
		client.connect((socketconfig.HOST, socketconfig.PORT))

		for hour in range(24):
			# RECEIVING PAYLOAD FROM SOCKET
			payload: schema.InputPayload = json.loads(client.recv(1024))
			return_payload = process(payload, battery, hour)
			battery -= sum(allocation["battery"] for allocation in return_payload["buildings"])
			battery += return_payload["generator"]

			client.sendall(json.dumps(return_payload).encode("utf-8"))

if __name__ == "__main__":
	run_client()