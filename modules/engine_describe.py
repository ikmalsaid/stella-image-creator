import requests; from requests.exceptions import Timeout
from io import BytesIO

from modules.service_endpoints import *
from modules.service_configs import *

def describe(input_describe, progress=ui.Progress()):
    image_bytes = BytesIO()
    input_describe.save(image_bytes, format='jpeg')
    print(receive())
    
    payload = {'model_version': (None, '1')}; data = [('image',('_describe.jpg', image_bytes.getvalue(), 'image/jpeg'))]
    
    try:
        progress(0.95, desc="Describing image")
        response = requests.post(mode['describe'], headers=head, data=payload, files=data, timeout=30)
        result = response.text.split(',', 1)
        described = result[0]
        print(done())
        return described
    
    except Timeout:
        print(timeout())
        ui.Warning(message=single_error)
        return None
    
    except Exception as e:
        print(f"An error occurred: {e}")
        ui.Warning(message=single_error)
        return None

def describe_png(input_describe, progress=ui.Progress()):
    image_bytes = BytesIO()
    input_describe.save(image_bytes, format='png')
    print(receive())
    
    payload = {'model_version': (None, '1')}; data = [('image',('_describe.png', image_bytes.getvalue(), 'image/png'))]
    
    try:
        progress(0.95, desc="Describing image")
        response = requests.post(mode['describe'], headers=head, data=payload, files=data, timeout=30)
        result = response.text.split(',', 1)
        described = result[0]
        print(done())
        return described
    
    except Timeout:
        print(timeout())
        ui.Warning(message=single_error)
        return None
    
    except Exception as e:
        print(f"An error occurred: {e}")
        ui.Warning(message=single_error)
        return None