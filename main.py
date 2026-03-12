# uvicorn main:app --reload 


from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from qr_reader import read_qr_from_url

app = FastAPI()


class CCCDRequest(BaseModel):
    image_url: str


def parse_cccd(qr_text):

    parts = qr_text.split("|")

    print("QR PARTS:", parts)

    soCCCD = parts[0]
    hoTen = parts[1]

    # tìm field có dạng ngày
    ngaySinh = None
    ngayCap = None

    for p in parts:

        if len(p) == 8 and p.isdigit():

            if ngaySinh is None:
                ngaySinh = p
            else:
                ngayCap = p

    return {
        "soCCCD": soCCCD,
        "hoTen": hoTen,
        "ngaySinh": datetime.strptime(ngaySinh, "%d%m%Y").date() if ngaySinh else None,
        "ngayCap": datetime.strptime(ngayCap, "%d%m%Y").date() if ngayCap else None,
        "raw": parts
    }


@app.post("/cccd/scan")
def scan_cccd(req: CCCDRequest):

    qr_text = read_qr_from_url(req.image_url)

    if qr_text is None:
        return {"error": "Không đọc được QR"}

    return parse_cccd(qr_text)