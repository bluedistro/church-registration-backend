import base64, os
dir_path = 'images'
def base64Encoder(dir_path):
    image_directory = os.listdir(dir_path)
    if len(os.listdir(dir_path)) > 0:
        image_path = os.listdir(dir_path)[0]
        full_path = os.path.join(dir_path, image_path)
        with open(full_path, 'rb') as imageFile:
            str = base64.b64encode(imageFile.read())
        os.remove(full_path)
        return str
    else:
        return 'empty directory'

print(base64Encoder(dir_path))

def base64Decoder(preferredFileName: str, encodedImg: str):
    dir_path = 'images'
    imageFileName = preferredFileName + '.jpg'
    full_path = os.path.join(dir_path, imgFileName)
    with open(imageFileName, 'wb') as fimage:
        fimage.write(encodedImg.decode('base64'))
    return True