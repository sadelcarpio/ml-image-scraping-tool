from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select

from app.api.deps import get_db, SessionDep, CurrentUser
from app.models import UrlModel, UserProjectModel, ProjectModel

router = APIRouter()


# For urls, we need 3 routes at the moment:
# 1. For getting the current url, for the current user (will need Dep get_current_user) and current_project (project_id)
# 2. For going to the nex url, updating current_url (could be merged into #1)
# 3. For submitting a URL (marking labeled=True)
@router.get("/{project_id}/current-url", status_code=status.HTTP_200_OK, response_model=UrlModel)
def get_current_url(project_id: int, session: SessionDep, current_user: CurrentUser):
    stmt = select(UserProjectModel.current_url).where(UserProjectModel.project_id == project_id,
                                                      UserProjectModel.user_id == current_user.id)
    url_idx = session.exec(stmt).first()
    current_url = session.exec(
        select(UrlModel).join(ProjectModel).limit(1).offset(url_idx)).first()
    return current_url


@router.put("/{project_id}/next-url", status_code=status.HTTP_201_CREATED)
def update_next_url(project_id: int, session: Session = Depends(get_db)):
    user_assignment = session.exec(
        select(UserProjectModel).where(UserProjectModel.project_id == project_id)).first()
    user_assignment.current_url += 1
    session.add(user_assignment)
    session.commit()
    # Here we could just call the get_current_url part in order to return that


# Would need to upload a json or a file with the annotation
@router.put("/{url_id}/{project_id}/submit", status_code=status.HTTP_201_CREATED)
def submit_url(url_id: int, project_id: int, session: Session = Depends(get_db)):
    url_to_submit = session.exec(
        select(UrlModel).where(UrlModel.project_id == project_id, UrlModel.id == url_id)).first()
    url_to_submit.labeled = True
    session.add(url_to_submit)
    session.commit()
    # Here return the 201 or whatever
