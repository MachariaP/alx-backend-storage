#!/usr/bin/env python3
import os
import logging
from pymongo import MongoClient

"""
A script that provides some stats about
Nginx logs stored in MongoDB.
"""

# Setup basic logging
logging.basicConfig(level=logging.INFO)


def log_stats():
    """
    Connects to the MOngoDB database 'logs', queries the 'nginx' collection,
    and prints statistics about the logs. It displays the total number of logs,
    counts of different HTTPmethods, and the number of logs with method GET
    and path /status.
    """
    try:
        # MongoDB connection string from environment variable or default
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db = client['logs']
        nginx_collection = db['nginx']

        # Total number of logs
        total_logs = nginx_collection.count_documents({})
        logging.info(f"{total_logs} logs")

        # Http methods statistics
        methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        logging.info("Methods:")

        for method in methods:
            count = nginx_collection.count_documents({"method": method})
            logging.info(f"  method {method}: {count}")

        # Number of documents with method=GET and path=/status
        status_checks = nginx_collection.count_documents(
                {"method": "GET", "path": "/status"})
        logging.info(f"{status_checks} status check")

    except Exception as e:
        logging.error(f"An error occured: {e}")


if __name__ == "__main__":
    log_stats()
