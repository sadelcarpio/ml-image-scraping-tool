from typing import Annotated

from fastapi import Depends

from app.models.urls import UrlModel


class ObjectStorage:
    def upload_label(self, url: UrlModel, labels: dict):
        pass


def get_object_storage():
    return ObjectStorage()


ObjectStorageUploader = Annotated[ObjectStorage, Depends(get_object_storage)]
