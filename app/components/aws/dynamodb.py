from __future__ import annotations

import boto3
from app.config import AWS_OFFLINE
from boto3.dynamodb.conditions import Key


class DynamoDBService:

    __slots__ = ("session", "client", "table")

    def __init__(self, table_name: str) -> None:
        self.session = boto3.Session()
        self.client = self.session.resource("dynamodb", **AWS_OFFLINE)
        self.table = self.client.Table(table_name)

    def __enter__(self) -> DynamoDBService:
        return self

    def __exit__(self, *args: list) -> None:
        self.close()

    def close(self) -> None:
        self.table = None
        self.client = None
        self.session = None

    def add(self, item: dict):
        self.table.put_item(Item=item)

    def remove(self, dict_query: dict):
        self.table.delete_item(Key=dict_query)

    def get_item(self, item_id: dict) -> list[dict]:
        response = self.table.get_item(Key={"id": item_id})
        if "Item" in response:
            return response["Item"]
        return []

    def query(self, query_expression: Key):
        response = self.table.query(KeyConditionExpression=query_expression)
        if "Items" in response:
            return response["Items"]
        return []
