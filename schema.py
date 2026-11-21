from typing import Literal, TypedDict

type RandomEvent = Literal["none", "cloudy_weather", "generator_failure", "battery_failure", "grid_failure"]
type Forecast = Literal["cloudy", "not cloudy"]
type BuildingType = Literal["library", "laboratory", "lecture_hall", "student_centre", "student_residence"]

class BuildingLoad(TypedDict):
    buildingType: BuildingType
    load: int

class ElectricityAllocation(TypedDict):
    solar: int
    battery: int
    grid: int

class InputPayload(TypedDict):
    random_event: RandomEvent
    forecast: Forecast
    buildingLoads: list[BuildingLoad]
    grid_price: float

class ReturnPayload(TypedDict):
    buildings: list[ElectricityAllocation]
    generator: int