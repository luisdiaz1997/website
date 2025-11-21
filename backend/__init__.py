from pathlib import Path
from io import BytesIO
import base64

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from PIL import Image, ImageOps
import numpy as np
import torch
from torchvision import models


BASE_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = BASE_DIR / "frontend" / "dist"
MODEL_PATH = BASE_DIR / "modelzoo" / "mymodel"

app = Flask(__name__, static_folder=None)
CORS(app)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def load_model():
    model = models.resnet34(pretrained=True)
    model.conv1 = torch.nn.Conv2d(
        in_channels=1,
        out_channels=64,
        kernel_size=(7, 7),
        stride=(2, 2),
        padding=(3, 3),
        bias=False,
    )
    model.fc = torch.nn.Linear(model.fc.in_features, 10)
    state_dict = torch.load(MODEL_PATH, map_location=device)
    model.load_state_dict(state_dict)
    model.eval()
    model.to(device)
    return model


classifier = load_model()


def _decode_image_from_request() -> Image.Image:
    """
    Accepts base64 data URLs from multipart form uploads, JSON, or raw bodies.
    """
    data_url = None

    # Multipart/form-data
    if "image" in request.form:
        data_url = request.form.get("image")

    # JSON payload
    if data_url is None and request.is_json:
        data_url = (request.get_json(silent=True) or {}).get("image")

    # Raw body fallback
    if data_url is None and request.data:
        try:
            data_url = request.data.decode()
        except Exception:
            data_url = None

    if not data_url:
        return None

    try:
        payload = data_url.split(",", 1)[1] if "," in data_url else data_url
        raw = base64.b64decode(payload)
        img = Image.open(BytesIO(raw)).convert("RGBA")
        return img
    except Exception:
        return None


@app.route("/process_number", methods=["POST"])
def process_number():
    """
    Accept a base64 data URL (PNG) and return model predictions.
    """
    img = _decode_image_from_request()
    if img is None:
        return jsonify(error="Invalid image payload"), 400

    resized = ImageOps.fit(img, (28, 28))
    tensor = (
        torch.tensor(np.array(resized)[None, None, :, :, 3], dtype=torch.float32)
        * (1 / 255.0)
    ).to(device)

    with torch.inference_mode():
        logits = classifier(tensor)
        preds = torch.nn.functional.softmax(logits, dim=1)[0].cpu().numpy().tolist()
    return jsonify(predictions=preds)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue_app(path: str):
    """
    Serve built Vue assets, falling back to index.html for client-side routing.
    """
    target = DIST_DIR / path
    if path and target.is_file():
        return send_from_directory(DIST_DIR, path)
    return send_from_directory(DIST_DIR, "index.html")
