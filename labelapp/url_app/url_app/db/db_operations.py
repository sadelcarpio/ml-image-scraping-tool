import logging

from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

from url_app.db import models
from url_app.url_dist import ConsistentHashing

logger = logging.getLogger(__name__)


class SQLSession:
    def __init__(self, session: sessionmaker):
        self.session = session
        self.n_users = None

    def upload_url(self, gcs_url: str, hashed_url: str, project_name: str, dist_strategy: ConsistentHashing):
        db = self.session()
        try:
            user_ids = db.query(models.UserModel.id).join(models.UserModel.projects).filter_by(name=project_name).all()
            if self.n_users is None:
                self.n_users = len(user_ids)
            if len(user_ids) < self.n_users:
                logger.info("A user was deleted, reassigning orphan URLs ...")
                # Could add a custom exception here to move this logic to consumer level
                self.reassign_unlabeled_urls(user_ids, dist_strategy)
                logger.info("Orphan URLs reassigned.")
                self.n_users = len(user_ids)
            user_id = dist_strategy.distribute_url(hashed_url, user_ids)
            project_id = db.query(models.ProjectModel).filter_by(name=project_name).first().id
            db_url = models.UrlModel(gcs_url=gcs_url,
                                     hashed_url=hashed_url,
                                     labeled=False,
                                     project_id=project_id,
                                     user_id=user_id)
            db.add(db_url)
            db.commit()
            db.refresh(db_url)
        except exc.IntegrityError:
            logger.error(f"The GCS URL: {gcs_url} already exists in the database.")
            db.rollback()
        except exc.SQLAlchemyError as e:
            logger.error(f"Failed to upload: {e}")
            db.rollback()
            raise
        finally:
            db.close()

    def reassign_unlabeled_urls(self, user_ids: list, dist_strategy: ConsistentHashing):
        db = self.session()
        try:
            unlabeled_urls = db.query(models.UrlModel).filter_by(labeled=False, user_id=None)
            for db_url in unlabeled_urls:
                user_id = dist_strategy.distribute_url(db_url.hashed_url, user_ids)
                if user_id is None:
                    return
                db_url.user_id = user_id
                db.commit()
                db.refresh(db_url)
        except exc.SQLAlchemyError as e:
            logger.error(f"Failed to update: {e}")
            db.rollback()
            raise
        finally:
            db.close()
