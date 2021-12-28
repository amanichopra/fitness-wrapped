import plotly.graph_objects as go
from datetime import date

# PATH VARS
WORKOUTS_PATH = r'./data/Workout_Processed.csv'
WORKOUT_MAP_PATH = r'./data/walks.html'


# FUNCTIONS TO LOAD DATA
def get_workout_map(path=WORKOUT_MAP_PATH):
    return open(path).read()


# FUNCTIONS TO GET PLOTS
def get_workout_overview_plot(workouts, metric='Hours Spent'):
    if metric == 'Hours Spent':
        workouts = workouts.groupby('Workout')['Duration (min)'].sum() / 60
    elif metric == 'Calories Burned':
        workouts = workouts.groupby('Workout')['Calories Burned'].sum()
    elif metric == 'Frequency':
        workouts = workouts.groupby('Workout')['Date'].count()

    lollipop = go.Figure()
    # Draw points
    lollipop.add_trace(go.Scatter(y=workouts,
                                  x=workouts.index,
                                  mode='markers',
                                  marker_color='#000fff',
                                  marker_size=10))
    # Draw lines
    for i in range(0, workouts.index.shape[0]):
        lollipop.add_shape(type='line',
            y0=0, x0=i,
            y1=workouts.iloc[i],
            x1=i,
            line=dict(color='black', width=3))

    # Set style
    lollipop.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    lollipop.update_xaxes(title='Workout')
    lollipop.update_yaxes(title=metric)
    lollipop.update_layout(font_family='Impact, Haettenschweiler, "Franklin Gothic Bold", Charcoal, "Helvetica Inserat", "Bitstream Vera Sans Bold", "Arial Black", "sans serif"', font_size=15, font_color='#000fff')
    lollipop.update_layout(margin={'l': 50, 'r': 50, 'b': 50, 't': 10, 'pad': 4})

    return lollipop


def get_daily_stats_plot(workouts, date=date(2021, 1, 1)):
    day = workouts[workouts['Date'].dt.date == date].groupby('Workout').sum().reset_index()
    day['Workout'] = day.apply(
        lambda x: f"{x['Workout']} ({round(x['Distance (mi)'], 2)}mi)" if x['Distance (mi)'] != 0 else x['Workout'],
        axis=1)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=day['Workout'], y=day['Duration (min)'], name='Duration (min)', marker={'color': 'black'}))
    fig.add_trace(go.Bar(x=day['Workout'], y=day['Calories Burned'], name='Calories Burned', marker={'color': '#000fff'}))

    fig.update_xaxes(title_text="Workout")
    fig.update_yaxes(title_text="Value")
    fig.update_layout(
        font_family='Impact, Haettenschweiler, "Franklin Gothic Bold", Charcoal, "Helvetica Inserat", "Bitstream Vera Sans Bold", "Arial Black", "sans serif"',
        font_size = 15, font_color = '#000fff')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(margin={'l': 50, 'r': 50, 'b': 50, 't': 10, 'pad': 4})

    return fig