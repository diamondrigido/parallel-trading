import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


API_KEY = ""
API_SECRET = ""


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] - %(processName)s %(message)s'
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
        'file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'default_formatter',
            'filename': os.path.join(BASE_DIR, "time_process.log")
        }
    },

    'loggers': {
        'root': {
            'handlers': ['stream_handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'time_process': {
            'handlers': ['file_handler'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
