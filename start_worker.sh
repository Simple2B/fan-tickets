#!/bin/bash
poetry run celery -A app.scheduled_tasks.celery worker -B
