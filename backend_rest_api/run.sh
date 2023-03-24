#!/bin/bash
gunicorn --reload -c gunicorn.conf.py server:app
