#!/usr/bin/env bash
flask db upgrade &&
flask create-admin &&
flask db-populate &&
flask get-buyers
# flask set-subscriptions --username=$USERNAME