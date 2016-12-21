#!/usr/bin/env python
""" Fixtures for running pytest """

import pytest
from pymongo import MongoClient
from sramongo.mongo import start_mongo


def test_start_mongo(mongo_folders):
    """ Test starting the database server. """
    mongoDB = start_mongo(dbDir=mongo_folders[0], logDir=mongo_folders[1])
    assert isinstance(mongoDB.pid, int)
    mongoDB.kill()


def test_mongo_connect(mongoDB):
    """ Test basic functionality of mongo and pymongo. """
    client = MongoClient()
    assert sorted(client.database_names()) == sorted(['admin', 'local'])

    db = client.test_database
    collection = db.test_collection
    collection.insert_one({'name': 'test'})

    assert sorted(client.database_names()) == sorted(['admin', 'local', 'test_database'])
    assert db.collection_names() == ['test_collection']
    assert collection.find_one({}, {'name': 1, '_id': 0}) == {'name': 'test'}

    client.close()