from travelplanner.classes import Passenger, Route, Journey
import pytest


def test_walk_time1():
    if Passenger(start=(0, 0), end=(3, 4), speed=5).walk_time() != 25.0:
        raise ValueError('function is invalid')
    else:
        assert True


def test_walk_time2():
    if Passenger(start=(0, 0), end=(6, 8), speed=10).walk_time() != 100.0:
        raise ValueError('function is invalid')
    else:
        assert True


def test_timetable():
    route = Route('travelplanner/path.csv')
    if route.timetable() != {'A': 0, 'B': 180, 'C': 190, 'D': 210, 'E': 280}:
        raise ValueError('wrong')
    else:
        assert True


a = Passenger(start=(0, 4), end=(9, 4), speed=8)
b = Passenger(start=(2, 5), end=(3, 8), speed=12)
c = Passenger(start=(1, 1), end=(5, 7), speed=12)
my_list = [a, b, c]


def test_travel_time():
    if Journey(Route('travelplanner/path.csv'),
               my_list).travel_time(0) != {'bus travel': -280,
                                           'walk travel': 40.0}:
        raise ValueError('travel_time_time() function is incorrect')
    else:
        assert True


def test_generate_cc():
    route = Route('travelplanner/route.csv')
    if route.generate_cc() != ((7, 5), '2200002006444466660'):
        raise ValueError('wrong')
    else:
        assert True


def test_print_time_stats():
    list = Passenger.read_passengers('travelplanner/passenger_information.csv')
    passengers = [
                  Passenger(start, end, speed)
                  for start, end, speed
                  in list]
    route = Route('travelplanner/route.csv')
    trip1 = Journey(route, passengers)
    bus_time, walk_time = trip1.print_time_stats()
    if bus_time != 0 or walk_time != 248.4100464755902:
        raise ValueError('print_time_stats() function is incorrect.')
    else:
        assert True


def test_Passenger1():
    start, end, speed = ((0, 0), (3, 4), 5)
    passenger = Passenger(start, end, speed)
    if passenger.start != (0, 0):
        raise ValueError('your Passenger class appears to be incorrect.')
    if passenger.end != (3, 4):
        raise ValueError('your Passenger class appears to be incorrect.')
    if passenger.speed != 5:
        raise ValueError('your Passenger class appears to be incorrect.')
    else:
        assert True


def test_Passenger2():
    start, end, speed = ((1, 1), (2, 5), 7)
    passenger = Passenger(start, end, speed)
    if passenger.start != (1, 1):
        raise ValueError('your Passenger class appears to be incorrect.')
    if passenger.end != (2, 5):
        raise ValueError('your Passenger class appears to be incorrect.')
    if passenger.speed != 7:
        raise ValueError('your Passenger class appears to be incorrect.')
    else:
        assert True


def test_read_route():
    route = Route('travelplanner/dummy_route.csv')
    expected_route = [(7, 5, 'A'), (7, 4, ''), (7, 3, 'B')]
    if route.read_route() != expected_route:
        raise ValueError('The route does not read the route file correctly.')
    else:
        assert True


def test_read_passengers():
    list = Passenger.read_passengers('travelplanner/dummy_passengers_list.csv')
    A = Passenger(start=(6, 9), end=(4, 23), speed=12)
    passenger_list = [A]

    passengers = [
                  Passenger(start, end, speed)
                  for start, end, speed
                  in list]
    if passengers[0].start != passenger_list[0].start:
        raise ValueError('Passenger class reads the list of passengers wrong')
    if passengers[0].end != passenger_list[0].end:
        raise ValueError('Passenger class reads the list of passengers wrong')
    if passengers[0].speed != passenger_list[0].speed:
        raise ValueError('Passenger class reads the list of passengers wrong')
    else:
        assert True


def test_wrong_route():
    testroute = Route('travelplanner/route.csv')
    with pytest.raises(AssertionError):
        wrong_route = Route('travelplanner/wrong_route.csv')
