#!/usr/bin/env python3
"""Task 7 module"""


from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz

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


# To make this work comment out line 30, 56 and uncomment line 106 - 109
# since new versions doesn't support it anymore
@babel.localeselector
def get_locale():
    """Selects the language best match for the locale from the
    configured languages"""

    # Locale from URL parameter
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    # locale from user settings
    if g.user:
        locale = g.user.get('locale')
        if locale and locale in app.config['LANGUAGES']:
            return locale

    # Locale from request header
    locale = request.headers.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    # Default locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """Infers appropriate timezone"""

    # Timezone from URL parameter
    timezone = request.args.get('timezone')
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone

        except pytz.exceptions.UnknownTimeZoneError as e:
            return app.config["BABEL_DEFAULT_TIMEZONE"]

    # Timezone from users preference
    if g.user and g.user.get('timezone') in users.values():
        try:
            timezone = g.user.get('timezone')
            return pytz.timezone(timezone)

        except pytz.exceptions.UnknownTimeZoneError as e:
            return app.config["BABEL_DEFAULT_TIMEZONE"]

    # Default Timezone
    return app.config["BABEL_DEFAULT_TIMEZONE"]


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
    return render_template("7-index.html")


# babel.init_app(
#     app, locale_selector=get_locale,
#     timezone_selector=get_timezone
# )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
