from pydantic import BaseModel


class DagMetaData(BaseModel):
    project: str
    keywords: str
    notify: str
