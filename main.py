# uvicorn main:app --reload 
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from qr_reader import read_qr_from_url

app = FastAPI()


class CCCDRequest(BaseModel):
    image_url: str


# def parse_cccd(qr_text):

#     parts = qr_text.split("|")

#     print("QR PARTS:", parts)

#     soCCCD = parts[0]
#     hoTen = parts[1]

#     # tìm field có dạng ngày
#     ngaySinh = None
#     ngayCap = None

#     for p in parts:

#         if len(p) == 8 and p.isdigit():

#             if ngaySinh is None:
#                 ngaySinh = p
#             else:
#                 ngayCap = p
#     ngaySinh = ngaySinh.strip() if ngaySinh else None
#     ngayCap = ngayCap.strip() if ngayCap else None
#     return {
#         "soCCCD": soCCCD,
#         "hoTen": hoTen,
#         "ngaySinh": datetime.strptime(ngaySinh.strip(), "%d%m%Y").strftime("%Y-%m-%d") if ngaySinh else None,
#         "ngayCap": datetime.strptime(ngayCap.strip(), "%d%m%Y").strftime("%Y-%m-%d") if ngayCap else None,
#         "raw": parts
#     }

def parse_cccd(qr_text):

    parts = qr_text.split("|")
    print("QR PARTS:", parts)

    soCCCD = parts[0] if len(parts) > 0 else None
    hoTen = parts[2] if len(parts) > 2 else None
    ngaySinh = parts[3] if len(parts) > 3 else None
    gioiTinh = parts[4] if len(parts) > 4 else None
    noiThuongTru = parts[5] if len(parts) > 5 else None
    ngayCap = parts[6] if len(parts) > 6 else None

    return {
        "soCCCD": soCCCD,
        "hoTen": hoTen,
        "gioiTinh": gioiTinh,
        "noiThuongTru": noiThuongTru,
        "ngaySinh": datetime.strptime(ngaySinh, "%d%m%Y").strftime("%Y-%m-%d") if ngaySinh else None,
        "ngayCap": datetime.strptime(ngayCap, "%d%m%Y").strftime("%Y-%m-%d") if ngayCap else None,
        "raw": parts
    }


@app.post("/cccd/scan")
def scan_cccd(req: CCCDRequest):

    qr_text = read_qr_from_url(req.image_url)

    if qr_text is None:
        return {"error": "Không đọc được QR"}

    return parse_cccd(qr_text)