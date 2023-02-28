#!/usr/bin/env python3
"""Task 5 module"""


from flask import Flask, render_template, request, g
from flask_babel import Babel

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    """Configurations for babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


# To make this work comment out line 30 and uncomment line 65
# since new versions doesn't support it anymore
@babel.localeselector
def get_locale():
    """Selects the language best match for the locale from the
    configured languages"""

    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """
    checks if a user exist and returns the user dict otherwise None
    """
    user_id = request.args.get('login_as')
    if not user_id or int(user_id) not in users.keys():
        return None
    return users.get(int(user_id))


@app.before_request
def before_request():
    """Executes before any other request is executed
    and also makes user global"""
    g.user = get_user()


@app.route("/", strict_slashes=False)
def index() -> str:
    """Serving the index page that has babel config"""
    return render_template("5-index.html")


# babel.init_app(app, locale_selector=get_locale)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
