import requests; from requests.exceptions import Timeout
from io import BytesIO; from PIL import Image, ImageEnhance; import concurrent.futures, time

from modules.service_endpoints import *
from modules.input_configs import *
from modules.styles_v1 import *
from modules.models_v1 import *
from modules.service_configs import *
from modules.engine_upscale_alt import *

def gen_v1(prompt, model, style, size, quality, seed_type, seed_num):
    prompt = stella_v1[style].format(prompt=prompt)
    print(f"{receive()} -> {prompt}")
    
    if seed_type == 'Randomized': seed_number = random.randint(0, max_seed)
    else: seed_number = seed_num
    
    data = {
        'model_version': (None, '1'),
        'prompt': (None, prompt),
        'style_id': (None, ckpt_v1[str(model)]),
        'negative_prompt': (None, 'hands, face, eyes, legs'),
        'aspect_ratio': (None, ratio[str(size)]),
        'high_res_results': (None, '1'),
        'cfg': (None, '10'),
        'priority': (None, '1'),
        'seed': (None, str(seed_number))
    }
    
    try:
        response = requests.post(mode['generate'], headers=head, files=data, timeout=(60, 60))
        
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
        
        if quality == 'Upscaled':
            print("better3 -> upscaled output")
            better3 = Image.open(BytesIO(response.content))
            return upscale(better3)
       
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

def queue_v1(a, b, c, d, e, f, g, h, progress=ui.Progress()):
    if g == 'Randomized': quantities = 2
    else: quantities = 1
    
    result_list = [None] * quantities
    percent = 0
    
    if f == 'Fusion': a = translate(a)
 
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for i in range(quantities):
            future = executor.submit(lambda x: gen_v1(a, b, c, d, e, g, h), i)
            futures.append(future)
            multiplier = 0.95 / quantities
            percent += multiplier
            progress(percent, desc=f"Generating results")
            time.sleep(0.25)

    for i, future in enumerate(futures):
        result = future.result()
        result_list[i] = result

    successful_results = [result for result in result_list if result is not None]
    
    if g == 'Randomized': return successful_results, ui.Gallery(columns=1, rows=2)
    else: return successful_results, ui.Gallery(columns=1, rows=1)