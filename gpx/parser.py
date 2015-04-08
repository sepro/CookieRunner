#!/usr/bin/env python3

import argparse

from xml.etree import ElementTree as etree 
from math import pi, sin, cos, acos
from datetime import datetime as dt

def deg2rad(degrees):
    return (pi * degrees) / 180

def rad2deg(radians):
    return (radians * 180)/pi

def gpxDistance(lat1, lon1, lat2, lon2):
    theta = lon1 - lon2
    rads = sin(deg2rad(lat1)) * sin(deg2rad(lat2)) +  cos(deg2rad(lat1)) * cos(deg2rad(lat2)) * cos(deg2rad(theta))
    rads = acos(rads);

    # multiply by radius of the earth to get distance
    return rads * 6367

class GPXParser:
    data = []

    def __init__(self):
        self.data = []
    
    def read(self, filename):
        tree = etree.parse(filename)
        root = tree.getroot()
    
        # Only consider first trk ! 
        trk = root.find('{http://www.topografix.com/GPX/1/1}trk')
        for segID, trkseg in enumerate(trk.findall('{http://www.topografix.com/GPX/1/1}trkseg')):
            segment = []
            for ptID, trkpt in enumerate(trkseg.findall('{http://www.topografix.com/GPX/1/1}trkpt')):
                point = {}

                point["segID"] = segID
                point["ptID"] = ptID
                point["lon"] = float(trkpt.attrib["lon"])
                point["lat"] = float(trkpt.attrib["lat"])

                point["ele"] = 0
                point["time"] = 0

                ele = trkpt.find('{http://www.topografix.com/GPX/1/1}ele')
                if not ele is None:
                    point["ele"] = float(ele.text)
                else:
                    point["ele"] = None
            

                time = trkpt.find('{http://www.topografix.com/GPX/1/1}time')
                if not time is None:
                    point["time"] = time.text.replace('T', ' ').replace('Z', '')
                else:
                    point["time"] = None
                
                # print(point)
                segment.append(point)
                
            self.data.append(segment)


def parseGPX(filename):

    tree = etree.parse(filename)
    root = tree.getroot()
 
    data = []
 
    # Only consider first trk ! 
    trk = root.find('{http://www.topografix.com/GPX/1/1}trk')
    for segID, trkseg in enumerate(trk.findall('{http://www.topografix.com/GPX/1/1}trkseg')):
        segment = []
        for ptID, trkpt in enumerate(trkseg.findall('{http://www.topografix.com/GPX/1/1}trkpt')):
            point = {}

            point["segID"] = segID
            point["ptID"] = ptID
            point["lon"] = float(trkpt.attrib["lon"])
            point["lat"] = float(trkpt.attrib["lat"])

            point["ele"] = 0
            point["time"] = 0

            ele = trkpt.find('{http://www.topografix.com/GPX/1/1}ele')
            if not ele is None:
                point["ele"] = float(ele.text)
            else:
                point["ele"] = None
        

            time = trkpt.find('{http://www.topografix.com/GPX/1/1}time')
            if not time is None:
                point["time"] = time.text.replace('T', ' ').replace('Z', '')
            else:
                point["time"] = None
            
            # print(point)
            segment.append(point)
            
        data.append(segment)

    return data

def getDistance(gpxData):

    totalDistance = 0

    for segment in gpxData:
        segmentDistance = 0
        
        lastLon = None
        lastLat = None

        for point in segment:
            currentLon = point["lon"]
            currentLat = point["lat"]

            # in case data is missing skip point !
            if currentLon is None or currentLat is None:
                continue

            # the first valid element is processed, get distance
            if not (lastLon is None or lastLat is None):
                distance = gpxDistance(lastLat, lastLon, currentLat, currentLon) 
                segmentDistance = segmentDistance + distance

            lastLon = currentLon
            lastLat = currentLat

        totalDistance = totalDistance + segmentDistance

    return totalDistance

def getTime(gpxData):

    totalTime = 0
    for segment in gpxData:
        segmentTime = 0
        
        lastTime = None

        for point in segment:
            currentTime = point["time"]

            # in case data is missing skip point !
            if currentTime is None:
                continue

            # the first valid element is processed, get distance
            if not (lastTime is None):
                a = dt.strptime(lastTime, "%Y-%m-%d %H:%M:%S")
                b = dt.strptime(currentTime, "%Y-%m-%d %H:%M:%S")
                timeDiff = b - a
                segmentTime = segmentTime + timeDiff.seconds

            lastTime = currentTime

        totalTime = totalTime + segmentTime

    return totalTime

def getClimb(gpxData):

    totalClimb = 0
    for segment in gpxData:
        segmentClimb = 0
        
        lastHeight = None

        for point in segment:
            currentHeight = point["ele"]

            # in case data is missing skip point !
            if currentHeight is None:
                continue

            # the first valid element is processed, get distance
            if not (lastHeight is None):
                if (currentHeight > lastHeight):
                    segmentClimb = segmentClimb + (currentHeight - lastHeight)

            lastHeight = currentHeight

        totalClimb = totalClimb + segmentClimb

    return totalClimb



# Start main function

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python script to parse gpx files (total distance, time, speed, ...)')

    parser.add_argument('input', type=str, help='GPX file to analyze')

    args = parser.parse_args()    

    gpxParser = GPXParser()

    gpxParser.read(args.input)

    loggedDistance = getDistance(gpxParser.data)
    loggedTime = getTime(gpxParser.data)
    loggedClimb = getClimb(gpxParser.data)

    loggedCalories = 76*0.862911*loggedDistance

    avgSpeed = loggedDistance*3600/loggedTime

    hours = loggedTime // 3600
    minutes = (loggedTime % 3600)//60
    seconds = (loggedTime % 3600) % 60

 
    print("Distance:", loggedDistance, "km")
    print("Time: ", hours, ':' , minutes, ':', seconds, sep='')
    print("Speed:", avgSpeed, "km/h")
    print("Climb:", loggedClimb, " m")
    print("Calories:", loggedCalories, "Cal")
    

