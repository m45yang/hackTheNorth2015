# hackTheNorth2015
Matthew, Jake, Jimmy and James

Run the server using this command:

- First go to the `python_server` dir:

`cd python_server`

- Then run:

`uwsgi --master --http :8080 --http-websockets --wsgi app:app`