def get_cities_in_region(np_df, region):
    return list(np_df[np_df['Область'] == region].sort_values(by='Місто')['Місто'].unique())