import requests; from requests.exceptions import Timeout
from io import BytesIO; from PIL import Image, ImageEnhance; import concurrent.futures, time

from modules.service_endpoints import *
from modules.input_configs import *
from modules.models_v1 import *
from modules.models_anime import *
from modules.styles_v1 import *
from modules.service_configs import *
from modules.engine_describe import *
from modules.engine_upscale_alt import *

def variate(input_variate, prompt, model, style, quality):
    image_bytes = BytesIO()
    input_variate.save(image_bytes, format='JPEG')
    prompt = stella_v1[style].format(prompt=prompt)
    
    print(f"{receive()} -> {prompt}")
    
    payload = {
        'model_version': (None, '1'),
        'prompt': (None, prompt),
        'style_id': (None, ckpt_variate[str(model)]),
        'negative_prompt': (None, 'hands, face, eyes, legs'),
        'cfg': (None, '9.5'),
        'strength': (None, '0.7'),
        'priority': (None, '0'),
        'prompt_processed': (None, '0'),
    }
    
    data = {
        'image': ('input_variate.jpg', image_bytes.getvalue(), 'image/jpeg')
    }
    
    try:
        response = requests.post(mode['variate'], headers=head, data=payload, files=data, timeout=(60, 60))

        if len(response.content) < 65 * 1024:
            print(reject())
            return None
        
        print(done())
 
        if quality == 'Enhanced':
            print("better1 -> better output")
            better1 = ImageEnhance.Contrast(
                    ImageEnhance.Color(
                        ImageEnhance.Brightness(
                            ImageEnhance.Sharpness(
                                Image.open(BytesIO(response.content))
                            ).enhance(2.00)
                        ).enhance(1.05)
                    ).enhance(1.05)
                ).enhance(1.05)
            return better1
        
        if quality == 'Enhanced and Upscaled':
            print("better2 -> better upscaled output")
            better2 = ImageEnhance.Contrast(
                    ImageEnhance.Color(
                        ImageEnhance.Brightness(
                            ImageEnhance.Sharpness(
                                Image.open(BytesIO(response.content))
                            ).enhance(2.00)
                        ).enhance(1.05)
                    ).enhance(1.05)
                ).enhance(1.05)
            return upscale(better2)
       
        else:
            print("original -> raw output")
            original = Image.open(BytesIO(response.content))
            return original
    
    except Timeout:
        print(timeout())
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        ui.Warning(message=single_error)
        return None

def queue_variate(a, b, c, d, e, f, progress=ui.Progress()):
    quantities = 2
    result_list = [None] * quantities
    percent = 0
    if f == 'Fusion': b = translate(b)
 
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for i in range(quantities):
            future = executor.submit(lambda x: variate(a, b, c, d, e), i)
            futures.append(future)
            multiplier = 0.95 / quantities
            percent += multiplier
            progress(percent, desc=f"Generating results")
            time.sleep(0.25)

    for i, future in enumerate(futures):
        result = future.result()
        result_list[i] = result

    successful_results = [result for result in result_list if result is not None]
    return successful_results

ckpt_variate = ckpt_v1 | ckpt_anime