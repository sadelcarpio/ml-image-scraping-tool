from pydantic import BaseModel


class DagMetaData(BaseModel):
    project: str
    keywords: str
    last_processed: str
    notify: str
