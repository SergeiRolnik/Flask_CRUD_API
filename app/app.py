from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask.views import MethodView
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'SOME KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    date_created = db.Column(db.Date)
    user_id = db.Column(db.Integer)


class AdView(MethodView):

    def get(self, ad_id):
        ad = Ad.query.filter_by(id=ad_id).first()
        if ad:
            return jsonify({
                'title': ad.title,
                'description': ad.description,
                'date_created': ad.date_created,
                'user_id': ad.user_id
            }), 200
        else:
            return jsonify({'message': 'ad does not exist'}), 404

    def post(self):
        data = request.json
        new_ad = Ad(
            title=data['title'],
            description=data['description'],
            date_created=datetime.today(),
            user_id=data['user_id']
        )
        db.session.add(new_ad)
        db.session.commit()
        return jsonify({'message': 'ad added', 'title': new_ad.title}), 201

    def delete(self, ad_id):
        ad = Ad.query.filter_by(id=ad_id).first()
        if ad:
            db.session.delete(ad)
            db.session.commit()
            return jsonify({'message': 'ad deleted'}), 200
        else:
            return jsonify({'message': 'ad does not exist'}), 404

    def patch(self, ad_id):
        data = request.json
        ad = Ad.query.filter_by(id=ad_id).first()
        if ad:
            for key, value in data.items():
                setattr(ad, key, value)
            db.session.commit()
            return jsonify({'message': 'ad updated'}), 200
        else:
            return jsonify({'message': 'ad does not exist'}), 404


app.add_url_rule('/ad', view_func=AdView.as_view('ad_add'), methods=['POST'])
app.add_url_rule('/ad/<int:ad_id>', view_func=AdView.as_view('ad_delete'), methods=['DELETE'])
app.add_url_rule('/ad/<int:ad_id>', view_func=AdView.as_view('ad_update'), methods=['POST', 'PATCH'])
app.add_url_rule('/ad/<int:ad_id>', view_func=AdView.as_view('ad_view'), methods=['GET'])

app.run()
