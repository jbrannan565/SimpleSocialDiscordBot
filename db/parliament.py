from db.mongo import db

class ParliamentDB:
    def __init__(self):
        self.collection = db.motions

    def read_pending(self):
        return self.collection.find({"status": "pending"})

    def read_tabled(self):
        return self.collection.find({"status": "tabled"})

    def read_laws(self):
        return self.collection.find({"status": "law"})

    def read_closed(self):
        return self.collection.find({"status": "closed"})

    def read_by_name(self, name):
        return self.collection.find({"name": name})

    def create(self, name, description):
        data = {
            'name': name,
            'description': description,
            'status': 'pending',
            'amendments': []
        }
        return self.collection.insert_one(data)

    def table(self, motion_name):
        return self.collection.find_one_and_update(
            {
                "name": motion_name
            }, 
            { 
                "$set": {"status": "tabled"} 
            })

    def untable(self, motion_name):
        return self.collection.find_one_and_update(
            {
                "name": motion_name
            }, 
            { 
                "$set": {"status": "pending"} 
            })

    def amend(self, motion_name, amendment):
        return self.collection.find_one_and_update(
            {
                "name": motion_name
            },
            {
                "$addToSet": { "amendments": amendment }
            }
        )

    def legislate(self, motion_name):
        return self.collection.find_one_and_update(
            {
                "name": motion_name
            }, 
            { 
                "$set": {"status": "law"} 
            })
    
    def close(self, motion_name):
        return self.collection.find_one_and_update(
            {
                "name": motion_name
            }, 
            { 
                "$set": {"status": "closed"} 
            })