from flask import Flask, jsonify, request
from flask.views import MethodView

from auth import hash_password
from crud import create_items, delete_item, get_items
from models import Ads, User, get_session_maker
from schema import CreateAds, CreateUser, UpdateAds, validate

app = Flask("app")

Session = get_session_maker()


class AdsViews(MethodView):
    def get(self, ads_id):
        with Session() as session:
            ads = get_items(session, Ads, ads_id)
            return jsonify({"id": ads.id, "title": ads.title, "autor": ads.autor})

    def post(self):
        new_post = validate(CreateAds, request.json)
        with Session() as session:
            post = create_items(session, Ads, **new_post)
            return jsonify({"id": post.id})
        
    def patch(self, ads_id: int):
        up_post = validate(UpdateAds, request.json)
        with Session() as session:
            ads = get_items(session, Ads, ads_id)
            for fields, value in up_post.items():
                setattr(up_post, fields, value)
            session.add(ads)
            session.commit()
            return jsonify({"status": 'success'})

    def delete(self, ads_id: int):
        with Session() as session:
            user = delete_item(session, Ads, ads_id)
            return jsonify({"status": user.status})


class UserViews(MethodView):
    def get(self, user_id):
        with Session() as session:
            user = get_items(session, User, user_id)
            return jsonify({"id": user.id, "name": user.name, "email": user.email})

    def post(self):
        new_user = validate(CreateUser, request.json)
        new_user["password"] = hash_password(new_user["password"])
        with Session() as session:
            user = create_items(session, User, **new_user)
            return jsonify({"id": user.id})

    def delete(self, user_id):
        with Session() as session:
            user = delete_item(session, User, user_id)
            return jsonify({"status": user.status})


