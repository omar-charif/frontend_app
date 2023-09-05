# frontend_app
This tool is the webpage for displaying and analyzing scraped data.This Web app show the scrapped\
data in a table that could be filtered and ordered. It also displays the filtered and ordered data\
on animated bar plot. The animation is done and time. 

# Usage
To run locally follow the below steps:
- create a virtual environment
- activate it
- run: pip install -r requirements.txt
- run: gunicorn --bind 0.0.0.0:8050 app:server

This tool requires an environmental variable to work. The environmental variable is:
DATA_API_HOST=http://{address_Of_data_Scrapper_app}:5050 \
example when deploying locally both backend and frontend: DATA_API_HOST=http://172.17.0.1:5050 \
Note that, 172.17.0.1 is the ip address of the bridge network used by backend container.

# usage using docker
This app using the ci/cd pipline is deployed automatically to docker hub everytime a pull request\
to main is merged.

To deploy the app locally:
- pull the docker image: docker pull ocharif/frontend_app
- run the container:\
  docker run -it -e DATA_API_HOST=http://{address_Of_data_Scrapper_app}:5050 ocharif/frontend_app