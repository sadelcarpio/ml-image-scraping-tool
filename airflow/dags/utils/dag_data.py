from typing import List

import requests
from pydantic import TypeAdapter

from utils.schemas import DagMetaData


def get_dag_metadata():
    response = requests.get('http://dag-info:3000')
    ta = TypeAdapter(List[DagMetaData])
    dags_metadata = ta.validate_python(response.json())
    return dags_metadata
