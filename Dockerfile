FROM bitnami/spark:3.3.2

# Set the working directory inside the container
WORKDIR /app

# Copy the local app files to the container's working directory
COPY . /app

USER root
# Fix the missing directory issue and install dependencies
RUN mkdir -p /var/lib/apt/lists/partial && \
    apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install py4j pyspark
