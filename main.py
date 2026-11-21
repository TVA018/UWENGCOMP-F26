import schema

def process(input_payload: schema.InputPayload) -> schema.ReturnPayload:
	randomEvent = input_payload.get("random_event")
	buildingLoads = input_payload.get("buildingLoads")
	forecast = input_payload.get("forecast")
	gridPrice = input_payload.get("grid_price")
	pass