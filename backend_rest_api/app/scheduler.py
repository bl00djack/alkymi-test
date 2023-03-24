from flask import Flask
from flask_apscheduler import APScheduler
from app.scheduler_jobs import process_data_file


class ConfigScheduler:
    JOBS = [
        {
            'id': 'process_data_file',
            'func': process_data_file,
            'trigger': 'interval',
            'seconds': 5,
            'timezone': 'UTC'
        },
    ]
    SCHEDULER_API_ENABLED = True


def add_scheduler(app: Flask):
    app.config.from_object(ConfigScheduler())

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
