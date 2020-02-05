"""
Test ORM backend for cifra.
"""
import os
import tempfile

import cifra.attack.database as database


def test_create_database():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_database = os.path.join(temp_dir, database.DATABASE_FILENAME)
        assert not os.path.exists(test_database)
        database.create_database(temp_dir)
        assert os.path.exists(test_database)


# def test_open_database_session():
#     with tempfile.TemporaryDirectory() as temp_dir:
#         test_database = os.path.join(temp_dir, database.DATABASE_PATH)
#         engine = database.create_database(test_database)
#         with database.open_database_session(engine) as session:
#             assert session.is_active