import matplotlib.pyplot as plt

plt.style.use("dark_background")

class Plotter:
    def __init__(self, data):
        self.data = data

    def clusters(self, city:str = 'Entire', figsize=(5, 5)) -> plt.Figure:
        lat_long_clusters = self.data.lat_long_cluster
        name_list = self.data.names

        if (city not in name_list) and (city != 'Entire'):
            raise ValueError(f"City {city} not available")

        if city == 'Entire':
            fig, axs = plt.subplots(3, 2, figsize=figsize)
            for i, ax in enumerate(axs.flat):
                if i < len(lat_long_clusters):
                    df = lat_long_clusters[name_list[i]]
                    clusters = sorted(df['Cluster'].unique(), key=lambda x: (x == -1, x))
                    for cluster in clusters:
                        subset = df[df['Cluster'] == cluster]
                        label = f'Cluster {cluster}' if cluster != -1 else 'Independent'
                        ax.scatter(subset['Longitude'], subset['Latitude'],label=label, s=10)
                    ax.set_xlabel('Longitude')
                    ax.set_ylabel('Latitude')
                    ax.set_title(name_list[i])
                    ax.legend()
                else:
                    ax.set_visible(False)
            plt.tight_layout()

        else:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
            df = lat_long_clusters[city]
            clusters = sorted(df['Cluster'].unique(), key=lambda x: (x == -1, x))
            for cluster in clusters:
                subset = df[df['Cluster'] == cluster]
                label = f'Cluster {cluster}' if cluster != -1 else 'Independent'
                ax.scatter(subset['Longitude'], subset['Latitude'], label=label, s=10)
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            ax.set_title(city)
            ax.legend()

        return fig

    def price_per_cluster(self, city:str = 'Entire', figsize=(5,5)) -> plt.Figure:
        cluster_price = self.data.cluster_price
        name_list = self.data.names

        if (city not in name_list) and (city != 'Entire'):
            raise ValueError(f"City {city} not available")

        if city == 'Entire':
            fig, axs = plt.subplots(3, 2, figsize=figsize)
            for i, ax in enumerate(axs.flat):
                if i < len(cluster_price):
                    df = cluster_price[name_list[i]]
                    updated_ordering = [i for i in df.index if i != -1]
                    if -1 in df.index:
                        updated_ordering.append(-1)
                    df = df.loc[updated_ordering]
                    labels = ["Independent" if j == -1 else f"Cluster {j}" for j in df.index]

                    ax.bar(labels, df["50%"])
                    ax.set_xticks(range(len(labels)))
                    ax.set_xticklabels(labels)
                    ax.set_ylabel('Price ($)')
                    ax.set_title(name_list[i])
                else:
                    ax.set_visible(False)
            plt.tight_layout()

        else:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
            df = cluster_price[city]
            updated_ordering = [i for i in df.index if i != -1]
            if -1 in df.index:
                updated_ordering.append(-1)
            df = df.loc[updated_ordering]
            labels = ["Independent" if j == -1 else f"Cluster {j}" for j in df.index]

            ax.bar(labels, df["50%"])
            ax.set_xticks(range(len(labels)))
            ax.set_xticklabels(labels)
            ax.set_ylabel('Price ($)')
            ax.set_title(city)

        return fig

    def median_cv(self, figsize=(5,5)) -> plt.Figure:
        median_cv = self.data.median_cv_cities
        name_list = self.data.names

        fig, ax = plt.subplots(2, 1, figsize=figsize)

        ax[0].bar(name_list, median_cv['median'])
        ax[0].set_ylabel('Median Nightly Price ($)')
        ax[0].set_title('Median AirBnb Price per City')

        ax[1].bar(name_list, median_cv['cv'])
        ax[1].set_ylabel('CV')
        ax[1].set_title('CV for AirBnb Price per City')

        plt.tight_layout()
        return fig

    def price_population(self, figsize=(5,5)) -> plt.Figure:
        population_price = self.data.population_median
        name_list = self.data.names

        offsets = {'Austin': (-15, 10), 'Chicago': (-20, 10), 'Los Angeles': (-68, 0),
                   'New York': (-55, 0), 'Portland': (10, 5)}

        fig, ax = plt.subplots(1, 1, figsize=figsize)
        ax.scatter(population_price['population'], population_price['price'],
                   s=70, edgecolor='white', linewidth=0.5, zorder=3)

        for x, y, name in zip(population_price['population'], population_price['price'], name_list):
            dx, dy = offsets[name]
            ax.annotate(name, (x, y), xytext=(dx, dy), textcoords='offset points')

        ax.set_xlabel('Population Estimate (log scale)')
        ax.set_ylabel('Median Nightly Price ($)')
        ax.set_title('Median AirBnb Price per City')

        return fig

    def borough_price_listing(self, figsize=(5,5)) -> plt.Figure:
        borough_price = self.data.borough_price

        fig, axs = plt.subplots(1, 2, figsize=figsize)

        axs[0].pie(borough_price['count'].to_list(),
                   labels = borough_price['count'].index.tolist(),
                   autopct='%1.2f%%',
                   textprops={'ha': 'center', 'va': 'center'},
                   wedgeprops={'width': 0.2})

        axs[0].set_title("Listings per Borough")

        axs[1].bar(borough_price['price'].index.tolist(), borough_price['price']["50%"])
        axs[1].set_ylabel("Price ($)")
        axs[1].set_title("Price per Borough")
        plt.tight_layout()
        return fig

    def host_population_listing_percentages(self, city:str = 'Entire', figsize=(5,5)) -> plt.Figure:
        host_population = self.data.host_population
        listing_percentages = self.data.listing_percentages
        name_list = self.data.names

        if (city not in name_list) and (city != 'Entire'):
            raise ValueError(f"City {city} not available")

        host_labels = ["Individual", "Small Host", "Large Host"]
        listing_order = [0, 1, 2]

        if city == 'Entire':
            fig = plt.figure(figsize=figsize, layout="constrained")
            outer = fig.add_gridspec(2, 3)

            for i, name in enumerate(name_list):
                row, col = divmod(i, 3)

                inner = outer[row, col].subgridspec(2, 1)

                ax_host = fig.add_subplot(inner[0, 0])
                ax_listing = fig.add_subplot(inner[1, 0])

                host_values = (host_population[name]
                    .reindex(host_labels)
                    .map(lambda x: x[0] if isinstance(x, list) else x)
                    .to_numpy())

                listing_values = (listing_percentages[name]
                    .reindex(listing_order)
                    .to_numpy())

                ax_host.pie(host_values,
                    labels=host_labels,
                    autopct="%1.2f%%",
                    wedgeprops={"width": 0.2})

                ax_listing.pie(listing_values,
                    labels=host_labels,
                    autopct="%1.2f%%",
                    wedgeprops={"width": 0.2})

                ax_host.set_title(name, fontsize=12, pad=8)

                ax_host.set_ylabel("Hosts", rotation=0, labelpad=25)
                ax_listing.set_ylabel("Listings", rotation=0, labelpad=25)

        else:
            fig, axs = plt.subplots(1, 2, figsize = figsize) #(11,6)

            host_values = (host_population[city]
                           .reindex(host_labels)
                           .map(lambda x: x[0] if isinstance(x, list) else x)
                           .to_numpy())

            listing_values = (listing_percentages[city]
                              .reindex(listing_order)
                              .to_numpy())

            axs[0].pie(host_values,
                        labels=host_labels,
                        autopct="%1.2f%%",
                        wedgeprops={"width": 0.2})
            axs[0].set_title(f"Host Population for {city}")

            axs[1].pie(listing_values,
                           labels=host_labels,
                           autopct="%1.2f%%",
                           wedgeprops={"width": 0.2})
            axs[1].set_title(f"Host Listings for {city}")

        return fig

    def host_price(self, city:str='Entire', figsize=(5,5)) -> plt.Figure:
        price_per_host = self.data.host_price
        name_list = self.data.names

        if (city not in name_list) and (city != 'Entire'):
            raise ValueError(f"City {city} not available")

        if city == 'Entire':
            fig, axs = plt.subplots(2, 3, figsize=figsize) # (12, 10) Suggested

            for i, ax in enumerate(axs.flat):
                if i < len(price_per_host.index):
                    ax.bar(price_per_host.columns.to_list(), price_per_host.loc[name_list[i], :])
                    ax.set_ylabel("Median Nightly Price ($)")
                    ax.set_title(name_list[i])
                else:
                    ax.set_visible(False)

            plt.tight_layout()

        else:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
            ax.bar(price_per_host.columns.to_list(), price_per_host.loc[city, :])
            ax.set_ylabel("Median Nightly Price ($)")
            ax.set_title(city)
        return fig

    def borough_hosts(self, figsize=(5,5)) -> plt.Figure:
        borough_hosts = self.data.borough_hosts
        fig, ax = plt.subplots(1, 1, figsize=figsize) # (5, 10) suggested

        im = ax.imshow(borough_hosts, cmap='BrBG', aspect='auto')
        ax.set_xticks(range(len(borough_hosts.columns)))
        ax.set_xticklabels(borough_hosts.columns.to_list())
        ax.set_yticks(range(len(borough_hosts.index)))
        ax.set_yticklabels(borough_hosts.index.tolist())
        ax.set_title("Host Percentages per Borough")

        for i in range(borough_hosts.shape[0]):
            for j in range(borough_hosts.shape[1]):
                ax.text(j, i, f"{borough_hosts.iloc[i, j]:.1f}%",
                        ha="center", va="center", color='black')

        return fig

    def manhattan_price(self, figsize=(5,5)) -> plt.Figure:
        manhattan_price = self.data.manhattan_host_price
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        ax.bar(manhattan_price.index.to_list(), manhattan_price)
        ax.set_ylabel("Price ($)")
        ax.set_title("Manhattan Price Distribution Across Host Types")
        return fig

    def cluster_room(self, city:str='Entire', figsize=(5,5)) -> plt.Figure:
        cluster_room = self.data.cluster_room
        name_list = self.data.names

        if (city not in name_list) and (city != 'Entire'):
            raise ValueError(f"City {city} not available")

        if city == 'Entire':
            fig, axs = plt.subplots(2, 3, figsize=figsize) # (15, 10) suggested

            for i, ax in enumerate(axs.flat):
                if i < len(cluster_room.keys()):
                    df = cluster_room[name_list[i]]
                    im = ax.imshow(df, cmap='BrBG', aspect='auto')

                    ax.set_xticks(range(len(df.columns)))
                    ax.set_xticklabels(df.columns.to_list())

                    ax.set_yticks(range(len(df.index)))
                    ax.set_yticklabels(["Independent" if c == -1 else f'Cluster {c}' for c in df.index])
                    ax.set_title(name_list[i])

                    for alpha in range(df.shape[0]):
                        for beta in range(df.shape[1]):
                            ax.text(beta, alpha, f"{df.iloc[alpha, beta]:.1f}%",
                                    ha='center', va='center',color='black')
                else:
                    ax.set_visible(False)
            plt.tight_layout()

        else:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
            df = cluster_room[city]
            im = ax.imshow(df, cmap='BrBG', aspect='auto')

            ax.set_xticks(range(len(df.columns)))
            ax.set_xticklabels(df.columns.to_list())

            ax.set_yticks(range(len(df.index)))
            ax.set_yticklabels(["Independent" if c == -1 else f'Cluster {c}' for c in df.index])
            ax.set_title(city)

            for alpha in range(df.shape[0]):
                for beta in range(df.shape[1]):
                    ax.text(beta, alpha, f"{df.iloc[alpha, beta]:.1f}%",
                            ha='center', va='center',color='black')

        return fig

    def room_host(self, city:str='Entire', figsize=(5,5)) -> plt.Figure:
        room_host = self.data.room_host
        name_list = self.data.names

        if (city not in name_list) and (city != 'Entire'):
            raise ValueError(f"City {city} not available")

        if city == 'Entire':
            fig, axs = plt.subplots(2, 3, figsize=figsize) #(15, 10) suggested

            for i, ax in enumerate(axs.flat):
                if i < len(room_host.keys()):
                    df = room_host[name_list[i]]
                    im = ax.imshow(df, cmap='BrBG', aspect='auto')
                    ax.set_xticks(range(len(df.columns)))
                    ax.set_xticklabels(df.columns.to_list())
                    ax.set_yticks(range(len(df.index)))
                    ax.set_yticklabels(df.index.to_list())
                    ax.set_title(name_list[i])

                    for alpha in range(df.shape[0]):
                        for beta in range(df.shape[1]):
                            ax.text(beta, alpha, f"{df.iloc[alpha, beta]:.1f}%",
                                    ha='center', va='center',color='black')
                else:
                    ax.set_visible(False)
            plt.tight_layout()

        else:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
            df = room_host[city]
            im = ax.imshow(df, cmap='BrBG', aspect='auto')
            ax.set_xticks(range(len(df.columns)))
            ax.set_xticklabels(df.columns.to_list())
            ax.set_yticks(range(len(df.index)))
            ax.set_yticklabels(df.index.to_list())
            ax.set_title(city)

            for alpha in range(df.shape[0]):
                for beta in range(df.shape[1]):
                    ax.text(beta, alpha, f"{df.iloc[alpha, beta]:.1f}%",
                            ha='center', va='center', color='black')

        return fig

    def borough_rooms(self, figsize=(5,5)) -> plt.Figure:
        borough_rooms = self.data.borough_rooms

        fig, ax = plt.subplots(1, 1, figsize=figsize) # (5,8) suggested
        im = ax.imshow(borough_rooms, cmap='BrBG', aspect='auto')
        ax.set_xticks(range(len(borough_rooms.columns)))
        ax.set_xticklabels(borough_rooms.columns.to_list())
        ax.set_yticks(range(len(borough_rooms.index)))
        ax.set_yticklabels(borough_rooms.index.to_list())
        ax.set_title("Room Percentages per Borough")

        for alpha in range(borough_rooms.shape[0]):
            for beta in range(borough_rooms.shape[1]):
                ax.text(beta, alpha, f"{borough_rooms.iloc[alpha, beta]:.1f}%",
                        ha='center', va='center', color='black')
        return fig

    def regression_coef(self, city:str='Entire', figsize=(5,5)) -> plt.Figure:
        price_models = self.data.price_models
        name_list = self.data.names

        if (city not in name_list) and (city != 'Entire'):
            raise ValueError(f"City {city} not available")

        if city == 'Entire':
            fig, axs = plt.subplots(2, 3, figsize=figsize) # (15, 10) suggested
            for i, ax in enumerate(axs.flat):
                if i < len(price_models.keys()):
                    df = (price_models[name_list[i]].params.drop("Intercept").
                          sort_values(key=abs, ascending=False))
                    ax.barh(df.index.tolist(), df)
                    ax.axvline(0, color='white', linestyle='--', alpha=0.4)
                    ax.set_title(name_list[i])
                    ax.grid(axis='x', alpha=0.2)
                else:
                    ax.set_visible(False)
            plt.tight_layout()
        else:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
            df = (price_models[city].params.drop("Intercept").
                  sort_values(key=abs, ascending=False))
            ax.barh(df.index.tolist(), df)
            ax.axvline(0, color='white', linestyle='--', alpha=0.4)
            ax.set_title(city)
            ax.grid(axis='x', alpha=0.2)

        return fig

    def city_availability(self, figsize=(5,5)) -> plt.Figure:
        city_availability = self.data.city_availability
        name_list = self.data.names

        dataset = [city_availability[name_list[i]]for i in range(len(name_list))]

        fig, ax = plt.subplots(1, 1, figsize=figsize) # (6,6) suggested

        ax.boxplot(dataset, showfliers=False, widths=0.18)
        violins = ax.violinplot(dataset = dataset, showmedians=True)

        for body in violins['bodies']:
            body.set_alpha(0.25)
            body.set_edgecolor('royalblue')
            body.set_linewidth(1)

        ax.set_xticks([1, 2, 3, 4, 5])
        ax.set_xticklabels(name_list)
        ax.set_ylabel('Availability (days)')
        ax.set_title('Availability within 90 days for Each City')
        return fig

    def borough_availability(self, figsize=(5,5)) -> plt.Figure:
        borough_availability = self.data.borough_availability
        dataset = [borough_availability[key] for key in borough_availability.keys()]
        fig, ax = plt.subplots(1, 1, figsize=figsize) # (6,6) suggested
        ax.boxplot(dataset, showfliers=False, widths=0.18)
        violins = ax.violinplot(dataset, showmeans=True, showmedians=True)

        for body in violins["bodies"]:
            body.set_alpha(0.25)
            body.set_edgecolor('royalblue')
            body.set_linewidth(1)

        ax.set_xticks(range(1, len(borough_availability.keys()) + 1))
        ax.set_xticklabels(borough_availability.keys())
        ax.set_ylabel("Available days until end of year")
        ax.set_title("Availability by NYC Borough")
        return fig

    def host_availability(self, figsize=(5,5)) -> plt.Figure:
        host_availability = self.data.host_availability
        fig, ax = plt.subplots(1, 1, figsize=figsize) # (9,6) suggested
        host_availability.plot.barh(ax=ax)
        ax.set_title('90 Day Availability for each Host Type')
        ax.set_xlabel("Median days available")
        ax.legend(loc='upper right', bbox_to_anchor=(1, 0.8), fontsize=10)
        ax.grid(axis='x', alpha=0.5)
        return fig

    def room_availability(self, figsize=(5,5)) -> plt.Figure:
        room_availability = self.data.room_availability
        fig, ax = plt.subplots(1, 1, figsize=figsize) # (9, 6) suggested
        room_availability.plot.barh(ax=ax)
        ax.set_title('90 Day Availability for each Room Type')
        ax.set_xlabel("Median days available")
        ax.legend(loc='upper right', bbox_to_anchor=(1, 0.87), fontsize=9)
        ax.grid(axis='x', alpha=0.5)
        return fig