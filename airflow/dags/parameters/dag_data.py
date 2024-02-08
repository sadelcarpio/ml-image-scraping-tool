from typing import List

import requests
from pydantic import BaseModel, TypeAdapter


class DagMetaData(BaseModel):
    project: str
    keywords: str
    notify: str


response = requests.get('http://dag-info:3000')
ta = TypeAdapter(List[DagMetaData])
dags_metadata = ta.validate_python(response.json())
