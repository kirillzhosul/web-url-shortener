"""
    CRUD for Referer database model.
"""


from flask_sqlalchemy import SQLAlchemy

from app.database.models.referer import Referer


def get_or_create(db: SQLAlchemy, referer: str) -> Referer:
    """
    Return Referer object if there is one in DB, else create it.
    :param SQLAlchemy db: database object
    :param str referer: referer from `Referer` header
    :return: Referer object
    :rtype: Referer
    """
    referer_object = Referer.query.filter_by(referer_value=referer).first()
    if referer_object is None:
        referer_object = Referer(referer_value=referer)
        db.session.add(referer_object)
        db.session.commit()
        db.session.refresh(referer_object)

    return referer_object
