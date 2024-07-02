from fastapi import status
from pymongo import MongoClient, errors
from typing import List, Dict
from bson import ObjectId

from src.shared.config.Environment import get_environment_variables
from src.shared.models.database.idatabase import IDatabase
from src.shared.models.response.response import getJsonResponse

# Runtime Environment Configuration
env = get_environment_variables()

class MongoDB(IDatabase):
    @staticmethod
    def get_connection():
        client = MongoClient("mongodb+srv://MShaquille:130277633sS.@vainillacluster.6znleyj.mongodb.net/?retryWrites=true&w=majority&appName=VainillaCluster")
        try:
            yield client
        finally:
            client.close()

    @staticmethod
    def select(conn: MongoClient, collection_name: str, query: Dict = None, sort: list[dict[str, int]] = None) -> List[Dict] | Exception:
        print("---------- Select ----------")
        print(f"query: {query}")
        returnValue: List[Dict] = []
        try:
            collection = conn[env.DATABASE_NAME.get("MongoDB")][collection_name]
            if (query is not None):
                result = collection.find(query).sort(sort) if sort is not None else collection.find(query)
            else:
                result = collection.find().sort(sort) if sort is not None else collection.find()
            returnValue = list(result)
        except errors.PyMongoError as e:
            print("Exception")
            print(e)
            print("--------------------------------------------")
            returnValue = getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=str(e), data={})
        finally:
            return returnValue

    @staticmethod
    def insert(conn: MongoClient, collection_name: str, document: Dict) -> ObjectId | Exception:
        print("---------- Insert ----------")
        print(f"document: {document}")
        try:
            collection = conn[env.DATABASE_NAME.get("MongoDB")][collection_name]
            result = collection.insert_one(document)
            returnValue = result.inserted_id
        except errors.PyMongoError as e:
            print("Exception")
            print(e)
            print("--------------------------------------------")
            returnValue = getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=str(e), data={})
        finally:
            return returnValue

    @staticmethod
    def update(conn: MongoClient, collection_name: str, query: Dict, update_values: Dict) -> bool | Exception:
        print("---------- Update ----------")
        print(f"query: {query}")
        print(f"update_values: {update_values}")
        try:
            collection = conn[env.DATABASE_NAME.get("MongoDB")][collection_name]
            result = collection.update_many(query, {'$set': update_values})
            returnValue = result.acknowledged
        except errors.PyMongoError as e:
            print("Exception")
            print(e)
            print("--------------------------------------------")
            returnValue = getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=str(e), data={})
        finally:
            return returnValue

    @staticmethod
    def delete(conn: MongoClient, collection_name: str, query: Dict) -> bool | Exception:
        print("---------- Delete ----------")
        print(f"query: {query}")
        try:
            collection = conn[env.DATABASE_NAME.get("MongoDB")][collection_name]
            result = collection.delete_many(query)
            returnValue = result.deleted_count > 0
        except errors.PyMongoError as e:
            print("Exception")
            print(e)
            print("--------------------------------------------")
            returnValue = getJsonResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False, message=str(e), data={})
        finally:
            return returnValue
