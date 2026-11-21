import schema
SOLAR_CAPACITY = 200
BATTERY_CAPACITY = 100

def process(input_payload: schema.InputPayload) -> schema.ReturnPayload:
	# TODO: use batteryChargeTarget to optimize battery charging depending on availability of other resources
	batteryChargeTarget = 40
	solarUnitsLeft = SOLAR_CAPACITY
	batteryUnitsLeft = BATTERY_CAPACITY
	totalLoad = 0
	nonSolar = 0
	returnPayload : schema.ReturnPayload = {
		"buildings": [],
		"generator": 0
	} 

	randomEvent = input_payload.get("random_event")
	buildingLoads = input_payload.get("buildingLoads")
	forecast = input_payload.get("forecast")
	gridPrice = input_payload.get("grid_price")

	# CALCULATE TOTAL LOAD
	for load in buildingLoads:
		totalLoad += load.get("load")

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