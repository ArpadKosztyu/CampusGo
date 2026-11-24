from pathlib import Path
import qrcode

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

qr_content = "GOLYAHET_MEGNYITO_2026"
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
qr.add_data(qr_content)
qr.make(fit=True)
img = qr.make_image()
output_path = ASSETS_DIR / "mock_qr.png"
img.save(output_path)

print(f"Mock QR-kód elkészült: {output_path}")