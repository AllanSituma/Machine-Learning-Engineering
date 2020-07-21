
import pandas as pd,pickle, sys, itertools, string, sys, re, datetime, time, shutil, copy
from matplotlib import pyplot as plt
import seaborn as sn
import numpy as np
import re



def displayall(df):
    """
    Setting the maximum rows and columns to to 1000.
    This is to enable us view all the features in the data set
    
    """
    with pd.option_context("display.max_rows",1000):
        with pd.option_context("display.max_columns",1000):
            display(df)
            
            
def desc_dataframe(df):
    """
    Function to describe dataframe
    
    """
    return displayall(df.describe(include = 'all'))


def plothist(col):
    """
    Function to plot distributions of various columns
    
    """
    sn.distplot(col)
    
    
    
def plot_groups(col):
    """
    Function for group by plot
    
    """
    sn.countplot(col)
    
    
    
def format_date(df,col):
    """
    Function to format date to mm/dd/yy for easy aggregation
    
    """
    
    df[col] = pd.to_datetime(df[col]).apply(lambda x : x.strftime("%m/%d/%Y"))
    
    
def to_date(df,col):
    """
    Function to convert column to date
    
    """
    df[col] = pd.to_datetime(df[col])
    
    
def change_index(df,date_column):
    """
    Function to set date as index
    
    """
    df.index = df[date_column]
    
    
    
def drop_columns (df,column_list):
    """
    Function to drop columns.
    
    column_list = list of columns to be dropped
    
    """
    df.drop(column_list,axis=1)
    return df

def add_datepart(df,fldname):
    
    """
    add_datepart converts a column of df from a datetime64 to many columns containing
    the information from the date. This applies changes inplace
    
    """
    
    fld = df[fldname]
    fld_dtype = fld.dtype
    if isinstance(fld_dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
        fld_dtype = np.datetime64

    if not np.issubdtype(fld_dtype, np.datetime64):
        df[fldname] = fld = pd.to_datetime(fld, infer_datetime_format=True, errors=errors)
    targ_pre = re.sub('[Dd]ate$', '', fldname)
    attr = ['Year', 'Month', 'Week', 'Day', 'Dayofweek', 'Dayofyear',
            'Is_month_end', 'Is_month_start', 'Is_quarter_end', 'Is_quarter_start', 'Is_year_end', 'Is_year_start','Hour']

def filter_na (df,column):
    """
    Function to filter data frame based on missing values in a certain column
    
    """
    drop_col = column
    new_df = df[df[drop_col].notnull()]
    return new_df
    
def count_null (df):
    """
    Function to count null values in a data frame
    
    """
    return df.isna().sum()


def days_time_diff (df,dateone,datetwo,newcolumn):
    """
    Function to create a new column based on the difference in days of two date columns.
    First the columns are changed to datetime format
    
    """
    to_date(df,dateone)
    to_date(df,datetwo)
    
    df[newcolumn] = (df[dateone] - df[datetwo]).dt.days