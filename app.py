from flask import Flask, render_template
from dash import Dash
from dash import dash_table
from data import *
from dash import dcc
from dash_styles import *
from dash.dependencies import Input, Output
from datetime import date, datetime
from dash import html
import base64
from io import BytesIO
import pickle
from plotly.io import read_json
from PIL import Image

# GLOBAL
DFS_PATH = r'./data/dfs.dat'
STATS_PATH  = './data/stats.dat'
HOURLY_ACTIVITY_PLOT_PATH = r'./data/hourly_activity_plot.json'
WC_PATH = r'./data/wc.png'

MB_B = r'./data/macro_breakdown_plot_bf.json'
MB_MS = r'./data/macro_breakdown_plot_morn_s.json'
MB_L = r'./data/macro_breakdown_plot_l.json'
MB_MDYS = r'./data/macro_breakdown_plot_midday_s.json'
MB_D = r'./data/macro_breakdown_plot_d.json'
MD_PD = r'./data/macro_breakdown_plot_pd.json'

OVERVIEW_HRS_PLOT_PATH = r'./data/overview_hrs_plot.json'
OVERVIEW_CAL_PLOT_PATH = r'./data/overview_cal_plot.json'
OVERVIEW_FREQ_PLOT_PATH = r'./data/overview_freq_plot.json'

# LOAD DATA
with open(DFS_PATH, 'rb') as f:
    workouts, m_stats, _, top_10_lifts = pickle.load(f)

m_stats_table_style = discrete_background_color_bins(m_stats) # monthly stats styling for dashboard
m_stats = format_df(m_stats) # format monthly stats to remove decimals, etc

top_10_lifts_table_style = discrete_background_color_bins(top_10_lifts) # format lifts data to remove decimals, etc

workout_map = get_workout_map()

# LOAD STATS
with open(STATS_PATH, 'rb') as f:
    stats = pickle.load(f)

total_weight_lifted = stats['total_weight_lifted']
total_reps_lifted = stats['total_reps_lifted']
total_num_workouts = stats['total_num_workouts']
total_time_spent = stats['total_time_spent']
total_cal_burned = stats['total_cal_burned']
total_step_count = stats['total_step_count']
total_dist_traveled = stats['total_dist_traveled']
avg_daily_expenditure = stats['avg_daily_expenditure']
avg_daily_exercise_time = int(stats['avg_daily_exercise_time'])
avg_daily_exercise_time_hrs = int(avg_daily_exercise_time / 60)
avg_daily_exercise_time_mins = int(avg_daily_exercise_time % 60)
avg_daily_calories = stats['avg_daily_calories']

# LOAD PLOTS
overview_plots = {'Hours Spent': read_json(OVERVIEW_HRS_PLOT_PATH), 'Calories Burned': read_json(OVERVIEW_CAL_PLOT_PATH),
    'Frequency': read_json(OVERVIEW_FREQ_PLOT_PATH)}
hourly_activity_plot = read_json(HOURLY_ACTIVITY_PLOT_PATH)
daily_stats_plot = get_daily_stats_plot(workouts)
macro_breakdown_plots = {'Breakfast': read_json(MB_B), 'Morning Snack': read_json(MB_MS),
    'Lunch': read_json(MB_L), 'Midday Snack': read_json(MB_MDYS), 'Dinner': read_json(MB_D), 'Post Dinner': read_json(MD_PD)}
nutrition_wordcloud = Image.open(WC_PATH)

# LOAD CSS STYLESHEETS AND JS FILES
stylesheets = ['./static/css/dash.css'] # CSS stylesheets
scripts = ['./static/js/vendor/jquery-2.2.4.min.js', './static/js/vendor/bootstrap.min.js', './static/js/isotope.pkgd.min.js',
 './static/js/jquery.nicescroll.min.js', '/static/js/owl.carousel.min.js', './static/js/jquery-validation.min.js',
 './static/js/form.min.js', './static/js/main.js']

# LOAD SERVER
app = Flask(__name__)

# LOAD DASH APP
dash = Dash(__name__, external_stylesheets=stylesheets, external_scripts=scripts, url_base_pathname='/wrapped/', server=app)
dash.title = '2021 Wrapped'

