# #from pymongo import MongoClient

# #mongo_client = MongoClient("mongo")
# db = mongo_client["cse312-because-the-internet"]

# users_id_collection = db["users_id"]
# users_account = db["user_accounts"]

# def get_next_id():
#     id_object = users_id_collection.find_one({})
#     if id_object:
#         next_id = int(id_object['last_id']) + 1
#         users_id_collection.update_one({}, {'$set': {'last_id': next_id}})
#         return next_id
#     else:
#         users_id_collection.insert_one({'last_id': 1})
#         return 1
    
    
# def create_record(dictionary):
#     id = get_next_id()
#     #create a record of a user's username and password
#     #handle duplicate usernames
#         #check if ursenamgit add
#     users_account.insert_one({"id": int(id), "username": dictionary.get("username"), "password": dictionary.get("password")})
#     dic = {"id": int(id), "username": dictionary.get("username"), "password": dictionary.get("password")}
#     return dic

# #how do we handle  duplicate usernames?
# def update_username(id, dictionary):
#     #update username
#     users_account.update_one({"id":int(id)},{"$set":{"username":dictionary.get("username")}})
#     dic = {{"username":dictionary.get("username")}}
#     return dic


