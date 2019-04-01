"""
Change 1
#1 Popular times of travel (i.e., occurs most often in the start time)
    most common month
    most common day of week
    most common hour of day

#2 Popular stations and trip
    most common start station
    most common end station
    most common trip from start to end (i.e., most frequent combination of start station and end station)

#3 Trip duration
    total travel time
    average travel time

#4 User info
    counts of each user type
    counts of each gender (only available for NYC and Chicago)
    earliest, most recent, most common year of birth (only available for NYC and Chicago)
small change"""


from datetime import datetime
from datetime import timedelta
import time
import pandas as pd
## Filenames

#chicago = 'chicago.csv'

#new_york_city = 'new_york_city.csv'

#washington = 'washington.csv'


def user_inputs():
        '''
        Asks user for input and based on input opens csv filename.
        If the input is wrong it prompts the user to re enter one of the cities as Chicago,
        New York or washington
        '''

        city = ''
        while city.lower() not in ['chicago', 'new york', 'washington']:
            city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                     'Would you like to see data for Chicago, New York, or'
                     ' Washington?\n')
            if city.lower() == 'chicago':
                return 'chicago.csv'
            elif city.lower() == 'new york':
                return 'new_york_city.csv'
            elif city.lower() == 'washington':
                return 'washington.csv'
            else:
                print('Sorry, I do not understand your input. Please input either '
                    'Chicago, New York, or Washington.')

def filter_input():
    '''Asks the user for a time period (day, month, week) and applies the
    specified filter to the data.
    '''

    filter_input = ''
    while filter_input.lower() not in ['month', 'day', 'none']:
        filter_input = input('\nFilter the data by month, day,'
                            ' or none at all? If none, then type "none" for no time filter.\n')
        if filter_input.lower() not in ['month', 'day', 'none']:
            print('Sorry, wrong input, try again.')
    return filter_input

def month_input():
    '''Asks the user for which month to show data then returns specified month.'''

    month_input = ''
    months_dict = {'january': 1, 'february': 2, 'march': 3, 'april': 4,
                   'may': 5, 'june': 6}
    while month_input.lower() not in months_dict.keys():
        month_input = input('\nWhich month? January, February, March, April,'
                            ' May, or June?\n')
        if month_input.lower() not in months_dict.keys():
            print('Sorry, incorrect month was entered. Please try again by typing'
                  'month between January and June')
    month = months_dict[month_input.lower()]
    return ('2017-{}'.format(month), '2017-{}'.format(month + 1))

def day_input():
    '''Asks the user for which day to show data then returns that specified day.'''

    this_month = month_input()[0]
    month = int(this_month[5:])
    valid_date = False
    while valid_date == False:
        is_int = False
        day = input('\nWhich day do you want to select? --> Enter number integer.\n')
        while is_int == False:
            try:
                day = int(day)
                is_int = True
            except ValueError:
                print('Wrong entry. Please type in an integer.')
                day = input('\nWhich day do you want to select? --> Enter number integer.\n')
        try:
            start_date = datetime(2017, month, day)
            valid_date = True
        except ValueError as e:
            print(str(e).capitalize())
    end_date = start_date + timedelta(days=1)
    return (str(start_date), str(end_date))

def popular_month(df):
    '''Calculates and prints most popular month'''

    months = ['January', 'February', 'March', 'April', 'May', 'June']
    index = int(df['start_time'].dt.month.mode())
    popular_month = months[index - 1]
    print('The most popular month: {}.'.format(popular_month))

def popular_day(df):
    '''Calculates the most popular day of week (Monday, Tuesday, etc.) for start time.'''

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                    'Saturday', 'Sunday']
    index = int(df['start_time'].dt.dayofweek.mode())
    popular_day = days_of_week[index]
    print('The most popular day of week for start time: {}.'.format(popular_day))

def popular_hour(df):
    '''Calcualted the most popular hour in start times!!!'''

    popular_hour = int(df['start_time'].dt.hour.mode())
    if popular_hour == 0:
        am_pm = 'am'
        popular_hour_dummy = 12
    elif 1 <= popular_hour < 13:
        am_pm = 'am'
        popular_hour_dummy = most_pop_hour
    elif 13 <= popular_hour < 24:
        am_pm = 'pm'
        popular_hour_dummy = popular_hour - 12
    print('The most popular hour in start time: {}{}.'.format(popular_hour_dummy, am_pm))

def tot_duration(df):
    '''Calculates and prints average and total time of trips. Trip duration field
    is in seconds. trip_duration function translates it into hour and minutes'''

    tot_duration = df['trip_duration'].sum()
    minute, second = divmod(tot_duration, 60)
    hour, minute = divmod(minute, 60)
    print('The total trip duration: {} hours, {} minutes and {}'
          ' seconds.'.format(hour, minute, second))
    avg_duration = round(df['trip_duration'].mean())
    m, s = divmod(avg_duration, 60)
    if m > 60:
        h, m = divmod(m, 60)
        print('Average duration: {} hours, {} minutes and {} seconds.'.format(h, m, s))
    else:
        print('Average trip duration: {} minutes and {} seconds.'.format(m, s))

