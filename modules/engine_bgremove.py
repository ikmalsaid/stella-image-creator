import requests; from requests.exceptions import Timeout
from io import BytesIO; from PIL import Image

from modules.service_endpoints import *
from modules.service_configs import *

def bgremove(input_bgremove, progress=ui.Progress()):
    image_bytes = BytesIO()
    input_bgremove.save(image_bytes, format='JPEG')
    print(receive())
    
    payload = {'model_version': (None, '1')}; data = [('image',('_bgr.jpg', image_bytes.getvalue(), 'image/jpeg'))]

    try:
        progress(0.95, desc="Removing background")
        response = requests.post(mode['bgremove'], headers=head, data=payload, files=data, timeout=(60, 60))
        print(done())
        return [Image.open(BytesIO(response.content))]
    
    except Timeout:
        print(timeout())
        ui.Warning(message=single_error)
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        ui.Warning(message=single_error)
        return None