from . import db,GridFSBucket

def get_bucket():
    if db is None:
        raise ConnectionError("Could not connect to the database.")
    return GridFSBucket(db, bucket_name='gameFiles')