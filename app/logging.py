

LOGGING = {
        'version': 1,                       # the dictConfig format version
        'disable_existing_loggers': False,  # retain the default loggers
        'formatters': {
            'main_format': {
                        'format': '{asctime} - {levelname} - {module} - {funcName} - {filename} - {message}',
                        'style': '{',
            },
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
        },
        },
        'handlers': {
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'debug.log',
                'formatter': 'main_format',
                'filters': ['require_debug_true'],
                'level': 'DEBUG',
            },
        
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'main_format',
            },
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }

    
