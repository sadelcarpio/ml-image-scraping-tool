from pydantic import BaseModel


class DagInfo(BaseModel):
    project: str
    last_processed: str
    keywords: str
    notify: str
