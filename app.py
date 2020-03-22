import os

from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SelectField, SubmitField

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")


class UploadForm(FlaskForm):
    upload = FileField(
        "Image",
        validators=[FileRequired(), FileAllowed(["jpg", "png"], "Images only!")],
    )
    resolution = SelectField(
        "Resolution",
        choices=[
            ((1125, 2436), "iPhone X/XS (1125x2436)"),
            ((1242, 2688), "iPhone XS Max (1242x2688)"),
            ((750, 1334), "iPhone 7/8 (750x1334)"),
            ((1080, 1920), "iPhone 7/8 Plus (1080x1920)"),
            ((2048, 2732), "iPad Pro (2048x2732)"),
            ((1536, 2048), "iPad Third & Fourth Generation (1536x2048)"),
            ((2560, 1600), "Macbook Pro 13-inch (2560x1600)"),
            ((1880, 1800), "Macbook Pro 15-inch (2880x1800)"),
            ((3072, 1920), "Macbook Pro 16-inch (3072x1920)"),
            ((500, 500), "Thumbnail (500x500)"),
            ((720, 480), "HD (720x480)"),
            ((1920, 1080), "FHD (1920x1080)"),
            ((2560, 1440), "QHD (2560x1440)"),
            ((3840, 2160), "4K (3840x2160)"),
        ],
        description="Find your device from the dropdown.",
    )
    submit = SubmitField("Submit")


@app.route("/")
def index():
    form = UploadForm()
    return render_template("index.html", form=form)
