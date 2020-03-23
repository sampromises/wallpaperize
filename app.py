import io
import os
import re

from flask import Flask, flash, redirect, render_template, request, send_file, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from image.color import RGB
from image.convert import create_wallpaper, get_wallpaper_filename
from PIL import Image
from resolution import Resolution, get_latest_resolutions
from s3_client import get_s3_path, upload_image
from wtforms import BooleanField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

IMAGES = tuple("jpg jpe jpeg png gif svg bmp".split())


class UploadForm(FlaskForm):
    image = FileField(
        "Image",
        validators=[InputRequired(), FileAllowed(IMAGES, "Only images allowed.")],
    )
    resolution = SelectField(
        "Device Resolution",
        validators=[InputRequired()],
        choices=get_latest_resolutions(),
        description="Find your device from the dropdown.",
    )
    user_color = StringField("Background Color", validators=[])
    use_default_color = BooleanField("Choose best background color for me",)
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


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            field_name = getattr(form, field).label.text
            error_msg = error
            flash(f"Error in the {field_name} field: {error_msg}")


@app.route("/<wallpaper_filename>")
def wallpaper(wallpaper_filename):
    s3_path = get_s3_path(wallpaper_filename)
    return render_template("wallpaper.html", wallpaper_path=s3_path)


@app.route("/", methods=("GET", "POST"))
def index():
    form = UploadForm()
    if form.validate_on_submit():
        print("Form submitted successfully!")
        print(f"Submitted filename: {form.image.data.filename}")
        print(f"Submitted resolution: {form.resolution.data}")
        res = parse_res(form.resolution.data)

        if form.use_default_color.data:
            color = None
        else:
            color = RGB.from_hex(form.user_color.data)

        wallpaper = create_wallpaper(Image.open(form.image.data), res, color)
        wallpaper_filename = get_wallpaper_filename(form.image.data.filename, res)
        print(f"New wallpaper name: {wallpaper_filename}")

        print(f"Uploading to S3...")
        upload_image(wallpaper, wallpaper_filename)
        s3_path = get_s3_path(wallpaper_filename)
        print(f"Done, uploaded to: {s3_path}")

        return redirect(url_for("wallpaper", wallpaper_filename=wallpaper_filename))
    elif request.method == "POST":
        print(f"Form errors: {form.errors}")
        flash_errors(form)
        return redirect(url_for("index"))
    return render_template("index.html", form=form)
