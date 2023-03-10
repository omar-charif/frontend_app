import pandas as pd
import requests

from logging_utils import get_logger

logger = get_logger("DataUtils")

# set constant
VALUE_COLUMN = "value"


def get_all_data(api_url: str = "", api_endpoint: str = "") -> pd.DataFrame:
    """
    get all data from api
    :param api_url: server url to hit with rest call
    :param api_endpoint: endpoint to call
    :return: pandas dataframe with the data
    """
    # submit api request
    if api_url == "":
        logger.error("Missing url for data restful api")
        return pd.DataFrame()

    if api_endpoint == "":
        logger.error("Missing endpoint param!")
        return pd.DataFrame()

    api_request_str = f"{api_url}/{api_endpoint}"
    response = requests.get(api_request_str)
    if response.status_code == 200:
        logger.info("Api call successful")
    else:
        logger.error(f"Api call failed  with {response.status_code}")

    response_json = response.json()

    num_rows_api_data = response_json["number_of_retrieved_rows"]

    data_df = pd.DataFrame(data=response_json["data"])

    if data_df.shape[0] != num_rows_api_data:
        logger.error("Something went wrong. Not all data rows were loaded!")
        return pd.DataFrame()

    logger.info(f"Retrieved {num_rows_api_data} from {api_request_str}")

    # read values as numeric
    data_df[VALUE_COLUMN] = pd.to_numeric(
        data_df[VALUE_COLUMN].replace(",", "", regex=True)
    )

    return data_df


if __name__ == "__main__":
    df = get_all_data(api_url=DATA_API_URL, api_endpoint=API_ENDPOINT)
    print(df.shape[0])
