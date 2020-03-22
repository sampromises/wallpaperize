import io
import os
import re

from flask import Flask, flash, redirect, render_template, send_file, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from image.convert import create_wallpaper, get_wallpaper_filename
from image.resolution import Resolution
from PIL import Image
from s3_client import get_s3_path, upload_image
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


def serve_pil_image(image):
    bytes = io.BytesIO()  # this is a file object
    image.save(bytes, "JPEG")
    bytes.seek(0)
    return send_file(bytes, mimetype="image/jpeg")


@app.route("/<wallpaper_filename>")
def wallpaper(wallpaper_filename):
    s3_path = get_s3_path(wallpaper_filename)
    return render_template("wallpaper.html", wallpaper_path=s3_path)


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
        wallpaper_filename = get_wallpaper_filename(form.image.data.filename, res)
        print(f"New wallpaper name: {wallpaper_filename}")

        print(f"Uploading to S3...")
        upload_image(wallpaper, wallpaper_filename)
        s3_path = get_s3_path(wallpaper_filename)
        print(f"Done, uploaded to: {s3_path}")

        return redirect(url_for("wallpaper", wallpaper_filename=wallpaper_filename))

    return render_template("index.html", form=form)
