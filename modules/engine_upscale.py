import requests; from requests.exceptions import Timeout
from io import BytesIO; from PIL import Image

from modules.service_endpoints import *
from modules.service_configs import *

def upscale(upscale_input, progress=ui.Progress()):
    image_bytes = BytesIO()
    upscale_input.save(image_bytes, format='JPEG')
    print(receive())
    
    payload = {'model_version': (None, '1')}; data = [('image',('upscale_input.jpg', image_bytes.getvalue(), 'image/jpeg'))]

    try:
        progress(0.95, desc="Upscaling image")
        response = requests.post(mode['upscale'], headers=head, data=payload, files=data, timeout=(60, 60))
                
        if len(response.content) < 65 * 1024:
            print(reject())
            ui.Warning(message=single_error)
            return None
        
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
