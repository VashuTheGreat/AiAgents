from dataclasses import dataclass

@dataclass
class IngestionConfig:
    db_path:str
    docs_path:str