# Imports
import itertools
import warnings
warnings.filterwarnings("ignore")
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import math

def curriculum_logs_data():
    import env
    import os
    # let's pull the dataset from the sql server
    url = f'mysql+pymysql://{env.user}:{env.password}@{env.host}/curriculum_logs'
    query = '''
    SELECT *
    FROM logs
    LEFT JOIN cohorts on cohorts.id = logs.cohort_id;
    '''

    if os.path.isfile('curriculum_logs.csv'):
        return pd.read_csv('curriculum_logs.csv', index_col = 0)    
    else:
        return pd.read_sql(query, url)


def wrangle_curriculum_logs_data(df):

    # concatenate and change date type columns to the respective type 
    df['date_time'] = df.date + ' ' + df.time
    df.date_time = pd.to_datetime(df.date_time, format = '%Y-%m-%d %H:%M:%S')
    df.date = pd.to_datetime(df.date)
    df.time = pd.to_datetime(df.time).dt.time
    df.start_date = pd.to_datetime(df.start_date)
    df.end_date = pd.to_datetime(df.end_date)
    df.created_at = pd.to_datetime(df.created_at)
    df.deleted_at = pd.to_datetime(df.deleted_at)
    
    # missing entirety of columns
    df.drop(['id', 'slack','deleted_at'], inplace = True, axis = 1)
    
    # let's clean up the dataset
    df.dropna(inplace = True)
    
    # set the index
    df = df.set_index(df.date)
    
    # let's rename some columns
    df.rename(columns = {'path':'endpoint', 'ip':'source_ip', 'name':'cohort_name'}, inplace = True)
    
    # let's remove the staff members since this exercise pertains to students
    df = df[df['cohort_name'] != 'Staff']
    
    # add program name and course to dataframe
    df['program_name'] = df.program_id.map({1.0: 'PHP Full Stack Web Development',
                                            2.0: 'Java Full Stack Web Development',
                                            3.0: 'Data Science',
                                            4.0: 'Front End Web Development'})
    
    df['course'] = df.program_id.map({1.0: 'Web Development',
                                       2.0: 'Web Development',
                                       3.0: 'Data Science',
                                       4.0: 'Web Development'})
    return df