## hackTheNorth2015
A tool that lets you query Tweets for a particular topic (e.g. Donald Trump) and aggregates the general sentiment of recent Tweets for that topic. A Flask app powered by indico.io's machine learning API. \
Built by Matthew, Jake, Jimmy and James.

### Running the server:

- First navigate to the `python_server` directory:

`cd python_server`

- Then run:

`uwsgi --master --http :8080 --http-websockets --wsgi app:app`

View the app at https://localhost:8080.
