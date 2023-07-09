from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from error import HttpError
from models import ORM_MODEL_CLS, get_session_maker

Session = get_session_maker()


def get_items(session: Session, model_cls: ORM_MODEL_CLS, item_id: int | str):
    item = session.query(model_cls).get(item_id)
    if item is None:
        raise HttpError(404, f"{model_cls.__name__.lower()} not found")
    return item


def create_items(session: Session, model_cls: ORM_MODEL_CLS, **params):
    new_item = model_cls(**params)
    session.add(new_item)
    try:
        session.commit()
    except IntegrityError as er:
        raise HttpError(409, f"{model_cls.__name__.lower()} уже есть")
    return new_item


def delete_item(session: Session, model_cls: ORM_MODEL_CLS, item_id: int | str):
    item = get_items(session, model_cls, item_id)
    session.delete(item)
    session.commit()
    return jsonify({"status": "deleted"})
