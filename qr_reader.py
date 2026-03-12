import cv2
import numpy as np
import requests
from huggingface_hub import hf_hub_download

print("Loading WeChat QR models...")

detect_prototxt = hf_hub_download(
    repo_id="opencv/opencv_zoo",
    filename="models/qrcode_wechatqrcode/detect_2021nov.prototxt"
)

detect_model = hf_hub_download(
    repo_id="opencv/opencv_zoo",
    filename="models/qrcode_wechatqrcode/detect_2021nov.caffemodel"
)

sr_prototxt = hf_hub_download(
    repo_id="opencv/opencv_zoo",
    filename="models/qrcode_wechatqrcode/sr_2021nov.prototxt"
)

sr_model = hf_hub_download(
    repo_id="opencv/opencv_zoo",
    filename="models/qrcode_wechatqrcode/sr_2021nov.caffemodel"
)

detector = cv2.wechat_qrcode.WeChatQRCode(
    detect_prototxt,
    detect_model,
    sr_prototxt,
    sr_model
)


def download_image(url):

    resp = requests.get(url)

    img_array = np.asarray(bytearray(resp.content), dtype=np.uint8)

    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    return img


def read_qr_from_url(url):

    img = download_image(url)

    if img is None:
        return None

    res, points = detector.detectAndDecode(img)

    if len(res) > 0:
        return res[0]

    # thử xoay ảnh
    for k in range(1,4):

        rotated = np.rot90(img, k)

        res, _ = detector.detectAndDecode(rotated)

        if len(res) > 0:
            return res[0]

    return None