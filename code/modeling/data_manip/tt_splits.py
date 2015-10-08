import pandas as pd
import datetime
import operator

def tt_split_all_less_n_days(df, days_back=60): 
	'''
	Input: Pandas Dataframe, Integer
	Output: Pandas DataFrame, Pandas DataFrame

	Split the pandas data frame into a train/test split where we train on all of the 
	data but the most recent days_back days. 
	'''

	df['date_fire'] = pd.to_datetime(df['date_fire'])
	today = df['date_fire'].max().date()
	today_less_days = today - pd.Timedelta(days=days_back)
    	train = df.query('date_fire < @today_less_days')
	test = df.query('date_fire >= @today_less_days')

	return train, test

def tt_split_early_late(df, year, months_forward, months_backward=None): 
	'''
	Input: Pandas DataFrame, Integer
	Output: Pandas DataFrame, Pandas DataFrame 

	Take the pandas dataframe, and put all those data points in year year and any prior years into the training data.
	Also put all those months that are within months_forward past that year into the training data. For example, 
	if year is 2013 and months_foward is 3, take all data from year 2012 and 2013 and put that into the training 
	data. In addition, put the first 3 months of 2014 into the training data. Use the rest as the test data set.
	''' 

	df.loc[:, 'date_fire'] = pd.to_datetime(df['date_fire'].copy())
	# If we want more than 12 months forward, then we want a whole nother year, so let's just adjust the 
	# year and months_forward variables to handle that. 
	if months_forward >= 12: 
		year += 1
		months_forward -= 12
	date_split = datetime.date(year + 1, 1, 1)
	date_split_forward = return_next_month_start(date_split, months_forward, foward = True)

	train = df.query('date_fire < @date_split_forward')
	test = df.query('date_fire >= @date_split_forward')

	return train, test

def return_month_start(time, n_months, forward=True): 
	'''
	Input: datetime.date
	Output: datetime.date

	For the given datetime.date, return a datetime.date object that is the date for the first day in the 
	nth month ahead. For example, if I feed in January and the number 3, then I want this to spit back a 
	datetime.date that is the first day of the month of April in the same year.
	'''

	# Go ahead and move the inputted time forward at least 27 days for the number of months 
	# that we want. We know that there are at least 27 days in each month, and that this step will 
	# put us only a handful of days away from the start of the month we want. We can then step through 
	# day by day until the month changes. 
    
    month_operator = operator.add
    if forward = False: 
        month_operator = operator.sub

	if n == 0: 
		return time

	time = month_operator(time, datetime.timedelta(days=(27 * n_months)))

	one_day = datetime.timedelta(days=1)
	date_to_return = month_operator(time, one_day) 

    if foward == True: 
        while date_to_return.month == time.month: 
            date_to_return += one_day
    else:
        while date_to_return.day != 1: 
            date_to_return -= one_day

	return date_to_return 
