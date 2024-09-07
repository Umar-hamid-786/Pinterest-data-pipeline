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


def send_to_kafka(data, topic):
    """
    Sends data to the given Kafka topic.
    """
    invoke_url = f"https://8qb57an8qh.execute-api.us-east-1.amazonaws.com/test/topics/{topic}"
    
    payload = json.dumps({
        "records": [{"value": data}]
    })

    headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
    response = requests.post(invoke_url, headers=headers, data=payload)

    if response.status_code == 200:
        print(f"Data sent successfully to {topic}")
    else:
        print(f"Failed to send data to {topic}: {response.status_code} - {response.text}")

        
def run_infinite_post_data_loop():
    """
    Runs an endless loop that fetches random rows from the database
    and sends the data to Kafka topics.
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
                send_to_kafka(pin_result, "12ffc5aba733.pin")

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)
                send_to_kafka(geo_result, "12ffc5aba733.geo")

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)
                send_to_kafka(user_result, "12ffc5aba733.user")

            print(pin_result)
            print(geo_result)
            print(user_result)


if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')


