import ast
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

def test_validity(original_sheet: pd.DataFrame, altered_series: pd.Series, column_name: str, error_handling:str = 'ignore') -> None:
    testing_nans = altered_series[altered_series.isnull()]
    errors = 0
    for row in testing_nans.index:
        if not pd.isna(original_sheet.loc[row, column_name]):
            errors += 1
            print(f"Error in conversion in row {row}, column name = {column_name}!")

    if errors != 0:
        if error_handling == 'ignore':
            print('Errors were found, see above for row index. Committing changes to dataframe.')
        elif error_handling == 'error':
            raise ValueError('Errors were found. Halting program.')

def flag(df: pd.DataFrame) -> pd.Series:
    conditions = {'no_response_time': (df.loc[:, 'host_response_time'].isna()).astype(int),
                  'low_reviews': (df.loc[:, 'number_of_reviews'] < 1).astype(int),
                  'low_availability': (df.loc[:, 'availability_30'] < 5).astype(int),
                  'price_per_person_high': (df.loc[:, 'price']/df.loc[:, 'accommodates'] > 500).astype(int),
                  'large_host': (df.loc[:, 'calculated_host_listings_count'] >= 10).astype(int),
                  'is_inactive': ((df.loc[:, 'number_of_reviews_ltm'] == 0) & (df.loc[:, 'estimated_occupancy_l365d'] == 0)).astype(int),
                  'high_price': (df.loc[:, 'price'] > 1000).astype(int)}

    # Hard pass rule
    extreme_price = df.loc[:, 'price'] > 20000
    extreme_price_per_person =  (df.loc[:, 'price']/df.loc[:, 'accommodates']) > 1500

    suspicion_score = sum(cond for cond in conditions.values())
    is_suspicious = (suspicion_score >= 3) | extreme_price | extreme_price_per_person
    return is_suspicious


def build_cities() -> dict:
    """
    Returns cleaned and clustered DataFrames
    """
    print("Loading data...")

    AustinData = pd.read_csv('data/Austin.csv')
    ChicagoData = pd.read_csv('data/Chicago.csv')
    LosAngelesData = pd.read_csv('data/LosAngeles.csv')
    NewYorkData = pd.read_csv('data/NewYorkCity.csv')
    PortlandData = pd.read_csv('data/Portland.csv')

    columns_to_use = ['host_id', 'host_response_time', 'host_is_superhost', 'neighbourhood_group_cleansed', 'latitude',
                      'longitude', 'room_type',
                      'accommodates', 'bathrooms', 'amenities', 'price', 'availability_30', 'number_of_reviews',
                      'number_of_reviews_ltm', 'availability_90',
                      'estimated_occupancy_l365d', 'review_scores_rating', 'calculated_host_listings_count']

    print("Data loaded. Moving onto cleaning....")

    cities = {'Austin': AustinData[columns_to_use].copy(),
              'Chicago': ChicagoData[columns_to_use].copy(),
              'Los Angeles': LosAngelesData[columns_to_use].copy(),
              'New York': NewYorkData[columns_to_use].copy(),
              'Portland': PortlandData[columns_to_use].copy()}

    response_map = {'within an hour': 0, 'within a few hours': 1, 'within a day': 2, 'a few days or more': 3}
    room_map = {'Entire home/apt': 0, 'Private room': 1, 'Shared room': 2, 'Hotel room': 3}

    for city, df in cities.items():
        superhost_series = (df.loc[:, 'host_is_superhost'] == 't').astype(int)
        test_validity(df, superhost_series, 'host_is_superhost')
        df['host_is_superhost'] = superhost_series

        response_series = df.loc[:, 'host_response_time'].map(response_map)
        test_validity(df, response_series, 'host_response_time')
        df['host_response_time'] = response_series

        room_series = df.loc[:, 'room_type'].map(room_map)
        test_validity(df, room_series, 'room_type')
        df['room_type'] = room_series

        amenity_series = df.loc[:, 'amenities'].apply(lambda x: ast.literal_eval(x)).str.len()
        test_validity(df, amenity_series, 'amenities')
        df['amenities'] = amenity_series

        price_series = pd.to_numeric(df.loc[:, 'price'].str.replace("$", "", regex=False).str.replace(",", "", regex=False),
                                     errors='coerce', downcast='float')
        test_validity(df, price_series, 'price')
        df['price'] = price_series

        flags = (df.loc[~flag(df)].dropna(subset=['price']))
        test_validity(df, flags.loc[:, 'price'], 'price')
        cities[city] = flags

    # eps and min_samples parameters for Austin, Chicago, Los Angeles, New York, and Portland
    param_pairs = [[0.35, 20], [0.28, 8], [0.25, 30],
                   [0.4, 15], [0.35, 12]]
    i = 0

    for city, df in cities.items():
        coords = StandardScaler().fit_transform(df.loc[:, ['latitude', 'longitude']])
        db = DBSCAN(eps=param_pairs[i][0], min_samples=param_pairs[i][1]).fit(coords)
        df['cluster'] = db.labels_
        i += 1

    print("Cleaning completed and clusters defined. Moving onto analysis...")

    return cities