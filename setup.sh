#!/bin/bash

# Install Python dependencies
pip install psycopg2 requests

# Run docker-compose up -d from the project folder
cd ./data_engineering_test_1
docker-compose up -d