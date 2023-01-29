from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import os

from frontend_app.app_utils.data_utils import get_all_data

# set constant data
DATA_API_URL = os.environ["DATA_API_HOST"]
API_ENDPOINT = "retrieve-data"
KEY_COLUMN = "country"
VALUE_COLUMN = "value"
MONTH_YEAR_COLUMN = "month_year"

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]


image_path = 'assets/oil_rig_small.png'


def build_dashboard():
    # build interactive web page

    # retrieve all data
    df = get_all_data(api_url=DATA_API_URL, api_endpoint=API_ENDPOINT)
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([
        html.Div(
            children=[
                html.Div(html.Img(src=image_path), className="header-img"),
                html.H1(
                    children="Beyond 2020 Analytics", className="header-title"
                ),
                html.P(
                    children="Display and explore worldwide oil and gas products balance data "
                             " specifically  the amount  of exported barrel per day"
                             " for the period from September, 2021 to November, 2022",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
            ],
            data=df.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=10,
        ),
        html.Div(id='datatable-interactivity-container')
    ])

    @app.callback(
        Output('datatable-interactivity', 'style_data_conditional'),
        Input('datatable-interactivity', 'selected_columns')
    )
    def update_styles(selected_columns):
        return [{
            'if': {'column_id': i},
            'background_color': '#D2F3FF'
        } for i in selected_columns]

    @app.callback(
        Output('datatable-interactivity-container', "children"),
        Input('datatable-interactivity', "derived_virtual_data"),
        Input('datatable-interactivity', "derived_virtual_selected_rows"))
    def update_graphs(rows, derived_virtual_selected_rows):
        # When the table is first rendered, `derived_virtual_data` and
        # `derived_virtual_selected_rows` will be `None`. This is due to an
        # idiosyncrasy in Dash (unsupplied properties are always None and Dash
        # calls the dependent callbacks when the component is first rendered).
        # So, if `rows` is `None`, then the component was just rendered
        # and its value will be the same as the component's dataframe.
        # Instead of setting `None` in here, you could also set
        # `derived_virtual_data=df.to_rows('dict')` when you initialize
        # the component.
        if derived_virtual_selected_rows is None:
            derived_virtual_selected_rows = []

        dff = df if rows is None else pd.DataFrame(rows)

        colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
                  for i in range(len(dff))]

        return [
            # dcc.Graph(figure=)
            dcc.Graph(
                id=VALUE_COLUMN,
                figure={
                    "data": [
                        {
                            "x": dff[KEY_COLUMN],
                            "y": dff[VALUE_COLUMN],
                            "type": "bar",
                            "marker": {"color": colors},
                        }
                    ],
                    "layout": {
                        "xaxis": {"automargin": True},
                        "yaxis": {
                            "automargin": True,
                            "title": {"text": VALUE_COLUMN}
                        },
                        "height": 600,
                        "margin": {"t": 50, "l": 50, "r": 50},
                    },
                },
            )
        ]

    return app


if __name__ == '__main__':
    app = build_dashboard()
    app.run_server(debug=True)
