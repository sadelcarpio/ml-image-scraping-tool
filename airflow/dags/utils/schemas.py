from pydantic import BaseModel


class DagMetaData(BaseModel):
    project: str
    keywords: str
    last_labeled: str
    notify: str
