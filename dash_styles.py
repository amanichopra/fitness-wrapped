from matplotlib import cm, colors


# Function to style dash tables
def discrete_background_color_bins(df, n_bins=7, columns='all', cmaps=['Blues', 'Reds', 'Oranges', 'Purples', 'Greens', 'Greys']):
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
        df_numeric_columns = df.select_dtypes('number')
    else:
        df_numeric_columns = df[columns]

    ranges = []
    for col in df_numeric_columns.columns:
        min_v = df_numeric_columns[col].min()
        max_v = df_numeric_columns[col].max()
        ranges.append([((max_v - min_v) * i) + min_v for i in bounds])  # equivalent to pd qcut

    styles = []
    for i, col in enumerate(df_numeric_columns.columns):
        norm = colors.Normalize(vmin=df_numeric_columns[col].min(), vmax=df_numeric_columns[col].max(), clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=cmaps[i])
        for i, val in enumerate(df_numeric_columns[col].values):
            r = '{:.2f}'.format(int(mapper.to_rgba(val)[0]*255) + 50)
            g = '{:.2f}'.format(int(mapper.to_rgba(val)[1]*255) + 50)
            b = '{:.2f}'.format(int(mapper.to_rgba(val)[2]*255) + 50)
            rgb = f'rgb({r},{g},{b})'
            styles.append({'if': {'row_index': i, 'column_id': col}, 'background-color': rgb})
    return styles


# Format df to have commas and no decimal places
def format_df(workouts_2021_monthly_stats):
    return workouts_2021_monthly_stats.apply(
        lambda x: x.astype(int).map('{:,}'.format) if x.dtype == float or x.dtype == int else x, axis=0)