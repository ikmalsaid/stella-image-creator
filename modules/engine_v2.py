import requests, io, tempfile; from requests.exceptions import Timeout
from PIL import Image, ImageEnhance; import concurrent.futures, time
from gradio_client import Client

from modules.service_endpoints import *
from modules.input_configs import *
from modules.styles_v2 import *
from modules.models_v2 import *
from modules.service_configs import *
from modules.engine_upscale_alt import *
from modules.engine_bgremove_alt import *

def gen_v2(prompt, model, style, size, quality, seed_type, seed_num, face_src):
    prompt = stella_v2[style]['prompt'].format(prompt=prompt)
    # negative_v2 = stella_v2[style]['negative_prompt']
    if seed_type == 'Randomized': seed_number = random.randint(0, max_seed)
    else: seed_number = seed_num
    
    print(f"{receive()} -> {prompt}")

    data = {
        'model_version': (None, '1'),
        'prompt': (None, prompt),
        'style_id': (None, ckpt_v2[str(model)]),
        'negative_prompt': (None, 'hands, face, eyes, legs'),
        'aspect_ratio': (None, ratio[str(size)]),
        'high_res_results': (None, '1'),
        'cfg': (None, '9.5'),
        'priority': (None, '1'),
        'seed': (None, str(seed_number))
    }
    
    try:
        if model == 'Realtime':
            response = requests.post(mode['turbo'], headers=head, files=data, timeout=(60, 60))
        else:
            response = requests.post(mode['generate'], headers=head, files=data, timeout=(60, 60))
        
        if model != 'Turbo V3' and len(response.content) < 65 * 1024:
            print(reject() + str(response.content))
            return None
        
        print(done())
        
        if quality == 'Creative Upscale (Testing)':
            print("creative -> superior output")
            superior = creative_img(Image.open(BytesIO(response.content)))
            return superior
        
        if quality == 'Enhanced':
            print("better1 -> better output")
            better1 = enhance_img(Image.open(BytesIO(response.content)))
            return better1
        
        if quality == 'Enhanced and Upscaled':
            print("better2 -> better upscaled output")
            better2 = enhance_img(Image.open(BytesIO(response.content)))
            return upscale(better2)
        
        if quality == 'Upscaled':
            print("better3 -> upscaled output")
            better3 = Image.open(BytesIO(response.content))
            return upscale(better3)
        
        if quality == 'Transparent':
            print("better4 -> transparent output")
            better3 = Image.open(BytesIO(response.content))
            return bgremove(better3)
        
        if quality == 'Face Avatar (Testing)':
            print("better5 -> enhanced face swap output")
            gen2_buffer = io.BytesIO()
            Image.open(BytesIO(response.content)).save(gen2_buffer, format='PNG')
            
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                temp_file.write(gen2_buffer.getvalue())
                gen2_target = temp_file.name
            
            try:
                client = Client("https://felixrosberg-face-swap.hf.space/")
                result = client.predict(gen2_target, face_src,	0, 0, [], api_name="/run_inference")
                return enhance_img(Image.open(result))
            
            except:
                print('unable to complete face swap')
                return enhance_img(Image.open(BytesIO(response.content)))
            
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

def queue_v2(a, b, c, d, e, f, g, h, face,  progress=ui.Progress()):
    if g == 'Randomized': quantities = 2
    else: quantities = 1
    
    result_list = [None] * quantities
    percent = 0
    
    if f == 'Fusion': a = translate(a)
    if f == 'Expansion': a = expand(a)
    if f == 'Fusion and Expansion': a = expand(translate(a))
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for i in range(quantities):
            future = executor.submit(lambda x: gen_v2(a, b, c, d, e, g, h, face), i)
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
    
def enhance_img(image):
    return ImageEnhance.Contrast(ImageEnhance.Color(ImageEnhance.Brightness(ImageEnhance.Sharpness(image).enhance(2.00)).enhance(1.05)).enhance(1.05)).enhance(1.05)

def creative_img(image):
    image_bytes = BytesIO()
    image.save(image_bytes, format='JPEG')
    print('creative upscale starting...')
    
    payload = {
        'model_version': (None, '1'),
        'prompt': (None, ''),
        'creativity': (None, '0.35'),
        'resemblance': (None, '1'),
        'style_id': (None, '6'),
        'hdr': (None, '0.35'),
        'negativePrompt': (None, 'hands, jpeg'),
        'negative_prompt': (None, 'hands, jpeg')               
    }
    
    data = [('image',('image.jpg', image_bytes.getvalue(), 'image/jpeg'))]

    try:
        response = requests.post(mode['creative'], headers=head, data=payload, files=data, timeout=(60, 60))

        print(done())
        return Image.open(BytesIO(response.content))
    
    except Timeout:
        print('creative timeout')
        return image

    except Exception as e:
        print(f"An error occurred: {e}")
        return image