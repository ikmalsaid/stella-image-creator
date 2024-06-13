import requests; from requests.exceptions import Timeout
from io import BytesIO; from PIL import Image;

from modules.service_endpoints import *
from modules.service_configs import *

def eraser(input_img, progress=ui.Progress()):
    image_pil = Image.fromarray(input_img["background"])
    mask_pil = Image.fromarray(input_img["layers"][0])
    image_bytes = BytesIO()
    mask_bytes = BytesIO()
    image_pil.save(image_bytes, format='PNG')
    mask_pil.save(mask_bytes, format='PNG')

    print(receive())
    
    payload = {
        'model_version': (None, '1'),
        'cfg': (None, '9.5'),
        'priority': (None, '1'),
    }
    
    data = {
        'image': ('input_image.png', image_bytes.getvalue(), 'image/png'),
        'mask': ('input_mask.png', mask_bytes.getvalue(), 'image/png')
    }

    try:
        progress(0.95, desc="Processing image")
        response = requests.post(mode['eraser'], headers=head, data=payload, files=data, timeout=(None, None))

        if len(response.content) < 65 * 1024:
            print(reject())
            return None
        
        print(done())
        return [Image.open(BytesIO(response.content))]
    
    except Timeout:
        print(timeout())
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        ui.Warning(message=single_error)
        return None

def submit(a):
    # input, output, submit, try again, eraser
    return ui.ImageEditor(visible=False), ui.Gallery(visible=True), ui.Button(visible=False), ui.Button(visible=True), eraser(a)

def reset():
    # input, output, submit, try again
    return ui.ImageEditor(visible=True), ui.Gallery(visible=False), ui.Button(visible=True), ui.Button(visible=False)