import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def getdf():
    uri = "mongodb+srv://fv121:Vasureddy2303@hw2cluster.zpracso.mongodb.net/?retryWrites=true&w=majority&appName=HW2Cluster"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    db = client["premier-league-db"]  # database name
    collection = db["pl-data"]  # table name

    cursor = collection.find({})
    df = pd.DataFrame(list(cursor))
    df = df.drop(columns=['_id'])

    # filter for inconsistent records
    df = df[df['Home_Team'] != '0']
    # print(df.shape)
    return df


def test_record_count():
    df = getdf()
    print('Checking if records exist')
    row_count = df.shape[0]
    print("Number of Records: ", row_count)
    assert row_count != 0, 'No Data in the file'
    # return row_count


def test_null_records():
    df = getdf()
    print('Checking for Null Records')
    # null_count = df[df.isnull()].shape[0]
    null_count = df[df.isnull().all(axis=1)].shape[0]
    print('Number of Null Records: ', null_count)
    assert null_count == 0, 'Null records in the data'
    # return null_count


def test_duplicate_check():
    df = getdf()
    print('Checking for Duplicate Recods')
    duplicates_count = df.duplicated().sum()
    print(
        f"Number of duplicated rows in the entire DataFrame: {duplicates_count}")
    assert duplicates_count == 0, 'Duplicates in the Data'
    # return duplicates_count


def test_nan_records():
    df = getdf()
    print('Checking for NaN Records')
    nan_rows_count = df.isna().any(axis=1).sum()
    print(f"Number of rows with at least one NaN value: {nan_rows_count}")
    assert nan_rows_count == 0, 'NaN Values in the Data'
    # return nan_rows_count


def test_inconsistent_records():
    df = getdf()
    print('Checking for Inconsistent Records')
    inconsistent_records = df[df['Home_Team'] == '0'].shape[0]
    print('Number of Inconsistent records: ', inconsistent_records)
    assert inconsistent_records == 0, 'Inconsistent Records in the Data'
    # return inconsistent_records
