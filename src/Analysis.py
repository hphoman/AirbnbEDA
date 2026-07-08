from dataclasses import dataclass
import pandas as pd
import statsmodels.formula.api as smf

def to_percents(df: pd.Series, column_names:list | None = None, index_names:list | None = None) -> pd.DataFrame:
    df = df.unstack(fill_value=0)
    df = df.div(df.sum(axis=1), axis=0) * 100

    if column_names is not None:
        if len(column_names) == len(df.columns):
            df = df.rename(columns=dict(zip(df.columns.to_list(), column_names)))
        else:
            raise ValueError("Length of column names does not match the length of columns.")
    if index_names is not None:
        if len(index_names) == len(df.index):
            df = df.rename(index=dict(zip(df.index.to_list(), index_names)))
        else:
            raise ValueError("Length of index names does not match the length of index.")

    df.columns.name = None
    df.index.name = None

    return df

@dataclass
class DashboardData:
    names: list
    metrics: dict
    param_pairs: dict
    lat_long_cluster: dict
    cluster_price: dict
    median_cv_cities:dict
    population_median: pd.DataFrame
    borough_price: dict
    host_population: dict
    listing_percentages: dict
    host_price: pd.DataFrame
    borough_hosts: pd.DataFrame
    manhattan_host_price: pd.Series
    cluster_room: dict
    borough_rooms: pd.DataFrame
    room_host: dict
    price_models: dict
    price_model_sums: dict
    city_availability: dict
    borough_availability: dict
    host_availability: pd.DataFrame
    room_availability: pd.DataFrame

