# To use this, you need to create an empty JSON file with the following structure:
# {"stations": {}}


import requests
from datetime import datetime
import time
import json


def get_stations_occupancy():
    url = "https://stockholmebikes.se/map?_data=routes/map"

    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8,sv-SE;q=0.5,sv;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://stockholmebikes.se/map/detail/5555380e-c81f-4e7f-a303-32d39396e50c',
        'Connection': 'keep-alive',
        'Cookie': '_dd_s=rum=1&id=0740abd4-1d54-4547-bd61-3c9685e615e9&created=1652735995181&expire=1652738019082',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'DNT': '1',
        'Sec-GPC': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    date = time.time()
    resJson = response.json()
    data = resJson['mobilityOptions']['data']
    for station in data:
        if (station['type'] == 'station-options'):
            coord = station['attributes']['leg']['from']['coord']

            id = station['id']
            occupancy = station['attributes']['occupancy']
            capacity = station['attributes']['capacity']
            mStation = {'coord': coord,
                        'occupancy': occupancy, 'capacity': capacity, 'date': date}
            write_json(mStation, id, 'stationsMonday.json')


def write_json(new_data, id, filename='stations.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)

        if id in file_data['stations']:
            new_data.pop('coord', None)
            file_data['stations'][id]['data'].append(new_data)
        else:
            coord = new_data['coord']
            new_data.pop('coord', None)
            file_data['stations'][id] = {
                'id': id, 'coord': coord, 'data': [new_data]}
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


def run(condition):
    
    def task():
        get_stations_occupancy()
        print("Data taken at:", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

    while condition == True:
        # Wait 1 second until we are synced up with the 'every 15 minutes' clock
        while datetime.now().minute not in {0, 15, 30, 45}:
            time.sleep(1)
            print("waiting, and loggin in", 15 -
                (datetime.now().minute % 15), "minutes", end="\r")
        task()
        time.sleep(60*2)  # Wait for 2 minutes so it doesn't trigger twice
        


run(True)
# get_stations_occupancy()
