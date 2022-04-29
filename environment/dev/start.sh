#!/bin/bash

docker-compose -f stack.dev.yml down

docker-compose -f stack.dev.yml up &

sleep 5

aws --endpoint-url=http://localhost:4566 dynamodb create-table --table-name sensorial.sattelite --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=2,WriteCapacityUnits=2
aws --endpoint-url=http://localhost:4566 dynamodb create-table --table-name sensorial.earthquake --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=2,WriteCapacityUnits=2
aws --endpoint-url=http://localhost:4566 dynamodb create-table --table-name sensorial.forecast --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=2,WriteCapacityUnits=2