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

    print('Hello! Let\'s explore some US bikeshare data!')
    print("Here you can find US bikeshare data!")

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # when user enter wrong letter he will be asked to type again
    city = input("please enter the city name that you want (chicago, new york city, washington):\n ").lower()
    while city not in CITY_DATA:
        city = input("Invalid city. Please try again:\n ")
        city = city.lower()
    # get user input for month (all, january, february, ... , june)
    month = input("please enter the month that you want (all, january, february, ... , june):\n ").lower()
    months=['all','january', 'february', 'march', 'april', 'may', 'june']
    while month not in months:
        month = input("Invalid month. Please try again:\n ")
        month = month.lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter the day that you want (Monday,Sunday, ...):\n").lower()
    days=['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'sunday']
    while day not in days:
        day = input("Invalid day. Please try again:\n")
        day = day.lower()
            
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
    df['day'] = df['Start Time'].dt.weekday_name

    if month != 'all':
         months = ['january', 'february', 'march', 'april', 'may', 'june']
         month = months.index(month) + 1
         df = df[df['month'] == month]
           
       
    if day != 'all':
         df= df[df['day'] == day.title()]
           
        
    return df


def time_stats(df):
    
     """Displays statistics on the most frequent times of travel."""

     print('\nCalculating The Most Frequent Times of Travel...\n')
     start_time = time.time()

     # display the most common month
     months=['january', 'february', 'march', 'april', 'may', 'june']
     common_month = df['month'].mode()[0]
     print("The most common month is:\n", months[common_month-1])

     # display the most common day of week
     common_day = df['day'].mode()[0]
     print("The most common day of week is:\n", common_day)

     # display the most common start hour
     df['hour'] = df['Start Time'].dt.hour
     common_shour = df['hour'].mode()[0]
     print("The most common hour is:\n", common_shour)


     print("\nThis took %s seconds." % (time.time() - start_time))
     print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is:\n{}".format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most commonly used start station is:\n{}".format(common_end_station))

    # display most frequent combination of start station and end station trip
    start_and_end = df.groupby(['Start Station', 'End Station'])
    frequent_combination = start_and_end.size().sort_values(ascending=False).head(1)
    print("most frequent combination of start station and end station trip is:\n{}".format(frequent_combination) )


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The Total Trip Duration is :\n", total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The Average of trip duration:\n", mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df['User Type'].value_counts()
    print("The count of user types:\n{}".format(count_user_type))

    # Display counts of gender
    if city != 'washington':
        count_of_gender = df['Gender'].value_counts()
        print("The count of gender:\n{}".format(count_of_gender))

        # Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].min()
        most = df['Birth Year'].max()
        common_year_of_birth = df['Birth Year'].mode()[0]
        print("The earlist year of birth is {}\nThe most recent year of birth is {}\nThe most common year of birth is {}        \n".format(earliest,most,common_year_of_birth))
    else:
        print("SORRY!, Gender and Birth data are not available in washington.")
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        
        
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        start_loc = 0
        while True:
            if view_data.lower() == 'yes':
                print(df.iloc[start_loc : start_loc + 5])
                start_loc += 5
                view_data = input("Do you wish to continue?: ").lower()   
            else:
                break
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
