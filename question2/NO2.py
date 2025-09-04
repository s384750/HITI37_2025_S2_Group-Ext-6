import csv
import glob
import math  # import math for square root in stddev calculation

# Function to read CSV file and return its rows as a list of lists
def read_csv(name):
    with open(name, newline="") as f:
        reader = csv.reader(f)   # create a CSV reader object
        row = list(reader)       # convert reader to list
    return row

# Function to write content (string) to a file
def write_csv(filename, content):
    with open(filename, 'w') as f:
        f.write(content)


# Function to calculate seasonal averages across all station CSV files
def seasonal_averages():
    # functions to calculate average temperature for each season ---
    def avg_temp_summer(file):
        year_avg = 0
        for x in range(1, len(file)):  # skip header row
            # Summer months = May, June, April (columns 4, 5, 15)
            station_avg = (float(file[x][4]) + float(file[x][5]) + float(file[x][15])) / 3
            year_avg += station_avg
        return year_avg / (len(file) - 1)

    def avg_temp_autumn(file):
        year_avg = 0
        for x in range(1, len(file)):
            # Autumn months = July, August, September (columns 6, 7, 8)
            station_avg = (float(file[x][6]) + float(file[x][7]) + float(file[x][8])) / 3
            year_avg += station_avg
        return year_avg / (len(file) - 1)

    def avg_temp_winter(file):
        year_avg = 0
        for x in range(1, len(file)):
            # Winter months = October, November, December (columns 9, 10, 11)
            station_avg = (float(file[x][9]) + float(file[x][10]) + float(file[x][11])) / 3
            year_avg += station_avg
        return year_avg / (len(file) - 1)

    def avg_temp_spring(file):
        year_avg = 0
        for x in range(1, len(file)):
            # Spring months = January, February, March (columns 12, 13, 14)
            station_avg = (float(file[x][12]) + float(file[x][13]) + float(file[x][14])) / 3
            year_avg += station_avg
        return year_avg / (len(file) - 1)

    #  Process all CSV files inside 'temperatures/' folder
    filepath = glob.glob('temperatures/*.csv')

    total_summer_avg = 0
    total_autumn_avg = 0
    total_winter_avg = 0
    total_spring_avg = 0

    # Loop through each file and accumulate seasonal averages
    for x in filepath:
        stations = read_csv(x)
        total_summer_avg += avg_temp_summer(stations)
        total_autumn_avg += avg_temp_autumn(stations)
        total_winter_avg += avg_temp_winter(stations)
        total_spring_avg += avg_temp_spring(stations)

    # Divide totals by number of files to get overall averages
    summer_avg = total_summer_avg / len(filepath)
    autumn_avg = total_autumn_avg / len(filepath)
    winter_avg = total_winter_avg / len(filepath)
    spring_avg = total_spring_avg / len(filepath)

    # Format results
    season_avg = (
        f"Summer = {summer_avg:.1f}°C \n"
        f"Autumn = {autumn_avg:.1f}°C \n"
        f"Winter = {winter_avg:.1f}°C \n"
        f"Spring = {spring_avg:.1f}°C "
    )

    # Save results to file
    write_csv("average_temp.txt", season_avg)


# Function to calculate temperature range (max - min) for each station
def temp_range():
    filepath = glob.glob('temperatures/*.csv')
    station_list = []          # list to store final results
    station_dict = {}          # dictionary to track largest range per station

    # Process each CSV file
    for x in filepath:
        station_group = read_csv(x)

        # Loop through each station row (skip header row)
        for y in range(1, len(station_group)):
            station = station_group[y][0]                      # station name
            temps = list(map(float, station_group[y][-12:]))   # last 12 columns = monthly temps

            high = max(temps)      # max temperature
            low = min(temps)       # min temperature
            Range = high - low     # temperature range

            # Update dictionary if station not seen before OR if range is larger
            if station not in station_dict or Range > station_dict[station]["range"]:
                station_dict[station] = {"range": Range, "max": high, "min": low}

    # Build formatted result lines for each station
    for station, values in station_dict.items():
        words = f"{station}: Range {values['range']:.1f}°C (Max: {values['max']}°C, Min: {values['min']}°C)"
        station_list.append(words)

    # Write results to file
    with open("largest_temp_range_station.txt", "w") as f:
        for item in station_list:
            f.write(item + "\n")


# Function to calculate stability (standard deviation) of temperatures for each station
def temp_stability():
    filepath = glob.glob('temperatures/*.csv')   # get all CSV files
    station_dict = {}                            # store all temperatures per station

    #Gather temperatures for each station across all files
    for x in filepath:
        station_group = read_csv(x)

        for y in range(1, len(station_group)):   # skip header row
            station = station_group[y][0]        # station name
            temps = list(map(float, station_group[y][-12:]))   # monthly temps

            if station not in station_dict:
                station_dict[station] = []       # initialize list if new station

            station_dict[station].extend(temps)  # add temps for this station

    # Compute standard deviation for each station
    station_stddev = {}
    for station, temps in station_dict.items():
        mean = sum(temps) / len(temps)                       # mean temperature
        variance = sum((t - mean) ** 2 for t in temps) / len(temps)  # variance
        stddev = math.sqrt(variance)                         # standard deviation
        station_stddev[station] = stddev                     # save result

    #  Find min and max stddev
    min_std = min(station_stddev.values())
    max_std = max(station_stddev.values())

    #  Handle ties by collecting all stations with min/max values
    most_stable = [s for s, v in station_stddev.items() if abs(v - min_std) < 1e-9]
    most_variable = [s for s, v in station_stddev.items() if abs(v - max_std) < 1e-9]

    # Build results in required format
    result_lines = []
    for station in most_stable:
        result_lines.append(f"Most Stable: {station}: StdDev {min_std:.1f}°C")
    for station in most_variable:
        result_lines.append(f"Most Variable: {station}: StdDev {max_std:.1f}°C")

    # Save results to text file
    with open("temperature_stability_stations.txt", "w") as f:
        for line in result_lines:
            f.write(line + "\n")


# Run all functions
temp_stability()
temp_range()
seasonal_averages()
