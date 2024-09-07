import requests
from time import sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text


random.seed(100)


class AWSDBConnector:
    """
    Manages the connection to an AWS RDS database.
    """

    def __init__(self):
        """
        Initializes the database connection details.
        """
        self.HOST = "pinterestdbreadonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com"
        self.USER = 'project_user'
        self.PASSWORD = ':t%;yCY3Yjg'
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        """
        Creates and returns a database connection.
        """
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine


new_connector = AWSDBConnector()


def send_to_kinesis(data, topic):
    """
    Sends data to an AWS Kinesis stream.
    """
    invoke_url = f"https://8qb57an8qh.execute-api.us-east-1.amazonaws.com/test/streams/streaming-12ffc5aba733-{topic}/record"
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({
        "StreamName": f"streaming-12ffc5aba733-{topic}",
        "Data": data,
        "PartitionKey": f"Partition_{topic}"
    }, default=str)

    response = requests.put(invoke_url, headers=headers, data=payload, timeout=30)

    if response.status_code == 200:
        print(f"Data sent successfully to {topic}")
        print(response.json())
    else:
        print(f"Failed to send data to {topic}: {response.status_code} - {response.text}")


def run_infinite_post_data_loop():
    """
    Runs an endless loop that fetches random rows from the database
    and sends the data to Kinesis streams.
    """
    while True:
        sleep(random.randrange(0, 2))  # Pause for 0-2 seconds
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:
            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            for row in pin_selected_row:
                pin_result = dict(row._mapping)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            for row in geo_selected_row:
                geo_result = dict(row._mapping)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            for row in user_selected_row:
                user_result = dict(row._mapping)

            # Send data to Kinesis
            send_to_kinesis(pin_result, "pin")
            send_to_kinesis(geo_result, "geo")
            send_to_kinesis(user_result, "user")


if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')