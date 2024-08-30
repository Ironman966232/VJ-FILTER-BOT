
from iron import config_dict, bot_id, DATABASE_URI
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from bot import logger


class DbManager:
    def __init__(self):
        self.__err = False
        self.__db = None
        self.__conn = None
        self.__connect()

    def __connect(self):
        try:
            self.__conn = AsyncIOMotorClient(DATABASE_URI)
            self.__db = self.__conn.luna
        except PyMongoError as e:
            logger.error(f"Error in DB connection: {e}")
            self.__err = True

    def db_load(self):
        if self.__err:
            return
        self.__db.settings.config.update_one(
            {"_id": bot_id}, {"$set": config_dict}, upsert=True
        )
        self.__conn.close

    def update_config(self, dict_):
        if self.__err:
            return
        self.__db.settings.config.update_one(
            {"_id": bot_id}, {"$set": dict_}, upsert=True
        )
        self.__conn.close

if DATABASE_URI:
        DbManager().db_load()
        
    