import qrcode 
import cv2     
# Encode function (QR code banana)
def encode_qr(data, filename):
    img = qrcode.make(data)
    img.save(filename)
    print(f'QR code saved as {filename}')

# Decode function (QR code padhna)
def decode_qr(filename):
    img = cv2.imread(filename)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    if data:
        print('Decoded data:', data)
    else:
        print('No QR code found.')

if __name__ == '__main__':
    choice = input('Do you want to encode or decode a QR code? (e/d): ').lower()
    if choice == 'e':
        data = input('Enter the data/text to encode: ')
        filename = input('Enter filename to save QR code (e.g. myqr.png): ')
        encode_qr(data, filename)
    elif choice == 'd':
        filename = input('Enter the QR code image filename to decode: ')
        decode_qr(filename)
    else:
        print('Invalid choice.') 