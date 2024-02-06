sleep 2
poetry run flask print-users
echo Run db upgrade
poetry run flask db upgrade
# echo Run app
echo Run app server
poetry run gunicorn -w 4 --worker-class gevent -b 0.0.0.0 'wsgi:app'
