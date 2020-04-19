import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!  Your input can be uppercase or lowercase')
    print('Please spell out the name of city, month, day, etc... as you make your selections')
    cityname = ["chicago", "new york", "washington"]
    choices = ['month', 'day', 'both','none']
    monthchoice = ['january', 'february', 'march', 'april', 'may', 'june']
    daychoice = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
    city = input("Would you like to see data for Chicago, New York, or Washington?").lower()
    month = 'all'
    day = 'all'
    while city not in cityname:
        city = input("Please type city name like: chicago ... ").lower()
    mon_date_both = input("Would you like to filter the data by month, day, both, or 'none' for not at all?").lower()
    if mon_date_both == 'none':
        print("You have chosen no filters")
    else:
        while mon_date_both not in choices:
            mon_date_both = input("Please type: month, day, both, or none ... ").lower()
        if mon_date_both == 'both':
            month = input("Which month - January, February, March, April, May, or June?").lower()
            while month not in monthchoice:
                month = input("Please type the month like: june ... ")
            day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?").lower()
            while day not in daychoice:
                day =  input("Please type the day like: sunday ... ").lower()
        elif mon_date_both == 'month':
            month = input("Which month - January, February, March, April, May, or June?").lower()
            while month not in monthchoice:
                month = input("Please type the month like: june ... ").lower()
        elif mon_date_both == 'day':
            day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?").lower()
            while day not in daychoice:
                day =  input("Please type the day like: sunday ... ").lower()
    return city, month, day
"""=========================================================================="""

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1  #get index number of string position
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df
"""=========================================================================="""
""" This function will write all data to a file"""
def writefile(data):
    with open("all4questions.txt", 'a') as file_out:
        file_out.write(data + '\n')

"""=========================================================================="""

""" From the dataframe, get Popular times of travel """
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    writefile('-'*50)
    writefile('Calculating The Most Frequent Times of Travel...')

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    # get the most common month
    df['month2'] = df['month'].apply(lambda x: calendar.month_abbr[x])
    monthct = df['month2'].mode()[0]
    # get the most common day of week
    dayoftheweek = df['day_of_week'].mode()[0]
    # get the most common start hour
    popular_hour = str(df['hour'].mode()[0])
    #print('Most popular Start Hour: ', popular_hour)
    writefile("1) Most common month:       " + monthct)
    writefile("2) Most common day of week: " + dayoftheweek)
    writefile("3) Most common Hour:        " + popular_hour)

"""=========================================================================="""
""" From the dataframe, get Popular stations and trip information """
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    writefile('-'*50)
    writefile('Calculating The Most Popular Stations and Trip...')
    # display most commonly used start station
    count_commonstart = df['Start Station'].mode()[0]
    # display most commonly used end station
    count_commonend = df['End Station'].mode()[0]
    # display most frequent combination of start station and end station trip
    df['start_and_end'] = df['Start Station'] + ' , ' + df['End Station']
    count_start_and_end = df['start_and_end'].mode()[0]
    writefile("1) Most common start station:          " + count_commonstart)
    writefile("2) Common End Station:                 " + count_commonend)
    writefile("3) Most common trip from start to end: " + count_start_and_end)

"""=========================================================================="""
""" From the dataframe, get Trip duration information """
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    writefile('-'*50)
    writefile('Calculating Trip Duration...')
    start_time = time.time()
    # display total travel time
    total_travel_time_duration = str(df['Trip Duration'].sum())
    # display mean travel time
    average_travel_time_duration = str(df['Trip Duration'].mean())
    writefile("1) Total travel time:   " + total_travel_time_duration)
    writefile("2) Average travel time: " + average_travel_time_duration)

"""=========================================================================="""
""" From the dataframe, get User info information. The count for gender and
    the earliest, most recent, most common year of birth are not available
    for Washington """
def user_stats(df,city):
    """Displays statistics on bikeshare users."""
    writefile('-'*50)
    writefile('Calculating User Stats...')
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df['date'] = df['Start Time'].dt.date
    # get counts of user types
    user_types =str(df['User Type'].value_counts())
    writefile("1) Counts of each user type:" + user_types)
    if city != "washington":
        # get counts of gender
        gender_types =str(df['Gender'].value_counts())
        writefile("2) Counts of each gender:" + gender_types)
        # Display earliest, most recent, and most common year of birth
        popular_year_birth = (df['Birth Year'].mode()[0])
        df = df[df['Birth Year'] == popular_year_birth]
        df = df.sort_values(by=['hour','date'], ascending = [True,False])
        earliest = str(df['hour'].min())
        getdatevalue = str(df.iloc[0]['date'])
        strpopularbirth = str(popular_year_birth)
        earliest_recent_year = ('The earliest hour, most recent date, most common year of birth: '+ earliest + ', ' + getdatevalue + ', ' + strpopularbirth)
        writefile('3) ' + earliest_recent_year)

"""=========================================================================="""
"""Function to display raw data from reading from a text file
   user can choose to dislay 5 lines at a time or all lines at 1 time   """
chkinput = ["y","n"]
def displayrawdata(displayNum):
    num_lines = sum(1 for line in open('all4questions.txt')) #get line total
    displayq = input("Do you want to display 5 lines at a time? Y for 'yes', N for 'no' ... ").lower()
    if displayq == 'n':     #if no, set to display all lines
        displayNum = num_lines
    while displayq not in chkinput:
        displayq = input("Please type Y for 'yes', N for 'no' ... ").lower()
    if displayq == 'n':     #if no, set to display all lines
        displayNum = num_lines
    with open("all4questions.txt", 'r') as infile:
        Num = displayNum
        for line in infile:
            new_lines = line.strip()
            if Num != 0:
                print(new_lines)
                Num -= 1
            # when count number of line is 0
            else:
                displayq = input("Do you want to display 5 lines at a time? Y for 'yes', N for 'no' ... ").lower()
                print(new_lines)
                while displayq not in chkinput:
                    displayq = input("Please type Y for 'yes', N for 'no' ... ").lower()
                if displayq == 'n':
                    Num = num_lines
                else:
                    Num = 5
    open('all4questions.txt', 'w').close()  #clear file
"""=========================================================================="""
""" This is the main program will call other functions to get data"""
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        displayrawdata(5)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
