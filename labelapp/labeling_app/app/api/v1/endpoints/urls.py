from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from app.api.deps import SessionDep, CurrentUser
from app.models import UrlModel, UserProjectModel
from app.schemas.urls import UrlResponse, UrlUpdated

router = APIRouter()


@router.get("/{project_id}/current-url", status_code=status.HTTP_200_OK, response_model=UrlResponse)
def get_current_url(project_id: int, session: SessionDep, current_user: CurrentUser):
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


# TODO: include multipart containing the annotation, may need a different endpoint submit-x for different annotation
#  types
@router.put("/{project_id}/submit-url", status_code=status.HTTP_201_CREATED, response_model=UrlUpdated)
def submit_url(project_id: int, session: SessionDep, current_user: CurrentUser):
    url_to_submit = session.exec(
        select(UrlModel).join(UserProjectModel, UserProjectModel.current_url == UrlModel.id).where(
            UserProjectModel.project_id == project_id,
            UserProjectModel.user_id == current_user.id)).first()
    if url_to_submit is None:
        raise HTTPException(status_code=404, detail="Error in selecting URL to sumbit. Be sure to have called"
                                                    " /current-url endpoint first")
    url_to_submit.labeled = True
    session.add(url_to_submit)
    session.commit()
    session.refresh(url_to_submit)
    return url_to_submit
