LOGGER = {
    'version': 1,
    'formatters': {'default': {
        'format':
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
}
DB_HOST = '127.0.0.1'
DB_USER = 'postgres'
DB_PORT = '5432'
DB_PASSWORD = 'postgres'
DB_NAME = 'gardener_testing'
