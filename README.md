- [Overview of project](#overview)
- [Project Aim](#project-structure)
- [Project structure](#project-structure)
- [What did I learn and what I found challenging](#challenge)
- [Installation and Usage instructions](#installation)
- [Future Enhancements](#future-enhancements)
- [License information](#license)



## Overview of Project
This project emulates the data processing system used by Pinterest to crunch massive amounts of data and provide personalized recommendations and insights to users. Utilizing various AWS services, the project implements an end-to-end data engineering pipeline that leverages both batch and real-time (streaming) data to analyze over 30,000 rows of data, employing robust distributed computing and processing techniques.

## Project Aim 
The goal of this project is to build an efficient, scalable data pipeline on AWS that handles both batch and streaming data. The system processes, stores, and analyzes data using key AWS services such as MSK (Managed Streaming for Apache Kafka), S3, Kinesis, Databricks, and MWAA (Managed Workflows for Apache Airflow), simulating the real-world data flow management techniques used by Pinterest.

## Project Structure 
The project follows a modular architecture that integrates various AWS services to manage different phases of data processing:

Data Ingestion:

Provisioned an API Gateway RESTful API to leverage a Kafka REST proxy.
Data was sent to 3 different Kafka topics on AWS MSK (Managed Streaming for Apache Kafka).
Batch Processing:

Batch data was distributed from MSK to an AWS S3 data lake using an MSK Connect plugin-connector pair.
Custom Spark transformations were created on Databricks to clean and aggregate the data in the S3 data lake.
Real-time (Stream) Processing:

Streamed data in real-time using 3 AWS Kinesis data streams.
Near real-time analysis was performed using Spark Structured Streaming on Databricks.
Automation:

Databricks workloads were automated to run daily using custom DAG scripts on MWAA (Managed Workflows for Apache Airflow).

## What Did I Learn and What I Found Challenging 
Key Learnings:

Deepened my understanding of distributed computing with Kafka and Spark.
Gained practical experience in working with various AWS services such as MSK, Kinesis, S3, Databricks, and MWAA.
Learned how to architect scalable systems for both batch and real-time data processing.
Challenges:

Configuring MSK Connect with appropriate plugin-connector pairs for seamless data transfer to S3.
Ensuring the real-time pipeline with Kinesis and Spark Streaming was optimized for low-latency processing.
Automating complex workflows in MWAA and debugging DAG execution issues.

## Installation and Usage Instructions 
Prerequisites:
AWS account with access to MSK, Kinesis, S3, Databricks, and MWAA services.
Databricks Workspace setup with Spark runtime.
Steps to Install and Run:
Clone the Repository:

bash
Copy code
git clone https://github.com/Umar-hamid-786/pinterest-data-pipeline549.git
cd pinterest_project

Set Up AWS Resources:

Deploy the API Gateway, MSK, and Kinesis services using the provided CloudFormation template.

Set up S3 buckets for the data lake.

Configure MSK Connect:

Use the plugin-connector pair to stream data from MSK topics to the S3 data lake.

Set Up Databricks:

Import the provided Spark transformation scripts into Databricks and configure them to read from S3.

Run the Airflow DAGs:

Upload the DAG scripts to MWAA to automate Databricks workloads.

Testing:

Test the API Gateway for batch data ingestion and verify real-time stream processing through Kinesis.

## Future Enhancements 
Improve Scalability: Integrate an auto-scaling mechanism for Databricks clusters and MSK nodes to handle higher volumes of data.
Enhanced Monitoring: Set up CloudWatch alarms and dashboards to better monitor the real-time performance of data streams.
Machine Learning Integration: Introduce a machine learning model on top of the data pipeline to provide predictions and recommendations.
Data Visualization: Add a dashboard to visualize real-time data analytics and trends.

## License Information 
This project is licensed under the MIT License. Feel free to use, modify, and distribute this project as needed. For more details, refer to the LICENSE file in the repository.