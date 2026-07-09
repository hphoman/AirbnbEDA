# Airbnb Market Explorer

An exploratory analysis of Airbnb markets across Austin, Chicago, Los
Angeles, New York, and Portland using September 2025 data from Inside
Airbnb.

## Project Overview

This project examines how short-term rental markets differ across and
within five U.S. cities. The analysis asks:

-   How do nightly prices vary across cities and local geographic
    clusters?
-   How are listings distributed among individual, small, and large
    hosts?
-   How does room composition vary across geography and host categories?
-   Which listing characteristics are associated with nightly price?
-   Do observed availability differ more by geography, host type, or
    room type?

The project includes a reproducible data pipeline, exploratory analysis,
spatial clustering, city-level regression models, a written report, and
an interactive Streamlit dashboard.

## Key Findings

-   Local geography is one of the strongest recurring sources of market
    variation.
-   Individual hosts make up the majority of hosts, but multi-listing
    hosts control a disproportionately large share of listings.
-   Entire homes and apartments dominate most markets; private rooms are
    more common in some local clusters and among small hosts.
-   For entire-home and apartment listings, bathrooms and accommodation
    capacity were statistically significant across all five city-level
    OLS models.
-   Review score and superhost status varied substantially across
    cities.
-   Availability differed more across geographic markets than across
    host or room categories.

## Data

Listing data come from the September 2025 releases provided by Inside
Airbnb.

Raw data are **not included in this repository**. Inside Airbnb requests
that users download data directly from its website. To reproduce the
project, download the appropriate city files and place them in the local
data directory expected by the ETL pipeline.

Cross-city population estimates were obtained from the U.S. Census
Bureau.

## Analysis Workflow

### Data Cleaning and Validation

The ETL pipeline standardizes numeric, boolean, and categorical columns;
converts nightly price to a numeric field; reduces the amenities field
to an amenity count; derives host categories; and identifies suspicious
observations using rule-based consistency checks.

The suspicious-listing procedure is intentionally conservative. High
price alone is not sufficient for removal. Listings are excluded only
when they violate hard-pass rules or contain multiple contradictory
indicators.

### Spatial Clustering

DBSCAN identifies geographic concentrations of listings because it
allows arbitrarily shaped clusters, does not require the number of
clusters to be chosen in advance, and labels isolated listings as noise.

`eps` and `min_samples` were selected separately for each city by
evaluating geographic interpretability and avoiding unnecessary
fragmentation of meaningful population centers. DBSCAN noise points are
labeled independent in the dashboard and report.

### Descriptive Analysis

The project compares median nightly price and price variability; price
across spatial clusters; host population and listing shares; price
across host categories; room composition across clusters, hosts, and New
York boroughs; and 90-day availability across cities, boroughs, host
categories, and room types.

### Regression Analysis

Separate ordinary least-squares models were fit for Entire
Home/Apartment listings in each city. The final explanatory variables
are accommodation capacity, superhost status, review score, and number
of bathrooms.

Shared rooms and hotel rooms were excluded because each represented less
than 1% of the combined observations. Private-room models were explored
but produced consistently weak explanatory power, so they were not
included in the final comparison.

## Interactive Dashboard

The Streamlit dashboard allows users to switch between the five cities,
inspect spatial DBSCAN clusters, compare pricing patterns, explore host
and room composition, review city-level regression coefficients and
significance, and compare availability distributions.

``` bash
git clone <repository-url>
cd <repository-name>

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
streamlit run dashboard/app.py
```

Since Inside Airbnb does not allow reuploading data, we will not be able to
publically host the data through Streamlit Community Cloud. Instead, you are
able to watch a short walkthrough of the dashboard here:

[Dashboard Demo](DashboardScreencast.mp4)

## Limitations

-   The analysis uses a single period of data and does not capture
    seasonality or long-term market change.
-   Availability does not distinguish booked nights from dates
    intentionally blocked by hosts.
-   The dataset does not include square footage, so variables such as
    bathrooms may partly proxy for overall property size.
-   Geographic and regulatory explanations are observational and should
    not be interpreted as causal.
-   The five-city population comparison is descriptive and is not
    sufficient for a general statistical relationship.

## Future Work

Potential extensions include incorporating multiple data snapshots,
expanding to additional cities, adding neighborhood-level socioeconomic
variables, testing alternative spatial models, and developing predictive
models as a separate task from the explanatory OLS analysis.

## Software Utilized

Python, pandas, NumPy, Matplotlib, scikit-learn, statsmodels, and Streamlit.