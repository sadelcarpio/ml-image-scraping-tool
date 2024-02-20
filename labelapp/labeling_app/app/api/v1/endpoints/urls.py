from fastapi import APIRouter, status, HTTPException, Body, Depends
from sqlmodel import select

from app.api.deps import SessionDep, validate_labels
from app.core.uploader import ObjectStorageUploader
from app.models.extras import UserProjectModel
from app.models.urls import UrlModel
from app.schemas.urls import UrlRead
from app.security.auth import CurrentUser

router = APIRouter(tags=["URLs Endpoints"])


@router.get("/{project_id}/current-url", status_code=status.HTTP_200_OK, response_model=UrlRead)
def get_current_url(project_id: int, session: SessionDep, current_user: CurrentUser) -> UrlModel:
    current_url = session.exec(
        select(UrlModel).where(UrlModel.project_id == project_id,
                               UrlModel.user_id == current_user.id,
                               UrlModel.labeled == False)).first()
    if current_url is None:
        raise HTTPException(status_code=404, detail="Didn't find any unlabeled urls.")
    user_assignment = session.exec(
        select(UserProjectModel).where(UserProjectModel.project_id == project_id,
                                       UserProjectModel.user_id == current_user.id)
    ).first()
    user_assignment.current_url = current_url.id
    session.add(user_assignment)
    session.commit()
    return current_url


@router.put("/{project_id}/submit-url",
            status_code=status.HTTP_204_NO_CONTENT,
            dependencies=[Depends(validate_labels)])
async def submit_url(project_id: int,
                     session: SessionDep,
                     current_user: CurrentUser,
                     uploader: ObjectStorageUploader,
                     labels: dict = Body(...)):
    url_to_submit = session.exec(
        select(UrlModel).join(UserProjectModel, UserProjectModel.current_url == UrlModel.id).where(
            UserProjectModel.project_id == project_id,
            UserProjectModel.user_id == current_user.id)).first()
    if url_to_submit is None:
        raise HTTPException(status_code=404, detail="Error in selecting URL to submit. Be sure to have called"
                                                    " /current-url endpoint first")
    uploader.upload_label(url_to_submit, labels)
    url_to_submit.labeled = True
    session.add(url_to_submit)
    session.commit()
    session.refresh(url_to_submit)
