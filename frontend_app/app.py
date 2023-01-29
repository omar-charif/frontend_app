# If you prefer to run the code online instead of on your computer click:
# https://github.com/Coding-with-Adam/Dash-by-Plotly#execute-code-in-browser
import os
import sys

from dash import Dash, dash_table, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd  # pip install pandas
from frontend_app.utils.data_utils import get_all_data

from frontend_app.utils.logging_utils import get_logger

logger = get_logger("Beyond2020App")

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

# get all data
df = get_all_data(api_url=DATA_API_URL, api_endpoint=API_ENDPOINT)


def build_bashboard():
    # Build your components
    app = Dash(__name__, external_stylesheets=external_stylesheets)
    title = dcc.Markdown("Beyond 2020 Analytics", className="header-title")
    description = dcc.Markdown(
        children="Display and explore worldwide oil and gas products balance data "
        " specifically  the amount  of exported barrel per day"
        " for the period from September, 2021 to November, 2022",
        className="header-description",
    )
    data_table = dash_table.DataTable(
        id="datatable-interactivity",
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True}
            for i in df.columns
        ],
        data=df.to_dict("records"),
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
    )
    graph = dcc.Graph(figure={})

    # Customize your own Layout
    app.layout = dbc.Container(
        [
            dbc.Row([dbc.Col([title])], className="header"),
            dbc.Row([dbc.Col([description])], className="header"),
            dbc.Row([dbc.Col([data_table], className="table")]),
            dbc.Row([dbc.Col([graph], width=12)]),
        ],
        fluid=True,
    )

    # detect if table change and update based on selection and filters in the table
    @app.callback(
        Output("datatable-interactivity", "style_data_conditional"),
        Input("datatable-interactivity", "selected_columns"),
    )
    def update_styles(selected_columns):
        return [
            {"if": {"column_id": i}, "background_color": "#D2F3FF"}
            for i in selected_columns
        ]

    # Callback allows components to interact
    @app.callback(
        Output(graph, "figure"),
        Input("datatable-interactivity", "derived_virtual_data"),
    )
    def update_graph(
        rows,
    ):  # function arguments come from the component property of the Input

        dff = df if rows is None else pd.DataFrame(rows)
        min_value = dff[VALUE_COLUMN].min()
        max_value = dff[VALUE_COLUMN].max()
        logger.info(f"{min_value}, {type(min_value)}")
        logger.info(f"{max_value}, {type(max_value)}")

        fig = px.bar(
            dff,
            x=KEY_COLUMN,
            y=VALUE_COLUMN,
            color=VALUE_COLUMN,
            animation_frame=MONTH_YEAR_COLUMN,
            animation_group=KEY_COLUMN,
            range_y=[min_value, max_value],
        )

        return fig

    return app


def main():
    # function that will run the app
    app = build_bashboard()
    app.run_server(debug=True)


# Run app
if __name__ == "__main__":
    sys.exit(main())
