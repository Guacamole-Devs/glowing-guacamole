import os

from flask import Flask


def create_app(test_config=None):

    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "guacamole.sqlite"),
    )

    @app.route("/hello")
    def hello():
        return "Hello, World!"


    # apply the blueprints to the app
    from guacamole import auth, marketplace, me

    app.register_blueprint(auth.bp)
    app.register_blueprint(marketplace.bp)
    app.register_blueprint(me.bp)

    #make url_for('index') == url_for('marketplace.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="marketplace.index")

    return app 