#!/usr/bin/env python3
"""
Module that returns the list of schools having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic.
    
    Args:
        mongo_collection: pymongo collection object.
        topic(string): The topic searched.

    Returns:
        A list of schools that have the specified topic in their topics list.
    """
    return list(mongo_collection.find({"topics": topic}))