# SET DASH LAYOUT
dash.layout = html.Div(children=[
    html.Div(className='wrap', children=[
        html.Div(className='container', children=[
            html.Div(className='text', children=[
                html.Span("2021's been a great year! I've completed over ", className='spanp'),
                html.Span(f"{'{:,}'.format(total_num_workouts)} workouts, ", className='s'),
                html.Span("totaling ", className='spanp'),
                html.Span(f"{'{:,}'.format(total_time_spent[0])} hours {'{:,}'.format(total_time_spent[1])} minutes {'{:,}'.format(total_time_spent[2])} seconds ", className='s'),
                html.Span("and ", className='spanp'),
                html.Span(f"{'{:,}'.format(int(total_cal_burned))} calories ", className='s'),
                html.Span("burned!", className='spanp')
            ])
        ]),

        html.Div(className='section', children=[
            html.H2('Overview of Workout Types', className="spanp", style={'font-size': 22, 'display': 'table', 'margin-top': 0}),
            dcc.Dropdown(id='workout-overview-dropdown',
                className='workout-overview-dropdown',
                options=[
                    {'label': 'Hours Spent', 'value': 'Hours Spent'},
                    {'label': 'Calories Burned', 'value': 'Calories Burned'},
                    {'label': 'Frequency', 'value': 'Frequency'}],
                    placeholder='Select a metric.'),
            dcc.Graph(id='workout-overview-plot', figure=overview_plots['Hours Spent'])
        ]),

        html.Br(),

        html.Div(className='section', style={'padding-bottom': '5px'}, children=[
            html.H2('Monthly Statistics', className="spanp", style={'font-size': 22, 'display': 'table', 'margin-top': 0}),
            dash_table.DataTable(id='monthly-stats',
                columns=[{"name": i, "id": i} for i in m_stats.columns],
                data=m_stats.to_dict('records'), style_data={
                'backgroundColor': 'transparent'}, style_as_list_view=True,
                style_header={'font-weight': 'bold'},
                style_cell={'font-family': 'Impact, Haettenschweiler, "Franklin Gothic Bold", '
                'Charcoal, "Helvetica Inserat", "Bitstream Vera Sans Bold", "Arial Black", "sans serif"'},
                style_data_conditional=[{
                "if": {"state": "selected"},
                "backgroundColor": "inherit !important",
                "border": "inherit !important"}] + m_stats_table_style)
        ]),

        html.Br(),

        html.Div(className='container', children=[
            html.Div(className='text', children=[
                html.Span("I love being on my feet. This year, I've walked ", className='spanp'),
                html.Span(f"{'{:,}'.format(total_step_count)} steps ", className='s'),
                html.Span("and ", className='spanp'),
                html.Span(f"{'{:,}'.format(int(total_dist_traveled))} miles. ", className='s'),
                html.Span("At this rate, in 3 years, I would have walked the full circumference of Earth!", className='spanp')
            ])
        ]),

        html.Div(className='section', style={'padding-bottom': '5px'}, children=[
            html.H2('The Walking Visualizer', className="spanp", style={'font-size': 22, 'display': 'table', 'margin-top': 0}),
            html.Iframe(id='workout-map', srcDoc=workout_map, width='80%', height='700')
        ]),

        html.Br(),

        html.Div(className='container', children=[
            html.Div(className='text', children=[
                html.Span("In a typical day, I burn ", className='spanp')]),
                html.Span(f"{'{:,}'.format(int(avg_daily_calories))} calories ", className='s', style={'padding-left': '4px'}),
                html.Span("and spend ", className='spanp', style={'padding-left': '4px'}),
                html.Span(f"{'{:,}'.format(avg_daily_exercise_time_hrs)} hours {'{:,}'.format(avg_daily_exercise_time_mins)} minutes ", className='s', style={'padding-left': '4px'}),
                html.Span("on exercise!", className='spanp', style={'padding-left': '4px'})
        ]),

        html.Div(className='section', children=[
            html.H2('Hourly Activity', className="spanp", style={'font-size': 22, 'display': 'table', 'margin-top': 0}),
            dcc.Graph(id='hourly-activity-plot', figure=hourly_activity_plot)
        ]),

        html.Br(),

        html.Div(className='section', children=[
            html.H2('Daily Statistics', className="spanp", style={'font-size': 22, 'display': 'table', 'margin-top': 0}),
            dcc.DatePickerSingle(
                id='daily-stats-date-picker',
                min_date_allowed=date(2021, 1, 1),
                max_date_allowed=date(2021, 12, 31),
                initial_visible_month=date(2021, 1, 1),
                date=date(2021, 1, 1)),
            dcc.Graph(id='daily-stats-plot', figure=daily_stats_plot)
        ]),

        html.Br(),

        html.Div(className='container', children=[
            html.Div(className='text', children=[
                html.Span("The gym is sanctuary. I've lifted ", className='spanp'),
                html.Span(f"{'{:,}'.format(int(total_weight_lifted))} lbs ", className='s'),
                html.Span("and ", className='spanp'),
                html.Span(f"{'{:,}'.format(int(total_reps_lifted))} reps ", className='s'),
                html.Span("this year!", className='spanp')
            ])
        ]),

        html.Div(className='section', style={'padding-bottom': '5px'}, children=[
            html.H2('My Top 10 Favorite Lifts', className="spanp", style={'font-size': 22, 'display': 'table', 'margin-top': 0}),
            dash_table.DataTable(id='top-10-lifts',
                columns=[{"name": i, "id": i} for i in top_10_lifts.columns],
                data=top_10_lifts.to_dict('records'), style_data={
                'backgroundColor': 'transparent'}, style_as_list_view=True,
                style_header={'font-weight': 'bold'},
                style_cell={'font-family': 'Impact, Haettenschweiler, "Franklin Gothic Bold", '
                'Charcoal, "Helvetica Inserat", "Bitstream Vera Sans Bold", "Arial Black", "sans serif"'},
                style_data_conditional=[{
                "if": {"state": "selected"},
                "backgroundColor": "inherit !important",
                "border": "inherit !important",
                }] + top_10_lifts_table_style)
        ]),

        html.Br(),

        html.Div(className='container', children=[
            html.Div(className='text', children=[
                html.Span("Nutrition is key. I consume an average of ", className='spanp')]),
                html.Span(f"{'{:,}'.format(int(avg_daily_calories))} calories ", className='s', style={'padding-left': '4px'}),
                html.Span("over 5 meals each day.", className='spanp', style={'padding-left': '4px'})
        ]),

        html.Div(className='section', style={'padding-bottom': '5px'}, children=[
            html.H2('Macronutrient Breakdown', className="spanp", style={'font-size': 22, 'display': 'table', 'margin-top': 0}),
            dcc.Dropdown(id='macro-breakdown-dropdown',
                className='macro-breakdown-dropdown',
                options=[
                    {'label': 'Breakfast', 'value': 'Breakfast'},
                    {'label': 'Morning Snack', 'value': 'Morning Snack'},
                    {'label': 'Lunch', 'value': 'Lunch'},
                    {'label': 'Midday Snack', 'value': 'Midday Snack'},
                    {'label': 'Dinner', 'value': 'Dinner'},
                    {'label': 'Post Dinner', 'value': 'Post Dinner'}],
                    placeholder='Select a meal.'),
            dcc.Graph(id='macro-breakdown-plot', figure=macro_breakdown_plots['Breakfast'])
        ]),

        html.Br(),

        html.Div(className='section', style={'padding-bottom': '5px'}, children=[
            html.H2('Most Frequently Eaten Foods', className="spanp", style={'font-size': 22, 'display': 'table', 'margin-top': 0}),
            html.Img(id='wc')
        ])
    ])
])


# SET CALLBACKS
@dash.callback(
    Output('workout-overview-plot', 'figure'),
    Input('workout-overview-dropdown', 'value'))
def update_workouts_overview(metric):
    return overview_plots['metric']


@dash.callback(
    Output('daily-stats-plot', 'figure'),
    Input('daily-stats-date-picker', 'date'))
def update_daily_stats_plot(date):
    date = datetime.strptime(date, '%Y-%m-%d').date()
    return get_daily_stats_plot(workouts, date=date)


@dash.callback(
    Output('macro-breakdown-plot', 'figure'),
    Input('macro-breakdown-dropdown', 'value'))
def update_macro_breakdown(meal):
    return macro_breakdown_plots[meal]


@dash.callback(
    Output('wc', 'src'),
    Input('wc', 'id'))
def make_image(placeholder):
    img = BytesIO()
    nutrition_wordcloud.save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


# SET ROUTES
@app.route("/")
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
