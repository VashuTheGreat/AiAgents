from pydantic import BaseModel
from typing import Optional, List

class WorkerTask(BaseModel):
    worker_name: str
    instruction: str
    file_path: str
    file_type: str

class OrchestratorOutput(BaseModel):
    use_worker: bool
    tasks: Optional[List[WorkerTask]] = None
    reason: str
    confidence: float