def popular_stations(df):
    '''Calculates and prints most popular start and end stations'''

    pop_start = df['start_station'].mode().to_string(index = False)
    pop_end = df['end_station'].mode().to_string(index = False)
    print('Popular start station: {}.'.format(pop_start))
    print('Popular end station: {}.'.format(pop_end))

def popular_trip(df):
    '''Calcultes and prints most popular trip'''

    popular_trip = df['journey'].mode().to_string(index = False)
    # The 'journey' column is created in the statistics() function.
    print('The most popular trip is {}.'.format(popular_trip))

def users(df):
    '''Calcultes and prints type of users: either Subscriber or Customers'''

    subs = df.query('user_type == "Subscriber"').user_type.count()
    cust = df.query('user_type == "Customer"').user_type.count()
    print('Distribution of user types: {} Subscribers and {} Customers.'.format(subs, cust))

def gender(df):
    '''Distribution of user's gender: Male or Female
    '''

    male_count = df.query('gender == "Male"').gender.count()
    female_count = df.query('gender == "Male"').gender.count()
    print('Total number of male user: {}. Total number of female users: {} female users.'.format(male_count, female_count))

def birthdate_stats(df):

    youngest = int(df['birth_year'].min())
    oldest = int(df['birth_year'].max())
    mode = int(df['birth_year'].mode())
    print('The oldest users are born in {}.\nThe youngest users are born in {}.'
          '\nThe most popular birth year is {}.'.format(youngest, oldest, mode))

def display_data(df):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.
    '''
    def is_valid(display):
        if display.lower() in ['yes', 'no']:
            return True
        else:
            return False
    head = 0
    tail = 5
    valid_input = False
    while valid_input == False:
        display = input('\nWould you like to view individual trip data? '
                        'Type \'yes\' or \'no\'.\n')
        valid_input = is_valid(display)
        if valid_input == True:
            break
        else:
            print("Sorry, I do not understand your input. Please type 'yes' or"
                  " 'no'.")
    if display.lower() == 'yes':
        # prints every column except the 'journey' column created in statistics()
        print(df[df.columns[0:-1]].iloc[head:tail])
        display_more = ''
        while display_more.lower() != 'no':
            valid_input_2 = False
            while valid_input_2 == False:
                display_more = input('\nWould you like to view more individual'
                                     ' trip data? Type \'yes\' or \'no\'.\n')
                valid_input_2 = is_valid(display_more)
                if valid_input_2 == True:
                    break
                else:
                    print("Sorry, I do not understand your input. Please type "
                          "'yes' or 'no'.")
            if display_more.lower() == 'yes':
                head += 5
                tail += 5
                print(df[df.columns[0:-1]].iloc[head:tail])
            elif display_more.lower() == 'no':
                break


def main():
    '''Prints user statistics from functions previously defined'''

    # Filter by city (Chicago, New York, Washington)
    city = user_inputs()
    print('Loading data...')
    df = pd.read_csv(city, parse_dates = ['Start Time', 'End Time'])

    # change all column names to lowercase letters and replace spaces with underscores
    new_labels = []
    for col in df.columns:
        new_labels.append(col.replace(' ', '_').lower())
    df.columns = new_labels

    # increases the column width so that the long strings in the 'journey'
    # column can be displayed fully
    pd.set_option('max_colwidth', 100)

    # creates a 'journey' column that concatenates 'start_station' with
    # 'end_station' for the use popular_trip() function
    df['journey'] = df['start_station'].str.cat(df['end_station'], sep=' to ')

    # Filter by time period (month, day, none)
    filter_period = filter_input()
    if filter_period == 'none':
        df_filtered = df
    elif filter_period == 'month' or filter_period == 'day':
        if filter_period == 'month':
            filter_lower, filter_upper = month_input()
        elif filter_period == 'day':
            filter_lower, filter_upper = day_input()
        print('Filtering data...')
        df_filtered = df[(df['start_time'] >= filter_lower) & (df['start_time'] < filter_upper)]
    print('\nCalculating the first statistic...')

    if filter_period == 'none':
        start_time = time.time()

        # What is the most popular month for start time?
        popular_month(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")

    if filter_period == 'none' or filter_period == 'month':
        start_time = time.time()

        # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
        popular_day(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
        start_time = time.time()

        # What is the most popular hour of day for start time?
        popular_hour(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
        start_time = time.time()

        # What is the total trip duration and average trip duration?
        tot_duration(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
        start_time = time.time()

        # What is the most popular start station and most popular end station?
        popular_stations(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
        start_time = time.time()

        # What is the most popular trip?
        popular_trip(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
        start_time = time.time()

        # What are the counts of each user type?
        users(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))

    if city == 'chicago.csv' or city == 'new_york_city.csv':
        print("\nCalculating the next statistic...")
        start_time = time.time()

        # What are the counts of gender?
        gender(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
        start_time = time.time()

        # What are the earliest (i.e. oldest user), most recent (i.e. youngest
        # user), and most popular birth years?
        birthdate_stats(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))

    # Display five lines of data at a time if user specifies that they would like to
    display_data(df_filtered)

    # Restart?
    restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
    while restart.lower() not in ['yes', 'no']:
        print("Invalid input. Please type 'yes' or 'no'.")
        restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
    if restart.lower() == 'yes':
        main()

if __name__ == "__main__":
	main()
