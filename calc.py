import argparse
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

def main(args):
    geolocator = Nominatim(user_agent="Carbon Neutral Calculator")
    location = geolocator.geocode(args.hq)
    hq = (location.latitude, location.longitude)

    pubs = {}
    locations = {}
    with open('./conferences.txt') as f:
        for line in f:
            conference, location = line.strip().split(';')
            pubs[conference] = location



    flights = []
    with open(args.pubs) as f:
        for line in f:
            count, conference = line.strip().split(',')
            conference = conference.strip()
            if conference not in pubs:
                print('Add conference and location to conferences.txt first!')
                print(conference)
                assert conference in pubs

            if conference not in locations:
                loc = geolocator.geocode(pubs[conference])
                locations[conference] = (loc.latitude, loc.longitude)
            for i in range(int(count)):
                flights.append(locations[conference])

    travel_kg = 0
    for flight in flights:
        km = geodesic(hq, flight).km
        travel_kg += get_carbon_for_flight(km)

    travel_kg *= args.avg_people_per_conference

    print('Your lab emitted {0:.2f} tons of CO2 equivalent for your conferences travels.'.format(travel_kg/1000.))

    kg_gpu = get_carbon_gpus(args)
    print('Your lab emitted {0:.2f} tons of CO2 equivalent by using GPUs'.format(kg_gpu/1000.))
    other_kg = args.other_emissions_fraction*(kg_gpu+travel_kg)
    total_kg = other_kg + kg_gpu + travel_kg
    print('If GPU and conference emissions make up {0}% of your carbon footprint\nthen the lab emitted a total of {1:.2f} tons of CO2 equivalent.'.format(100*(1.0-args.other_emissions_fraction), total_kg/1000.))


def get_carbon_for_flight(km):
    # Source: http://www.co2list.org/files/carbon.htm#RANGE!A175
    return 164 + (3268*((1.0000791**km)**-1))


def get_carbon_gpus(args):
    # Source 1: http://www.co2list.org/files/carbon.htm#RANGE!A175 230g per MJ -> 0.828 g per KwH
    # Source 2: https://carbonfund.org/how-we-calculate/ 0.5925 kg per kWh
    # I take the average here which is 0.71025 kg per kWh
    kg_per_kWH = 0.71025
    num_gpus = args.num_gpus
    kwatt = args.avg_gpu_watt/1000.
    util = args.avg_gpu_util
    total_watt = num_gpus*kwatt*util
    hours_in_year = 24*365
    return hours_in_year*total_watt*kg_per_kWH




if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--hq', default='Seattle', type=str, help='The city name where your lab is based. This is for travel to conferences.')
    p.add_argument('--pubs', default='./xlab.txt', type=str, help='The text file which contains the list of conferences.')
    p.add_argument('--avg_people_per_conference', default=2.0, type=float, help='How many people do on average travelt to conferences.')
    p.add_argument('--num_gpus', default=10, type=int, help='The number of GPUs in the lab.')
    p.add_argument('--avg_gpu_watt', default=250, type=int, help='The average wattage of all GPUs in the lab')
    p.add_argument('--avg_gpu_util', default=0.75, type=float, help='The average utilization of all GPUs in the lab')
    p.add_argument('--other_emissions_fraction', type=float, default=0.2, help='This is the fraction of all other emissions of your lab that are not from GPUs or conferences. This can be food, paper for printing, and others. The default value of 0.2 is quite conservative.')
    args = p.parse_args()
    main(args)
