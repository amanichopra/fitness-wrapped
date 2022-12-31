import plotly.graph_objects as go
from datetime import date


# FUNCTIONS TO LOAD DATA
def get_workout_map(path):
    return open(path).read()


def get_daily_stats_plot(workouts, date=date(2022, 1, 1)):
    day = workouts[workouts['Date'].dt.date == date].groupby('Workout').sum().reset_index()
    if day.empty: return None
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