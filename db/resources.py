from db.mongo import db

def read_resources(resource_type):
    '''
    returns a cursor of the queried resource
    '''
    return db[resource_type].find()

def read_resources_where(resource_type, query):
    '''
    returns a cursor of the queried resource
    '''
    return db[resource_type].find(query)


def create_resource(resource_type, data):
    '''
    add data dict to resource_type collection
    '''
    data['last_update'] = datetime.utcnow()
    resource_collection = db[resource_type]
    return resource_collection.insert_one(data)

def update_resource(resource_type, query, data):
    '''
    updates a document in resource type collection found by query and data is update
    returns the updated document as a dict
    '''
    data['last_update'] = datetime.utcnow()
    resource_collection = db[resource_type]
    return resource_collection.find_one_and_update(query, { "$set": data })

def delete_resource(resource_type, query):
    '''
    deletes resource found by query
    '''
    resource_collection = db[resource_type]
    return resource_collection.delete_one(query).deleted_count