import pandas as pd
import matplotlib.pyplot as plt


def read_csv_file():
    """
    Read a CSV file containing Bradford weather data.
    
    Returns:
        pd.DataFrame: DataFrame containing the weather data.
    """
    data = pd.read_csv('E:/jupyter notebook/bradforddata.csv')
    return data


def manipulating_data(df):
    """
    Modify DataFrame columns and clean data.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Modified DataFrame.
    """

    # selecting data for the last 10 years
    df = df[df['yyyy'] >= 2013]

    # renaming columns for clarity
    df.rename(columns={'yyyy': 'year', 'mm': 'month',
                       'tmax_degC': 't_max', 'tmin_degC': 't_min',
                       'af days': 'air_frost', 'rain mm': 'rainfall',
                       'sun hours': 'sunshine_duration'}, inplace=True)

    # converting year and month to year_month format
    df['year_month'] = pd.to_datetime(df['year'].astype(
        str) + '-' + df['month'].astype(str), format='%Y-%m')

    columns_to_clean = ['sunshine_duration',
                        'air_frost', 't_max', 't_min', 'rainfall']

    # removing '*' and '---' from specified columns
    for col in columns_to_clean:
        df[col] = df[col].str.replace('*', '')
    df = df.replace('---', '')

    # converting 'air_frost' to numeric, replace NaN with 0, and convert to int
    df['air_frost'] = pd.to_numeric(
        df['air_frost'], errors='coerce').fillna(0).astype(int)

    # converting specified columns to numeric format
    df[['t_max', 't_min', 'rainfall', 'sunshine_duration']] = df[['t_max', 't_min',
                                                                  'rainfall', 'sunshine_duration']].apply(pd.to_numeric, errors='coerce')
    return df


def linegraph(data):
    """
    Generate a line graph to visualize temperature trends.
    
    Args:
        data (pd.DataFrame): DataFrame containing 'date', 't_max', and 't_min' columns.
    
    Returns:
        None
    """
    # Extract necessary columns
    dates = data['year_month']
    tmax = data['t_max']
    tmin = data['t_min']

    # Creating line graph
    plt.figure(figsize=(10, 5))
    plt.plot(dates, tmax, label='Max Temperature (°C)', color='red')
    plt.plot(dates, tmin, label='Min Temperature (°C)', color='blue')

    # labels and title
    plt.xlabel('Year-Month')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Trends in Bradford (Data for Last 10 Years)')

    # legend at the lower center
    plt.legend(loc='lower left')

    # Show the plot
    plt.show()


def bargraph(data):
    """
    Generate a bar chart to visualize total air frost days per year.

    Args:
        data (pd.DataFrame): DataFrame containing 'year' and 'air_frost' columns.

    Returns:
        None
    """
    # Grouping data by year to get the total number of air frost days
    total_af_per_year = data.groupby(
        'year')['air_frost'].sum().reset_index()

    # Creating a bar chart for total air frost days per year
    plt.figure(figsize=(10, 6))
    plt.bar(total_af_per_year['year'],
            total_af_per_year['air_frost'], color='blue')

    # labels and title
    plt.xlabel('Year')
    plt.ylabel('Total Air Frost Days')
    plt.title('Total Air Frost Days per Year')

    # Show the plot
    plt.show()


def hist2d_plot(data):
    """
    Generate a 2D histogram plot to visualize the distribution of sunshine hours by year and month.

    Args:
        data (pd.DataFrame): DataFrame containing 'year', 'month', and 'sunshine_duration' columns.

    Returns:
        None
    """
    # Extracting year, month, and sunshine hours data
    years = data['year']
    months = data['month']
    sunshine_hours = data['sunshine_duration']

    # ranges for the bins
    year_range = range(min(years), max(years)+1)
    month_range = range(1, 13)

    # 2D histogram for the distribution of sunshine hours by year and month
    plt.figure(figsize=(10, 8))
    plt.hist2d(years, months, weights=sunshine_hours,
               bins=(year_range, month_range), cmap='YlOrBr')

    # labels and title
    plt.xlabel('Year')
    plt.ylabel('Month')
    plt.title('Distribution of Sunshine Hours by Year and Month')
    plt.colorbar(label='Sunshine Hours')

    # show the plot
    plt.show()


if __name__ == '__main__':
    print('Started!!!')
    data = read_csv_file()
    data = manipulating_data(df=data)
    linegraph(data)
    bargraph(data)
    hist2d_plot(data)
    print('Ended!!!')
