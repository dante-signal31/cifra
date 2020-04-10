"""
Test ORM backend for cifra.
"""
import os
import tempfile
import pytest

import cifra.attack.database as database


@pytest.mark.quick_test
def test_create_database():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_database = os.path.join(temp_dir, database.DATABASE_FILENAME)
        assert not os.path.exists(test_database)
        database.create_database(temp_dir)
        assert os.path.exists(test_database)
