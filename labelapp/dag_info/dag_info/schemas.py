from pydantic import BaseModel


class DagInfo(BaseModel):
    project: str
    keywords: str
    notify: str
