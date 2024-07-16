#!/usr/bin/env python3
from pymongo import MongoClient


def log_stats():
    """
    Connects to the MOngoDB database 'logs', queries the 'nginx' collection,
    and prints statistics about the logs. It displays the total number of logs,
    counts of different HTTPmethods, and the number of logs with method GET
    and path /status.
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client.logs
    nginx_collection = db.nginx

    # Total number of logs
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    # Http methods statistics
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")

    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f" method {method}: {count}")

    # Number of documents with method=GET and path=/status
    status_checks = nginx_collection.count_documents(
            {"method": "GET", "path": "/status"})
    print(f"{status_checks} status check")


if __name__ == "__main__":
    log_stats()
