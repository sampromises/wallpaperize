import os
import re

from flask import Flask, flash, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from image.convert import create_wallpaper
from image.resolution import Resolution
from image.util import get_final_filename
from PIL import Image
from wtforms import SelectField, SubmitField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")


class UploadForm(FlaskForm):
    image = FileField(
        "Image",
        validators=[FileAllowed(["jpg", "jpeg", "png", "gif"], "Images only!")],
    )
    resolution = SelectField(
        "Resolution",
        validators=[InputRequired()],
        choices=[
            ("1125x2436", "iPhone X/XS (1125x2436)"),
            ("1242x2688", "iPhone XS Max (1242x2688)"),
            ("750x1334", "iPhone 7/8 (750x1334)"),
            ("1080x1920", "iPhone 7/8 Plus (1080x1920)"),
            ("2048x2732", "iPad Pro (2048x2732)"),
            ("1536x2048", "iPad Third & Fourth Generation (1536x2048)"),
            ("2560x1600", "Macbook Pro 13-inch (2560x1600)"),
            ("1880x1800", "Macbook Pro 15-inch (2880x1800)"),
            ("3072x1920", "Macbook Pro 16-inch (3072x1920)"),
            ("500x500", "Thumbnail (500x500)"),
            ("720x480", "HD (720x480)"),
            ("1920x1080", "FHD (1920x1080)"),
            ("2560x1440", "QHD (2560x1440)"),
            ("3840x2160", "4K (3840x2160)"),
        ],
        description="Find your device from the dropdown.",
    )
    submit = SubmitField("Submit")


def parse_res(resolution):
    res = Resolution(1920, 1080)  # Default
    try:
        match = re.search(r"([0-9]+)\s*[x,\s]\s*([0-9]+)\)?$", resolution)
        groups = match.groups()
        res = Resolution(int(groups[0]), int(groups[1]))
        print(f"Resolution given:{res}")
    except:
        flash(f"Invalid resolution, using default.")
    print(f"Parsed resolution: {res}")
    return res


@app.route("/", methods=("GET", "POST"))
def index():
    form = UploadForm()
    wallpaper_path = None
    if form.validate_on_submit():
        print("Form submitted successfully!")
        print(f"Submitted filename: {form.image.data.filename}")
        print(f"Submitted resolution: {form.resolution.data}")
        res = parse_res(form.resolution.data)

        color = None  # TODO Pick Color

        wallpaper = create_wallpaper(Image.open(form.image.data), res, color)
        wallpaper_filename = get_final_filename(form.image.data.filename, res)
        print(f"New wallpaper name: {wallpaper_filename}")

        wallpaper_path = wallpaper_filename

    return render_template("index.html", form=form, wallpaper_path=wallpaper_path)
