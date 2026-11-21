import schema
SOLAR_CAPACITY = 200
BATTERY_CAPACITY = 100

def process(input_payload: schema.InputPayload) -> schema.ReturnPayload:
	# TODO: use batteryChargeTarget to optimize battery charging depending on availability of other resources
	batteryChargeTarget = 40
	solarUnitsLeft = SOLAR_CAPACITY
	batteryUnitsLeft = BATTERY_CAPACITY

	randomEvent = input_payload.get("random_event")
	buildingLoads = input_payload.get("buildingLoads")
	forecast = input_payload.get("forecast")
	gridPrice = input_payload.get("grid_price")

	# LOOP FOR SOLAR

	# LOOP FOR BATTERY + GRID