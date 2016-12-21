#!/usr/bin/env python
""" Fixtures for running pytest. """

import pytest

from sramongo.mongo import start_mongo


@pytest.fixture(scope="session")
def mongo_folders(tmpdir_factory):
    """ Create TMPDIR for database and logs. """
    data = tmpdir_factory.mktemp('db')
    log = tmpdir_factory.mktemp('log')
    return str(data), str(log)


@pytest.fixture(scope="session")
def mongoDB(mongo_folders):
    """ Start the database server.

    Server will be killed after the fixture is no longer neaded.
    """
    mongoDB = start_mongo(dbDir=mongo_folders[0], logDir=mongo_folders[1])
    yield mongoDB
    print('Shutting down mongoDB.')
    mongoDB.kill()
