from pymongo import MongoClient
import qrcode
import uuid

client = MongoClient('mongodb://localhost:27017/')
db = client['database']
col = db['Person']

def QrCode():
    while True:
        id = str(uuid.uuid4())
        if col.find_one({'_id': id}) is None:
            break
    url = f"http://127.0.0.1:5000/Person/{id}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(f"static/qr_codes/{id}.png")
    child = {
        '_id': id,
        'data': False
    }
    col.insert_one(child)

QrCode()
