from argparse import ArgumentParser
from travelplanner import Passenger, Route, Journey


def process():

    parser = ArgumentParser(description='travelplanner')

    parser.add_argument('passengers_csv', type=str,
                        help='Gives the pathname to the Passengers CSV file.')
    parser.add_argument('route_csv', type=str,
                        help='Gives the pathname to the Route CSV file.')
    parser.add_argument('--bus_speed', default=10, type=int,
                        help='The assigned speed of the bus.')
    parser.add_argument('--saveplots', default=False,
                        help='Gives the option to save plots.')

    arguments = parser.parse_args()


if __name__ == "__main__":
    process()
