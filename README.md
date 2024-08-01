# airflow-news-data-categorizer
## Overview
The airflow-news-data-categorizer is a demonstration project that uses Apache Airflow to categorize news data fetched from a public API. The project includes a Docker Compose file to set up the necessary Airflow-related containers.

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/hpahasini/airflow-news-data-categorizer.git
    cd airflow-news-data-categorizer
    ```

2. **Build and start the Airflow services:**
    ```sh
    docker-compose up -d
    ```

3. **Access the Airflow web interface:**
    - Open your web browser and go to `http://localhost:8080`.
    - Use the default credentials:
        - Username: `airflow`
        - Password: `airflow`

### Configuration

1. **Create Airflow connections:**
    - Go to the Airflow web interface.
    - Navigate to `Admin -> Connections`.
    - Add a new HTTP connection:
        - Connection ID: `http_connection`
        - Connection Type: `HTTP`
        - Host: `newsapi.org`
    - Add a new AWS connection:
        - Connection ID: `aws_connection`
        - Connection Type: `Amazon Web Services`
        - Set up the necessary credentials.

### DAG Details

The DAG `news_data_categorizer` performs the following tasks:

1. **Fetch news data from a public API:**
    - Uses `SimpleHttpOperator` to fetch top headlines from `newsapi.org`.

2. **Transform the news data:**
    - Uses `PythonOperator` to categorize the news articles based on their titles and save the transformed data as a CSV file.

3. **Upload the CSV file to an S3 bucket:**
    - Uses `PythonOperator` to upload the transformed CSV file to an S3 bucket.

