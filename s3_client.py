import io
import os
import re

import boto3

BUCKET_NAME = os.environ.get("AWS_S3_BUCKET_NAME")


def _sanitize_s3_filename(filename):
    return re.sub(r"[^0-9a-zA-Z!\-_.*'()]", "", filename)


def get_image_format(filename):
    try:
        extension = filename.split(".")[-1].upper()
        if extension == "JPG":
            return "JPEG"
        else:
            return extension
    except:
        return "JPEG"


def upload_image(file, filename):
    s3_filename = _sanitize_s3_filename(filename)
    bytes = io.BytesIO()  # this is a file object
    file.save(bytes, get_image_format(s3_filename))
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(BUCKET_NAME)

    bucket.put_object(Key=s3_filename, Body=bytes.getvalue())


def get_s3_path(filename):
    s3_filename = _sanitize_s3_filename(filename)
    return f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_filename}"
