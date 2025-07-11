from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class BaseImporter(ABC):
    """
    A base class for data importers.
    Provides a common structure for importing data into the database.
    """
    def __init__(self, db_session: Session, file_path: str):
        """
        Initializes the importer.

        :param db_session: The SQLAlchemy database session.
        :param file_path: Path to the data file to be imported.
        """
        self.db_session = db_session
        self.file_path = file_path

    @abstractmethod
    def import_data(self):
        """
        Abstract method to perform the data import.
        Subclasses must implement this to read the file, transform data,
        and save it to the database.
        """
        pass

    def _file_exists(self) -> bool:
        """Helper method to check if the source file exists."""
        import os
        return os.path.exists(self.file_path)

    def log_message(self, message: str, level: str = "INFO"):
        """Simple logging method."""
        import datetime
        print(f"{datetime.datetime.now().isoformat()} [{level}] [Importer: {self.__class__.__name__}] {message}")
