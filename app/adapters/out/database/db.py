from contextlib import asynccontextmanager

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.adapters.out.database.entities.user import User
from app.config.config import app_config


class OutDatabase:
    _instance = None  # Singleton instance
    _initialized = False  # Track if Beanie is initialized

    def __init__(self, db_name: str, db_uri: str):
        """ Private constructor: Prevent direct instantiation """
        if hasattr(self, "_db"):  # Prevent reinitialization
            return

        self.db_name = db_name
        self.db_uri = db_uri
        self.client = AsyncIOMotorClient(self.db_uri)
        self.db = self.client[self.db_name]

    @classmethod
    async def get_instance(cls):
        """ Ensure the singleton instance is created asynchronously. """
        if cls._instance is None:
            cls._instance = cls(app_config.DATABASE_NAME, app_config.MONGO_URI)
            await cls._instance._initialize_beanie()  # Async initialization

        return cls._instance

    async def _initialize_beanie(self):
        """ Private method to initialize Beanie if not already initialized """
        if not self._initialized:
            await init_beanie(
                database=self.db,
                document_models=[User]
            )
            self._initialized = True

    @classmethod
    @asynccontextmanager
    async def initialize(cls):
        """ Context manager to get the database instance asynchronously """
        instance = await cls.get_instance()
        yield instance

async def get_db():
    """ Dependency injection to provide a singleton database instance. """
    db = await OutDatabase.get_instance()
    return db.db  # Returning the actual database instance