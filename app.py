# app.py
import dash
from dash import Dash, dcc, html, Input, Output
from dash import dash_table
from fetch_standings import get_epl_standings, get_upcoming_fixtures, get_top_scorers, slugify

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', style={"color": "black"})
])

def main_page():
    return html.Div([
        html.H1("Premier League Standings (Live)", style={"textAlign": "center"}),
        dcc.Interval(id="interval-refresh", interval=5*60*1000, n_intervals=0),
        html.Div(id='standings-table'),
        html.Br(),
        html.Div(id='fixtures-display', style={"marginTop": "30px"}),
        
    ], style={
        "backgroundImage": "url('/assets/bg1.png')",
        "backgroundSize": "cover",
        "backgroundRepeat": "no-repeat",
        "backgroundAttachment": "fixed",
        "minHeight": "100vh",
        "padding": "20px"
    })

@app.callback(
    [Output('standings-table', 'children'), Output('fixtures-display', 'children')],
    Input('interval-refresh', 'n_intervals')
)
def update_content(n):
    rows = get_epl_standings()
    gameday, fixtures = get_upcoming_fixtures()

    headers = list(rows[0].keys())
    table_header = html.Tr([html.Th(h, style={"border": "1px solid black", "backgroundColor": "rgba(255,255,255,0.8)"}) for h in headers])
    table_body = []

    for i, row in enumerate(rows):
        bg = "rgba(212, 237, 218, 0.8)" if row["Position"] <= 4 else ("rgba(248, 215, 218, 0.8)" if row["Position"] >= 18 else ("rgba(255,255,255,0.8)" if i % 2 == 0 else "rgba(255,255,255,0.6)"))
        table_body.append(
            html.Tr([
                html.Td(row["Position"], style={"border": "1px solid black"}),
                html.Td(
                    html.Div([
                        html.Img(src=row["Team"]["logo"], height="20px", style={"marginRight": "5px"}),
                        html.Span(row["Team"]["name"], style={"color": "black"})
                    ], style={"display": "flex", "alignItems": "center", "justifyContent": "center"}),
                    style={"border": "1px solid black"}
                ),
                html.Td(row["Played"], style={"border": "1px solid black"}),
                html.Td(row["Wins"], style={"border": "1px solid black"}),
                html.Td(row["Draws"], style={"border": "1px solid black"}),
                html.Td(row["Losses"], style={"border": "1px solid black"}),
                html.Td(row["Points"], style={"border": "1px solid black"}),
                html.Td(row["Goal Difference"], style={"border": "1px solid black"})
            ], style={"backgroundColor": bg})
        )

    table = html.Table([
        html.Thead(table_header),
        html.Tbody(table_body)
    ], style={
        "width": "100%",
        "textAlign": "center",
        "borderCollapse": "collapse",
        "border": "1px solid black",
        "backgroundColor": "transparent"
    })

    fixtures_section = html.Div([
        html.H2(f"Upcoming Fixtures - Matchday {gameday}", style={"textAlign": "center", "color": "black"}),
        html.Div([
            html.Div([
                html.Div([
                    html.Img(src=f"/assets/{slugify(fix['home'])}.png", height="30px", style={"marginRight": "10px"}),
                    html.Strong(fix['home']),
                    html.Span(" vs ", style={"margin": "0 10px"}),
                    html.Strong(fix['away']),
                    html.Img(src=f"/assets/{slugify(fix['away'])}.png", height="30px", style={"marginLeft": "10px"})
                ], style={"display": "flex", "alignItems": "center", "justifyContent": "center"}),
                html.Div(fix['date'] + ' ' + fix['time'], style={"marginTop": "5px", "fontStyle": "italic"})
            ], style={
                "backgroundColor": "rgba(255, 255, 255, 0.8)",
                "padding": "10px",
                "margin": "10px auto",
                "borderRadius": "10px",
                "textAlign": "center",
                "width": "320px"
            }) for fix in fixtures
        ])
    ])

    return table, fixtures_section

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    return main_page()

if __name__ == "__main__":
    app.run(debug=True)