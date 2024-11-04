# Nyc-Taxi-January
# PySpark AWS Docker Project

This project is an industrial-level data engineering project designed to process NYC Taxi data using PySpark and AWS S3. The entire setup runs within Docker containers, making it easy to manage dependencies and streamline deployment.

## Project Overview

The project is designed to:
- Ingest raw NYC taxi trip data stored in AWS S3
- Process and clean the data using PySpark
- Store the processed data back into a different location in AWS S3
- Facilitate data analytics and visualization

## Directory Structure

The project has the following main files:
- `Dockerfile`: Configures the Docker environment for PySpark.
- `docker-compose.yml`: Sets up services for Spark Master, Spark Worker, and PySpark application containers.
- `app.py`: Main application script for data processing using PySpark.

## Setup

### Prerequisites
1. **AWS Account** with full access to S3.
2. **Docker** installed on your machine.
3. **Git** for version control.

### Project Installation

1. Clone this repository to your local machine:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2. Ensure you have the following environment variables set in a `.env` file:
    ```
    AWS_ACCESS_KEY_ID=<Your AWS Access Key>
    AWS_SECRET_ACCESS_KEY=<Your AWS Secret Key>
    AWS_REGION=<Your AWS Region>
    ```

3. **Build and Run the Docker Containers**:
    ```bash
    docker-compose up --build
    ```

4. **Execute the Application**:
    Once the containers are up and running, execute the following command in a separate terminal:
    ```bash
    docker exec -it pyspark-aws-docker-pyspark-app python /app/app.py
    ```

## Project Details

### Data Flow

1. **Raw Data**: NYC Taxi data in Parquet format stored in S3 at `s3://<your-bucket>/raw/Jan_2023` and `s3://<your-bucket>/raw/Jan_2024`.
2. **Data Processing**: PySpark processes the data by:
   - Calculating trip duration.
   - Adding pickup day and hour.
   - Calculating average fare amount based on pickup day and hour.
3. **Processed Data**: Output stored in S3 at `s3://<your-bucket>/processed/`.

### Accessing Processed Data

You can use AWS services like **Athena** to query the processed data directly from S3 or integrate with **Tableau** for data visualization.

## Future Enhancements

1. **Tableau Integration**: Connect directly to S3 for visualization.
2. **AWS Glue or Athena**: Use AWS Glue for ETL processes or Athena for querying the data.

## Repository Details

- **.gitignore** includes `.env` and other sensitive files to ensure they are not pushed to the repository.
- **README.md** provides comprehensive setup instructions and project details.

## License

This project is licensed under the MIT License.
