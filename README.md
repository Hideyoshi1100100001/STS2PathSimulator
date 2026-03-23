# STS2PathSimulator
A set of scripts that generates maps of Slay the Spire 2 and analyze some interested performance parameters.

Run `python MapGenerator.py` to generate the map structure and save in Maps.json.

Run `python PointAssigner.py` to read the map structures from Maps.json, assign point types and save in AssignedMaps.json.

Run `python Analyzer.py` to read the generated maps from AssignedMaps.json and analyze. The outputs are given by 4 figs and log.txt.
