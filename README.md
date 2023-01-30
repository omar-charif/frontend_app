# frontend_app
This tool is the webpage for displaying and analyzing scraped data.

# Usage
Currently the Dockerfile is broken. Therefore, to run locally follow the below steps:
- create a virtual environment
- activate it
- run: pip install -r requirements.txt
- run: gunicorn --bind 0.0.0.0:8050 app:server