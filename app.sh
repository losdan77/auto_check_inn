#!/bin/bash

gunicorn main:app --workers 2 --timeout 960 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

