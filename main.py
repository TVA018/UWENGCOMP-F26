import schema
SOLAR_CAPACITY = 200
BATTERY_CAPACITY = 100
GENERATOR_PRICE = 1.0
SOLAR_WORK = True
BATTERY_WORK = True
GRID_WORK = True

def process(input_payload: schema.InputPayload, current_battery) -> schema.ReturnPayload:
	# TODO: use batteryChargeTarget to optimize battery charging depending on availability of other resources
	batteryChargeTarget = 40
	solarUnitsLeft = SOLAR_CAPACITY
	batteryUnitsLeft = current_battery
	totalLoad = 0
	nonSolar = 0
	loadLeft = 0
	recharge = 0

	randomEvent = input_payload.get("random_event")
	buildingLoads = input_payload.get("buildingLoads")
	forecast = input_payload.get("forecast")
	gridPrice = input_payload.get("grid_price")
 
	elecAlloc : schema.ElectricityAllocation = {
		"battery": 0,
		"grid": 0,
		"solar": 0
	}	
 
	returnPayload : schema.ReturnPayload = {
		"buildings": [elecAlloc] * len(buildingLoads),
		"generator": 0
	} 

	# CALCULATE TOTAL LOAD
	for load in buildingLoads:
		totalLoad += load.get("load")

	tracker = buildingLoads
	
	# LOOP FOR SOLAR
	for buildingLoad in enumerate(buildingLoads):
		buildingType = buildingLoad.get("buildingType")
		if buildingType == "lecture_hall":
			nonSolar += 1
			continue
		load = buildingLoad.get("load")
		if solarUnitsLeft > load:
			solarUnitsLeft -= load

	# LOOP FOR BATTERY + GRID
	for index, buildingLoad in enumerate(tracker):
		load = tracker.get("load")
		if gridPrice > GENERATOR_PRICE and batteryUnitsLeft > 0:
			if load != 0:
				if batteryUnitsLeft > load:
					tracker[index].update({"load" : 0})
					returnPayload.get("buildings")[index].update({"battery" : load})
					batteryUnitsLeft -= loads
				else:
					tracker[index].update({"load" : load - batteryUnitsLeft})
					returnPayload.get("buildings")[index].update({"battery" : batteryUnitsLeft})
					batteryUnitsLeft = 0
		else:
			if load != 0:
				returnPayload.get("buildings")[index].update({"grid" : load})
				tracker[index].update({"load" : 0})


	returnPayload.update({"generator" : current_battery - batteryUnitsLeft})
 
	return returnPayload