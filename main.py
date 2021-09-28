import requests
import json
from datetime import datetime
import time

URL = "https://www.ulgeauxride.com/Services/JSONPRelay.svc/"

def get_time():
    global incidents_clean
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return str(date_time)



def get_map_vehicle_points():
    """Returns the location of all of the vehicles on route """
    response = requests.get(URL + "GetMapVehiclePoints")
    json_dict = json.loads(response.text) 
    return json_dict



def bus_running_count():
    map_points = get_map_vehicle_points()
    busses_running = 0
    for bus in range(len(map_points)):
        if map_points[bus]['IsOnRoute'] == True:
            busses_running += 1
    return str(busses_running)


def get_route_id(route_id):
    routes = {"1" : "Vermilion Route", "20" : "Bus 444"}
    return routes[route_id]



def get_specific_bus_info(bus_id):
    map_points = get_map_vehicle_points()
    for bus in range(len(map_points)):
        if map_points[bus]['VehicleID'] == bus_id:
            print("-" * 20)
            print(f"Bus:          {map_points[bus]['Name'] }")
            print(f"Route ID:     {get_route_id(str(map_points[bus]['RouteID']))}")
            print(f"Ground Speed: {map_points[bus]['GroundSpeed']}")
            print(f"Is On Route:  {map_points[bus]['IsOnRoute']}")
            print(f"Is Delayed:   {map_points[bus]['IsDelayed']}")    


def bus_report():
    map_points = get_map_vehicle_points()
    for bus in range(len(map_points)):
        print("-" * 20)
        print(f"Bus:          {map_points[bus]['Name'] }")
        print(f"Route ID:     {get_route_id(str(map_points[bus]['RouteID']))}")
        print(f"Ground Speed: {map_points[bus]['GroundSpeed']}")
        print(f"Is On Route:  {map_points[bus]['IsOnRoute']}")
        print(f"Is Delayed:   {map_points[bus]['IsDelayed']}")
    print("-" * 20)
    print("-" * 20)
    print(f"There are {bus_running_count()} busses running at {get_time()}")
    print()


def show_all_data():
    map_points = get_map_vehicle_points()
    print(json.dumps(map_points, indent=4))


def menu():
    menu_select = input('''
    - UL BUS THINGIE 1.6 -

    1. Show All Busses
    2. Show Specific Bus
    3. Show All Raw Data
    Please Select a Number: ''')
    

    if menu_select == "1":
        refresh_time = input("Enter number of seconds to refresh data: ")
        while True:
            bus_report()
            time.sleep(int(refresh_time))
            print("#", end = '', flush=True)

    elif menu_select == "2":
        bus_id = input("Enter the bus ID number: ")
        refresh_time = input("Enter number of seconds to refresh data: ")
        
        while True: 
            get_specific_bus_info(int(bus_id))
            time.sleep(int(refresh_time))
            print("#", end = '', flush=True)
    
    elif menu_select == "3":
        show_all_data()


menu()
