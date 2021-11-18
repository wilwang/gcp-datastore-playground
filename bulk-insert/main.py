from google.cloud import datastore
import uuid
import time

def delete_all(kind_name):
    datastore_client = datastore.Client()
    query = datastore_client.query(kind=kind_name)
    all_keys = query.fetch()

    batch_size = 10
    batch = []
    deleted = 0

    for key in all_keys:
        batch.append(key)
        deleted = deleted + 1
        if (len(batch) == batch_size):
            datastore_client.delete_multi(batch)
            
            batch.clear()
    
    if len(batch) > 0:
        datastore_client.put_multi(batch)
        print (batch)

    print(f"Deleted {deleted} records from {kind_name}")

def main():
    datastore_client = datastore.Client()

    total_items = 100
    batch_size = 10
    kind = "TestObject"
    batch = []

    for x in range(total_items):    
        name = "name+" + str(uuid.uuid4())
        item = datastore.Entity(datastore_client.key(kind, name))
        item["name"] = name
        item["timestamp"] = time.time()
        item["data"] = str(uuid.uuid4())
        batch.append(item)
        if (len(batch) == batch_size):
            datastore_client.put_multi(batch)
            batch.clear()

    if len(batch) > 0:
        datastore_client.put_multi(batch)
        batch.clear()

    print(f"Inserted {total_items} entities into {kind}")

delete_all("TestObject")
#main()