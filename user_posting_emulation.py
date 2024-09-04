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

    def __init__(self):

        self.HOST = "pinterestdbreadonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com"
        self.USER = 'project_user'
        self.PASSWORD = ':t%;yCY3Yjg'
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine


new_connector = AWSDBConnector()


def send_to_kinesis(data, topic, partition_key):
    invoke_url = f"https://8qb57an8qh.execute-api.us-east-1.amazonaws.com/test/streams/streaming-12ffc5aba733-{topic}/record"

    payload = json.dumps({
        "StreamName": f"streaming-12ffc5aba733-{topic}",
        "Data": [
            {
                "value": data
            }
        ],
        "PartitionKey": str(partition_key)
    }, default=str)

    headers = {'Content-Type': 'application/json'}

    response = requests.request("PUT", invoke_url, headers=headers, data=payload)

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Data sent successfully to {topic}")
        print(response.json())
    else:
        print(f"Failed to send data to {topic}: {response.status_code} - {response.text}")



def run_infinite_post_data_loop():
    while True:
        sleep(random.randrange(0, 2))
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


            send_to_kinesis(pin_result, "pin", 5)
            send_to_kinesis(geo_result, "geo", 5)
            send_to_kinesis(user_result, "user", 5)
            
            #print(pin_result)
            #print(geo_result)
            #print(user_result)


if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')
    
    