def build_dashboard_data(cities: dict) -> DashboardData:
    name_list = list(cities.keys())

    # New York County (Manhattan), Kings County (Brooklyn), Queens County, Bronx County, and Richmond County (Staten Island)
    borough_estimates = [1664862, 2653963, 2358182, 1406332, 501290]

    # Travis County (Austin), Cook County (Chicago), Los Angeles County, sum of five boroughs, and Multnomah County (Portland)
    population_estimate = [1389670, 5194625, 9694934, sum(borough_estimates), 795391]

    host_labels = {0: "Individual",
                   1: "Small Host",
                   2: "Large Host"}

    room_labels = {0: "Entire",
                   1: "Private",
                   2: "Shared",
                   3: "Hotel"}

    metrics = []
    lat_long_clusters = []
    cluster_prices = []
    unique_hosts = []
    host_type_counts = []
    host_price = []
    host_percentages = []
    listing_percentages = []
    price_models = []
    price_model_stats = []
    room_per_cluster = []
    medians = []
    cvs = []
    availability_data = []
    host_availability_data = {'Individual': [], 'Small Host': [], 'Large Host': []}
    room_availability_data = {'Entire': [], 'Private': [], 'Shared': [], 'Hotel': []}
    room_per_host = []

    # Taken from DBSCAN
    param_pairs = [[0.35, 20], [0.28, 8], [0.25, 30],
                   [0.4, 15], [0.35, 12]]

    for city, df in cities.items():
        lat_long_clusters.append(pd.DataFrame(data = {'Latitude': df['latitude'],
                                                      'Longitude': df['longitude'],
                                                      'Cluster': df['cluster']}))

        cluster_prices.append(df.groupby('cluster', observed=True)['price'].describe())

        unique_host = df.loc[:, 'host_id'].drop_duplicates().count()
        unique_hosts.append(unique_host)

        # 0 -> individual, 1 -> small multi-host, 2 -> large multi-host
        df['host_type'] = pd.cut(
            df.loc[:, 'host_id'].map(df.loc[:, 'host_id'].value_counts()),
            bins = [0, 1, 9, float('inf')],
            labels=[0, 1, 2],
            include_lowest=True)

        host_count = (df.loc[:, ['host_id', 'host_type']].drop_duplicates()
                      .groupby('host_type', observed=True).count()
                      .rename(columns={'host_id': 'count'}))
        host_count = host_count.reindex([0, 1, 2], fill_value=0)

        host_type_counts.append(host_count)

        median_host_price = df.groupby('host_type', observed=True)['price'].median()
        host_price.append([median_host_price[i] for i in range(len(median_host_price))])

        host_percentage = pd.Series(
            data={label: [host_count.loc[i, 'count'] / unique_host * 100]
                  for i, label in host_labels.items()}
        )

        host_percentages.append(host_percentage)

        listing_counts = df['host_type'].value_counts()
        listing_percentages.append(listing_counts.div(listing_counts.sum()) * 100)

        room_types = df.groupby('cluster')['room_type'].value_counts().unstack(fill_value=0)
        room_types = room_types.div(room_types.sum(axis=1), axis=0) * 100
        room_per_cluster.append(room_types.rename(columns=room_labels))

        host_room = df.groupby('room_type', observed=True)['host_type'].value_counts().unstack(fill_value=0)
        host_room = host_room.div(host_room.sum(axis=1), axis=0) * 100

        room_per_host.append(host_room.rename(columns=host_labels, index=room_labels))

        regression_condition = (df.loc[:, 'room_type'] == 0)
        price_regression_columns = ['price', 'accommodates', 'host_is_superhost', 'bathrooms', 'review_scores_rating']

        price_regression = df.loc[regression_condition, price_regression_columns].dropna()

        price_model = smf.ols(
            """
            price ~ accommodates
                    + host_is_superhost
                    + bathrooms
                    + review_scores_rating
            """, data = price_regression).fit()

        price_models.append(price_model)
        price_model_stats.append(price_model.summary())

        describe_data = df.loc[:, 'price'].describe()
        median_price = df.loc[:, 'price'].median()
        medians.append(median_price)
        cv = describe_data['std'] / describe_data['mean']
        cvs.append(cv)

        availability_data.append(df.loc[:, 'availability_90'].dropna())
        host_availability = df.groupby('host_type', observed=True)['availability_90'].describe()
        for i, label in zip(range(len(host_availability)), list(host_labels.values())):
            host_availability_data[label].append(host_availability.loc[i, :]['50%'])

        room_availability = df.groupby('room_type', observed=True)['availability_90'].describe()
        for i, label in zip(range(len(room_availability)), list(room_labels.values())):
            room_availability_data[label].append(room_availability.loc[i, :]['50%'])

        metrics.append(pd.Series(
                        data = {'Listings': df.shape[0],
                                'Median Price': median_price,
                                'Unique Hosts': unique_host,
                                'Median Availability': df.loc[:, 'availability_90'].median()},
                        index = ['Listings', 'Median Price',
                                'Unique Hosts', 'Median Availability']))

        if city == 'New York':
            borough_count = df.loc[:, 'neighbourhood_group_cleansed'].value_counts()
            borough_value = df.groupby('neighbourhood_group_cleansed', observed = True)['price'].describe()
            borough_hosts = df.groupby('neighbourhood_group_cleansed', observed = True)['host_type'].value_counts()
            borough_rooms = df.groupby('neighbourhood_group_cleansed', observed = True)['room_type'].value_counts()

            borough_availability_data = df.groupby('neighbourhood_group_cleansed', observed=True)['availability_90']

    host_availability_data = pd.DataFrame(index=name_list, data=host_availability_data)
    room_availability_data = pd.DataFrame(index=name_list, data=room_availability_data)

    print("Calculations completed. Loading data...")

    median_cv = {'median': medians, 'cv': cvs}

    price_per_pop = pd.DataFrame(index=name_list,
                                 data={'population': population_estimate,
                                       'price':medians})

    borough_price = {'count': borough_count, 'price': borough_value}

    price_per_host = pd.DataFrame(index=name_list,
                                  columns=['Individual', 'Small Host', 'Large Host'],
                                  data=host_price)

    manhattan_prices = cities['New York'][['neighbourhood_group_cleansed', 'price', 'host_type']]
    manhattan_prices = manhattan_prices.drop(
        index = manhattan_prices[manhattan_prices['neighbourhood_group_cleansed'] != 'Manhattan'].index
    ).dropna()
    manhattan_prices = manhattan_prices.groupby('host_type', observed = True)['price'].median()
    manhattan_prices = manhattan_prices.rename(index={0: "Individual", 1: "Small Host", 2: "Large Host"})
    manhattan_prices.index.name = None

    room_per_borough = borough_rooms.unstack(fill_value=0)
    room_per_borough = room_per_borough.div(room_per_borough.sum(axis=1), axis=0) * 100
    room_per_borough = room_per_borough.rename(columns={0: "Entire", 1:"Private", 2:"Shared", 3:"Hotel"})
    room_per_borough.columns.name = None
    room_per_borough.index.name = None

    borough_availability = dict(zip(
        list(borough_availability_data.groups.keys()),
        [group.values for _, group in borough_availability_data]))

    print("Data loaded. Preparing plots...")

    return DashboardData(
        names=name_list,
        metrics=dict(zip(name_list, metrics)),
        param_pairs=dict(zip(name_list, param_pairs)),
        lat_long_cluster=dict(zip(name_list, lat_long_clusters)),
        cluster_price=dict(zip(name_list, cluster_prices)),
        median_cv_cities=median_cv,
        population_median=price_per_pop,
        borough_price=borough_price,
        host_population=dict(zip(name_list, host_percentages)),
        listing_percentages=dict(zip(name_list, listing_percentages)),
        host_price=price_per_host,
        borough_hosts=to_percents(borough_hosts, column_names=['Individual', 'Small Host', 'Large Host']),
        manhattan_host_price=manhattan_prices,
        cluster_room=dict(zip(name_list, room_per_cluster)),
        borough_rooms=to_percents(borough_rooms, column_names=['Entire', 'Private', 'Shared', 'Hotel']),
        room_host=dict(zip(name_list, room_per_host)),
        price_models=dict(zip(name_list, price_models)),
        price_model_sums=dict(zip(name_list, price_model_stats)),
        city_availability= dict(zip(name_list, availability_data)),
        borough_availability=borough_availability,
        host_availability=host_availability_data,
        room_availability=room_availability_data
    )