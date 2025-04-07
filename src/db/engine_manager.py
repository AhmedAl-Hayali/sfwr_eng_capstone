from typing import Optional
from sqlalchemy import URL, Engine
from sqlalchemy import create_engine

class EngineManager:
    username: str = None
    password: str = None
    host: str = None
    database: str = None
    port: int = None
    dialect: str = None
    driver: str = None

    def __init__(
            self,
            username: str,
            password: str,
            host: str,
            database: str,
            port: Optional[int] = 5432,
            dialect: Optional[str] = 'postgresql',
            driver: Optional[str] = 'psycopg'
    ) -> None:
        """Initialize connection parameters.
        
        #TODO: Docstring :)
        """
        self.username = username
        self.password = password
        self.host = host
        self.database = database
        self.port = int(port)
        self.dialect = dialect
        self.driver = driver
        
        self._url = None
        self._engine = None

    def _create_url(self) -> URL:
        """Initialize connection URL.
        
        #TODO: Docstring :)
        """
        return URL.create(
            drivername=f'{self.dialect}+{self.driver}',
            username=self.username,
            password = self.password,
            host = self.host,
            database = self.database,
            port = self.port
        )

    def _create_engine(self) -> Engine:
        """Initialize engine.
        
        #TODO: Docstring :)
        """
        if self._url is None:
            self._url = self._create_url()

        return create_engine(self._url)
    
    def engine(self):
        """Engine singleton.
        
        #TODO: Docstring :)
        """
        if self._engine is None:
            self._engine = self._create_engine()
        return self._engine
