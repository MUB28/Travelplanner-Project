import math
import numpy as np
import csv
import matplotlib.pyplot as plt


class Passenger:
    def __init__(self, start, end, speed):
        self.start = start
        self.end = end
        self.speed = speed

    def walk_time(self):

        """ Calulates the time taken if a passenger walked

        Returns
        --------
        float
            Time the passenger walks

        Example
        -------
        >>> John = Passenger(start=(20,20), end=(23,24), speed=5)
        >>> John.walk_time()
        25.0
        """
        ams = (np.sqrt((self.end[1]-self.start[1])**2 +
               (self.end[0]-self.start[0])**2))*(self.speed)
        return(ams)

    def read_passengers(self):
        output = []
        with open(self, 'r') as csv_file:
            for i in csv_file:
                line_data = i.split(',')
                output.append(((int(line_data[0]), int(line_data[1])),
                               (int(line_data[2]), int(line_data[3])),
                               int(line_data[4])))
        return output


class Route:
    def __init__(self, filename, bus_speed=10):
        self.filename = filename
        self.bus_speed = bus_speed
        self.read_route()
        self.route = self.read_route()
        chain_code = self.generate_cc()
        for el in chain_code[1]:
            assert int(el) % 2 == 0, "Diagonal moves are not allowed"

    def read_route(self):
        outing = []
        with open(self.filename, 'r') as filestream:
            for i in filestream:
                line_data = i.split(',')
                outing.append((int(line_data[0]),
                               int(line_data[1]), (line_data[2][0:-1])))
        return outing

    def get_route(self):
        return(self.route)

    def plot_map(self):
        max_x = max([n[0] for n in self.route]) + 5
        max_y = max([n[1] for n in self.route]) + 5
        grid = np.zeros((max_y, max_x))
        for x, y, stop in self.route:
            grid[y, x] = 1
            if stop:
                grid[y, x] += 1
        fig, ax = plt.subplots(1, 1)
        ax.pcolor(grid)
        ax.invert_yaxis()
        ax.set_aspect('equal', 'datalim')
        plt.show()

    def timetable(self):
        time = 0
        stops = {}
        for step in self.route:
            if step[2]:
                stops[step[2]] = time
            time += self.bus_speed
        return stops

    def generate_cc(self):

        start = self.route[0][:2]
        cc = []
        freeman_cc2coord = {0: (1, 0),
                            1: (1, -1),
                            2: (0, -1),
                            3: (-1, -1),
                            4: (-1, 0),
                            5: (-1, 1),
                            6: (0, 1),
                            7: (1, 1)}
        freeman_coord2cc = {val: key for key, val in freeman_cc2coord.items()}
        for b, a in zip(self.route[1:], self.route):
            x_step = b[0] - a[0]
            y_step = b[1] - a[1]
            cc.append(str(freeman_coord2cc[(x_step, y_step)]))
        return start, ''.join(cc)


class Journey(Route, Passenger):

    def __init__(self, route, passengers, bus_speed=10):
        self.passengers = passengers
        self.bus_travel_time = {}
        self.route = route.route
        self.bus_speed = bus_speed

    def passenger_trip(self, passenger):

        stops = [value for value in (self.route) if value[2]]

        distances_start = [(math.sqrt((x - passenger.start[0])**2 +
                                      (y - passenger.start[1])**2), stop)
                           for x, y, stop in stops]

        distances_start.reverse()
        closer_start = min(distances_start)

        distances = [(math.sqrt((x - passenger.end[0])**2 +
                                (y - passenger.end[1])**2), stop)
                     for x, y, stop in stops]
        closer_end = min(distances)
        return (closer_start, closer_end)

    def plot_bus_load(self):
        stops = {step[2]: 0 for step in self.route if step[2]}
        for passenger in self.passengers:
            trip = self.passenger_trip(passenger)
            stops[trip[0][1]] += 1
            stops[trip[1][1]] -= 1
            for i, stop in enumerate(stops):
                if i > 0:
                    stops[stop] += stops[prev]
                prev = stop
            fig, ax = plt.subplots()
            ax.step(range(len(stops)), list(stops.values()), where='post')
            ax.set_xticks(range(len(stops)))
            ax.set_xticklabels(list(stops.keys()))
            plt.show()

    def id(self, x):
        output = self.passengers[x]
        return(output)

        # id() function associates every passenger
        # in my passengers list with a number.
        # travel_time() function returns the
        # time a passenger spent on the bus and walking.
        # plot_bus_load() function plots and displays a graph of the number of passengers on the bus as it moves
        # along the route.  

    def travel_time(self, ID):
        identification = self.id(ID)
        walk_distance_stops = self.passenger_trip(identification)
        bus_times = self.timetable()
        bus_travel = bus_times[walk_distance_stops[1][1]] - \
            bus_times[walk_distance_stops[0][1]]
        walk_travel = walk_distance_stops[0][0] * identification.speed + \
            walk_distance_stops[1][0] * identification.speed

        if identification.walk_time() < bus_travel + walk_travel:
            trip_information = {'bus travel': 0,
                                'walk travel': identification.walk_time()}

        else:
            trip_information = {'bus travel': bus_travel,
                                'walk travel': walk_travel}

        return(trip_information)

    def print_time_stats(self):
        total_bus_time = 0
        total_walk_time = 0
        for i in range(len(self.passengers)):
            total_bus_time += self.travel_time(i)['bus travel']
            total_walk_time += self.travel_time(i)['walk travel']
        average_walk_time = (total_walk_time)/len(self.passengers)
        average_bus_time = (total_bus_time)/len(self.passengers)

        print("Average time on bus:", average_bus_time,
              "mins" '\n' "Average walking time:", average_walk_time, "mins")
        return(average_bus_time, average_walk_time)

        # print_time_stats() function prints the
        # average time a passenger spends walking and on the bus.
