import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')

    cities = ['chicago', 'new york city', 'washington']

    while True:
        city = input("Which city you would like to see data for? Please input Chicago, New York City, or Washington: ").lower()
        if city in cities:
            break
        print('\nThis is not a valid city. Please try again.\n')


    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    while True:
        month = input("\nWhich month (January - June) would you like to see data for? Input 'all' for no filter: ").lower()
        if month in months:
            break
        print('\nThis is not a valid month. Please try again.')


    day_of_week = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("\nWhich day of the week you would like to see data for? Input 'all' for no filter: ").lower()
        if day in day_of_week:
            break
        print('\nThis is not a valid day of the week. Please try again.\n')

    print('-'*40)
    return city, month, day

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

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most common month:', popular_month)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('\nMost common day of the week:', popular_day_of_week)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nMost common start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', popular_start_station)

    popular_end_station = df['End Station'].mode()[0]
    print('\nMost commonly used end station:', popular_end_station)

    df['station_to_station'] = df['Start Station'] + ' to ' + df['End Station']
    popular_station_combination = df['station_to_station'].mode()[0]
    print('\nMost frequent trip:', popular_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel = df['Trip Duration'].sum()
    print('Total travel time:', total_travel)

    mean_travel = df['Trip Duration'].mean()
    print('\nMean travel time:', mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print('User types count:\n', user_types.to_string())

    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('\nGender count:\n', gender.to_string())
    else:
        print('\nNo gender information for this city.')

    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        print('\nEarliest birth year:', earliest_birth_year)

        recent_birth_year = int(df['Birth Year'].max())
        print('\nMost recent birth year:', recent_birth_year)

        most_common = int(df['Birth Year'].mode()[0])
        print('\nMost common birth year:', most_common)

    else:
        print('\nNo birth year information for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Asks user if they would like to see 5 lines of raw data and displays them if requested, incrementing rows by 5 with each yes response"""

    pd.options.display.max_columns = None

    print('\nCalculating Raw Data...\n')
    start_time = time.time()

    raw_data_inputs = ['yes', 'no']
    data_lines = 0

    while True:
        raw_data_input = input('\nWould you like to see 5 lines of raw data?\n').lower()
        if raw_data_input in raw_data_inputs:
            break
        print('\nInvalid response. Please try again.')

    if raw_data_input == 'yes':
        print(df.head())
        while True:
            more_raw_data = input("\nDo you want to see another 5 lines of raw data?\n").lower()
            if more_raw_data == 'no':
                break
            if more_raw_data not in raw_data_inputs:
                print('\nInvalid response. Please try again.')
                continue
            data_lines += 5
            print(df.iloc[data_lines:(data_lines + 5)])

    if raw_data_input == 'no':
        return

    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
