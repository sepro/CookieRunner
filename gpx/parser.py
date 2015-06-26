#!/usr/bin/env python3

import argparse

from xml.etree import ElementTree
from math import sin, cos, acos, radians
from datetime import datetime as dt


def gpx_distance(lat1, lon1, lat2, lon2):
    """
    Gives the distance between two gpx positions in kilometer (km)

    :param lat1: latitude of the first position
    :param lon1: longitude of the first position
    :param lat2: latitude of the second position
    :param lon2: longitude of the second position
    :return: the distance between both points in kilometer (km)
    """
    theta = lon1 - lon2
    rads = sin(radians(lat1)) * sin(radians(lat2)) + cos(radians(lat1)) * cos(radians(lat2)) * cos(radians(theta))
    rads = acos(rads)

    # multiply by radius of the earth to get distance
    return rads * 6367


class GPXParser:

    data = []

    def __init__(self):
        self.data = []

    def read(self, filename):
        """
        reads a gpx file. The required information is stored in self.data

        :param filename: path to the file to read
        """
        tree = ElementTree.parse(filename)
        root = tree.getroot()

        # Only consider first trk ! 
        trk = root.find('{http://www.topografix.com/GPX/1/1}trk')
        for segID, trkseg in enumerate(trk.findall('{http://www.topografix.com/GPX/1/1}trkseg')):
            segment = []
            for ptID, trkpt in enumerate(trkseg.findall('{http://www.topografix.com/GPX/1/1}trkpt')):
                point = {
                    "segID": segID,
                    "ptID": ptID,
                    "lon": float(trkpt.attrib["lon"]),
                    "lat": float(trkpt.attrib["lat"]),
                    "ele": 0,
                    "time": 0
                }

                ele = trkpt.find('{http://www.topografix.com/GPX/1/1}ele')
                if ele is not None:
                    point["ele"] = float(ele.text)
                else:
                    point["ele"] = None

                time = trkpt.find('{http://www.topografix.com/GPX/1/1}time')
                if time is not None:
                    point["time"] = time.text.replace('T', ' ').replace('Z', '')
                else:
                    point["time"] = None

                # print(point)
                segment.append(point)

            self.data.append(segment)

    def total_calories(self, weight=75):
        """
        Calculates the amount of Calories burnt running the track in the gpx file.

        :param weight: The weight of the runner in kilogram (kg, default 75 kg)
        :return: Calories burnt in Cal (kcal)
        """
        return weight * 0.862911 * self.total_distance

    @property
    def total_distance(self):
        """
        Calculates the length of the track in the gpx file in kilometer (km)

        :return: total length of the gpx file in kilometer
        """
        distance = 0

        for segment in self.data:
            segment_distance = 0

            last_lon = None
            last_lat = None

            for point in segment:
                current_lon = point["lon"]
                current_lat = point["lat"]

                # in case data is missing skip point !
                if current_lon is None or current_lat is None:
                    continue

                # the first valid element is processed, get distance
                if not (last_lon is None or last_lat is None):
                    d = gpx_distance(last_lat, last_lon, current_lat, current_lon)
                    segment_distance += d

                last_lon = current_lon
                last_lat = current_lat

            distance += segment_distance

        return distance

    @property
    def total_time(self):
        """
        Calculates in which time the gpx track was completed.

        :return: Time it took to complete the track in seconds (s)
        """
        time = 0
        for segment in self.data:
            segment_time = 0

            last_time = None

            for point in segment:
                current_time = point["time"]

                # in case data is missing skip point !
                if current_time is None:
                    continue

                # the first valid element is processed, get distance
                if not (last_time is None):
                    a = dt.strptime(last_time, "%Y-%m-%d %H:%M:%S")
                    b = dt.strptime(current_time, "%Y-%m-%d %H:%M:%S")
                    time_difference = b - a
                    segment_time += time_difference.seconds

                last_time = current_time

            time += segment_time

        return time

    @property
    def total_climb(self):
        """
        Calculates how many meters the track climbed up in meters (m).

        :return: total climb in meter (m)
        """
        climb = 0
        for segment in self.data:
            segment_climb = 0

            last_height = None

            for point in segment:
                current_height = point["ele"]

                # in case data is missing skip point !
                if current_height is None:
                    continue

                # the first valid element is processed, get distance
                if last_height is not None and current_height > last_height:
                    segment_climb += (current_height - last_height)

                last_height = current_height

            climb += segment_climb

        return climb

    @property
    def average_speed(self):
        """
        Calculates the average speed at which the track was completed

        :return: average speed in kilometer/hour
        """
        return self.total_distance * 3600 / self.total_time



# Start main function

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python script to parse gpx files (total distance, time, speed, ...)')

    parser.add_argument('input', type=str, help='GPX file to analyze')

    args = parser.parse_args()

    gpxParser = GPXParser()

    gpxParser.read(args.input)

    loggedDistance = gpxParser.total_distance
    loggedTime = gpxParser.total_time
    loggedClimb = gpxParser.total_climb

    loggedCalories = 76 * 0.862911 * loggedDistance

    avgSpeed = loggedDistance * 3600 / loggedTime

    hours = loggedTime // 3600
    minutes = (loggedTime % 3600) // 60
    seconds = (loggedTime % 3600) % 60

    print("Distance:", loggedDistance, "km")
    print("Time: ", hours, ':', minutes, ':', seconds, sep='')
    print("Speed:", avgSpeed, "km/h")
    print("Climb:", loggedClimb, " m")
    print("Calories:", loggedCalories, "Cal")
