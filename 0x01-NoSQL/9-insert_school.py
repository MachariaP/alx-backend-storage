#!/usr/bin/env python3
"""
Module that inserts a new Doc in a collection based on kwargs.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs.

    Args:
        mongo_collection: pymongo collection object.
        **kwargs: Arbitrary keyword arguments that defines the document to be inserted.

        Returns:
            The new_id of the inserted document.
    """
    new_doc = mongo_collection.insert_one(kwargs)
    return new_doc.inserted_id
