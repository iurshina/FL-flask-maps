import os
import sys
from flask import Flask, request, abort, jsonify, render_template, url_for, flash, redirect
from flask_cors import CORS
import traceback
from forms import NewLocationForm, AddPosts
from models_mongo import db_drop_and_create_all, Location, Post
from flask_mongoengine import MongoEngine


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        'db': 'mydatabase',
        'host': 'mongodb://127.0.0.1:27017',
    }
    db = MongoEngine(app)

    CORS(app)

    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    """ uncomment at the first time running the app. Then comment back so you do not erase db content over and over """
    db_drop_and_create_all(app, db)

    @app.route('/', methods=['GET'])
    def home():
        return render_template(
            'map.html',
            map_key=os.getenv('GOOGLE_MAPS_API_KEY', 'GOOGLE_MAPS_API_KEY_WAS_NOT_SET?!')
        )

    @app.route('/test', methods=['GET'])
    def test():
        return render_template(
            'posts.html',
        )

    @app.route('/detail', methods=['GET'])
    def detail():
        location_id = float(request.args.get('id'))
        item = Location.query.get(location_id)
        return render_template(
            'detail.html',
            item=item,
            map_key=os.getenv('GOOGLE_MAPS_API_KEY', 'GOOGLE_MAPS_API_KEY_WAS_NOT_SET?!')
        )

    @app.route("/new-location", methods=['GET', 'POST'])
    def new_location():
        form = NewLocationForm()

        if form.validate_on_submit():
            latitude = float(form.coord_latitude.data)
            longitude = float(form.coord_longitude.data)
            description = form.description.data

            location = Location(
                description=description,
                geom=Location.point_representation(latitude=latitude, longitude=longitude)
            )
            location.save()

            flash(f'New location created!', 'success')
            return redirect(url_for('home'))

        return render_template(
            'new-location.html',
            form=form,
            map_key=os.getenv('GOOGLE_MAPS_API_KEY', 'GOOGLE_MAPS_API_KEY_WAS_NOT_SET?!')
        )

    @app.route("/new-post", methods=['GET', 'POST'])
    def new_posts():
        form = AddPosts()

        if form.validate_on_submit():
            post = Post(
                title=form.title.data,
                content=form.content.data
            )
            db.session.add(post)
            db.session.commit()

            flash(f'New post added!', 'success')
            return redirect(url_for('home'))

        return render_template(
            'new-post.html',
            form=form,
            testing='hi there'
        )

    @app.route("/api/store_item")
    def store_item():
        try:
            latitude = float(request.args.get('lat'))
            longitude = float(request.args.get('lng'))
            description = request.args.get('description')

            location = Location(
                description=description,
                geom=Location.point_representation(latitude=latitude, longitude=longitude)
            )
            location.insert()

            return jsonify(
                {
                    "success": True,
                    "location": location.to_dict()
                }
            ), 200
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            app.logger.error(traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2))
            abort(500)

    @app.route("/api/get_items_in_radius")
    def get_items_in_radius():
        try:
            latitude = float(request.args.get('lat'))
            longitude = float(request.args.get('lng'))
            radius = int(request.args.get('radius'))

            locations = Location.get_items_within_radius(latitude, longitude, radius)
            return jsonify(
                {
                    "success": True,
                    "results": locations
                }
            ), 200
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            app.logger.error(traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2))
            abort(500)

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500

    return app, db


app, db = create_app()
if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='127.0.0.1',port=port,debug=True)