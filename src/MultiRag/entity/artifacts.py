from dataclasses import dataclass
from typing import Any
from src.MultiRag.constants import RETREIVER_DEFAULT_K
@dataclass
class IngestionArtifact:
    vector_db:Any
