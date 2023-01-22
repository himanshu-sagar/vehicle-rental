import qrcode
import cv2
from pyzbar import pyzbar
from django.core.exceptions import BadRequest
from django.conf import settings


class QrCode:
    base_path = "static/qr_codes/"

    def __init__(self, vehicle_id=None):
        self.vehicle_id = vehicle_id

    def generate_qr_code(self):
        # Generating QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.vehicle_id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        # Saving QR Code | Better to save these images in S3
        path = QrCode.base_path + self.vehicle_id + '.png'
        img.save(path)
        return path

    def decode_qr_code(self, image_path):
        try:
            # read QR code
            image = cv2.imread(image_path)
            #  decode QR code
            decoded_data = pyzbar.decode(image)
            self.vehicle_id = decoded_data[0].data.decode("utf-8")
        except Exception as e:
            raise BadRequest(str(e))
        return self.vehicle_id