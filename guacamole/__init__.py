import os

from flask import Flask
from flask import render_template
from flask_socketio import SocketIO

socketio = SocketIO()


def page_not_found(e):
    return render_template("errorpages/404.html"), 404


def create_app(test_config=None, debug=False):

    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
    )

    # apply the blueprints to the app
    from guacamole import api, auth, marketplace, me, messaging_system

    app.register_blueprint(api.bp)
    app.register_blueprint(messaging_system.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(marketplace.bp)
    app.register_blueprint(me.bp)

    app.register_error_handler(404, page_not_found)
    # make url_for('index') == url_for('marketplace.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="marketplace.index")

    socketio.init_app(app)
    return app

