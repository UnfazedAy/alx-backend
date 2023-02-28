#!/usr/bin/env python3
"""Task 3 module"""


from flask import Flask, render_template, request
from flask_babel import Babel


class Config(object):
    """Configurations for babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


# To make this work comment out line 23 and uncomment line 36
# since new versions doesn't support it anymore
@babel.localeselector
def get_locale():
    """Selects the language best match for the locale from the
    configured languages"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/", strict_slashes=False)
def index() -> str:
    """Serving the index page that has babel config"""
    return render_template("3-index.html")


# babel.init_app(app, locale_selector=get_locale)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
