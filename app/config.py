import os

TITLE = "Sensorial"
DESCRIPTION = "Sensorial, sensor at your hand!"

IS_OFFLINE = bool(os.getenv("IS_OFFLINE", 0))

AWS_OFFLINE = {}
if IS_OFFLINE:
    AWS_OFFLINE = {"region_name": "us-east-1", "endpoint_url": "http://localstack:4566"}
