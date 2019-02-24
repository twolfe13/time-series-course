# import matplotlib.pyplot as plt
import numpy as np

import tools 

def get_data():
    """
    
    Parameters 
    ----------
    none
    
    Returns
    --------
    temps: arrary of floats
    year, month, day: array of ints
    
    
    
    """
# 1) LOAD THE DATA

# predict_weather.py

# Read in the data
    weather_filename = 'weather_predictor/fort_lauderdale.csv'
    weather_file = open(weather_filename)
    weather_data = weather_file.read()
    weather_file.close()

#At this point, the whole file is just a single string of characters


# Inspect briefly

# print(len(weather_data))
# print(weather_data[:200])


# Break weather records into lines using .split()
    lines = weather_data.split('\n')
    labels = lines[0]
    values = lines[1:]
    n_values = len(values)

#CONGRATULATIONS!  The data is now read in, loaded, and ready to work with! (the column titles are saved as 'labels' and data as 'values')

#Print the first 10 values
# print(labels)
#for i in range(10):
#    print(values[i])
    

# 2) CONVERT THE DATA TO LISTS: Break the list of comma-separate value strings (into days, temps, etc.) into lists of values.

    year = []
    month = []
    day = []
    max_temp = []
#To keep the data clear, we'll call out the column number of each label
    j_year = 1
    j_month = 2
    j_day = 3
    j_max_temp = 5

#Loop for each list | note: strings from lists converted into numbers (integers)

    for i_row in range(n_values):
    #we'll use split_values again, but this time splitting on commas - this gives us back a list of strings that fall between each of the commas
        split_values = values[i_row].split(',')
    #then as we step through each day in the data set, we'll add it's year, month, day, and max temp. to the respective lists. 
        if len(split_values) >= j_max_temp:
        #in doing this, we need to make sure the strings are converted into integers, so we can add, and peform numeric computations with them
            year.append(int(split_values[j_year]))
            month.append(int(split_values[j_month]))
            day.append(int(split_values[j_day]))
        #float interprets the number as a decimal
            max_temp.append(float(split_values[j_max_temp]))

# Examining the days list, and it matches with what we'd expect from before 
#for i_day in range(100): 
#    print(max_temp[i_day])
    
#plt.plot(max_temp)    
#plt.show()


# 3) REPLACE MISSING DATA WITH NaNs

# Isolate the valid recent data, in order to eventually get the 'non-NaN' data (via a midpoint, since we saw most NaNs occur in the middle)

# to find midpoint, find out how long the list is 
    i_mid = len(max_temp) // 2
#put temp data into array, for easier NaN management and more. Grab all values to the right of midpoint (most recent data)
    temps = np.array(max_temp[i_mid:])
# year
    year = year[i_mid:]
# month
    month =month[i_mid:]
# day
    day = day[i_mid:]

#select all places where we have missing values, and subsittue in NaN
    temps[np.where(temps == -99.9)] = np.nan

# Plot data again, representing each data point with a black dot - to see different types of patterns.
#plt.plot(temps, color='black', marker='.', linestyle='none')
#plt.show()


# Remove all the nan's
# Trim both ends and fill nans in the iddle.
# Find the first non-nan.
# Since we chopped the data set in the middle of a bunch of NaN's, we expect the first couple thousand to be NaN's
#print(np.where(np.isnan(temps))[0])
#print(np.where(np.logical_not(np.isnan(temps)))[0][0])
    i_start = np.where(np.logical_not(np.isnan(temps)))[0][0]
    temps = temps[i_start:]
    year = year[i_start:]
    month = month[i_start:]
    day = day[i_start:]

#view location values of all nan's 
    i_nans = (np.where(np.isnan(temps))[0])
#print(i_nans)

# Replace***(!)** all nans with the most recent non-nan. 
    for i in range(temps.size):
        if np.isnan(temps[i]):
            temps[i] = temps[i - 1]
    return (temps, year, month, day)

# CREATING AND UNDERSTANDING FEATURES OF THE MODEL 

# Determine whether the previous day's temperature is 
# related to that of the following day. This is a good feature because previous day's temp is highly related to the following day

#plt.plot(temps[:1], temps[1:], color='black', marker='.', linestyle='none')
#plt.show

# Show the relationship between two variables. 
# 'adding some jitter'... to better show frequency and tendency 



def find_autocorr():
    #shift = 1
#Find the autocorrelation value
    autocorr = []
#for shift in range (# of days.. 1-x # of days)
    for shift in range(1,1000):
        correlation = (np.corrcoef(temps[:-shift], temps[shift:])[1,0])
        autocorr.append(correlation)
#   print(autocorr)
#   plt.plot(autcorr)


def build_temp_calendar(temps, year, month, day):
    """
    Create an arrary of typical temperatures by day-of-year. 
    Day 0 = Jan 1, etc.
    
    Parameters 
    ----------
    temps: arrary of floats
    year, month, day: arrary of ints
    
    Returns
    -------
    median_temp_calendar: array of floats length 366
    """
# start with an array of zero's according to the proper temp. size
    day_of_year = np.zeros(temps.size) 
    for i_row in range(temps.size): 
        day_of_year[i_row] = tools.find_day_of_year(
            year[i_row], month[i_row], day[i_row])

# Create 10-day medians for each day of the year
#we use median instead of mean to avoid outliers skewing our calcs
    median_temp_calendar = np.zeros(366)
    ten_day_medians = np.zeros(temps.size)
    for i_day in range(0, 365):
    # create 10-day window
        low_day = i_day - 5
        high_day = i_day + 4
    
        if low_day < 0:
            low_day += 365
        if high_day > 365:
            high_day += -365
        if low_day < high_day: 
            i_window_days = np.where(
            np.logical_and(day_of_year >= low_day,
            day_of_year <= high_day))
        else: 
            i_window_days = np.where(
            np.logical_or(day_of_year >=low_day,
                day_of_year <= high_day))

        ten_day_median = np.median(temps[i_window_days])
        median_temp_calendar[i_day] = ten_day_median
        ten_day_medians[np.where(day_of_year == i_day)] = ten_day_median
    #Handle '364' years, to be handled the same as normal years, to make things easier
        if i_day ==364: 
            ten_day_medians[np.where(day_of_year == 365)] = ten_day_median
            median_temp_calendar[365] = ten_day_median
    #print(i_day, low_day, high_day, i_window_days[0].size)
#print(ten_day_medians.size, np.unique(ten_day_medians), ten_day_medians)
    return median_temp_calendar


# NEXT STEP: Use temperature calendar to make predictions 

def predict (year, month, day, temperature_calendar):
    """
    For a given day, month, and year, predict 
    the high temperature for Fort Lauderdale Beach.
    
    Parameters
    ----------
    year, month, day: int
        The date of interest
    temperature_calendar: arrary of floats
        The typical temperature for each day of the year
        Jan 1 = 0,etc.
    
    Returns
    -------
    prediction: float
    
    """
    day = tools.find_day_of_year(year, month, day)
    # Looks up the associated temperature, and returns that as a prediction
    prediction = temperature_calendar[day]
    return prediction 
    

if __name__ == '__main__': 
    temps, year, month, day = get_data()
    temp_calendar = build_temp_calendar(temps, year, month, day)
    for test_day in range(1,30): 
        test_year = 2016
        test_month = 6
        prediction = predict(test_year, test_month, test_day, temp_calendar)
        print(test_year, test_month, test_day, prediction)
