import requests; from requests.exceptions import Timeout
from io import BytesIO; from PIL import Image, ImageEnhance; import concurrent.futures, time

from modules.service_endpoints import *
from modules.input_configs import *
from modules.models_remix import *
from modules.styles_v1 import *
from modules.service_configs import *
from modules.engine_upscale_alt import *
from modules.engine_describe import *

def sketch(input_sketch, prompt, model, style, type, quality):
    image_bytes = BytesIO()
    input_sketch.save(image_bytes, format='png')
    prompt = stella_v1[style].format(prompt=prompt)
    
    print(f"{receive()} -> {prompt}")
    
    payload = {
        'model_version': (None, '1'),
        'prompt': (None, prompt),
        'style_id': (None, ckpt_remix[str(model)]),
        'control': (None, mode_remix[str(type)]),
        'negative_prompt': (None, 'hands, face, eyes, legs'),
        'strength': '40',
        'cfg': (None, '9.5'),
        'priority': (None, '1'),
    }
    
    data = {'image': ('input_sketch.png', image_bytes.getvalue(), 'image/png')}
      
    try:
        response = requests.post(mode['remix'], headers=head, data=payload, files=data, timeout=(60, 60))
        
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

def queue_sketch(a, b, c, d, e, f, g, progress=ui.Progress()):
    quantities = 2
    result_list = [None] * quantities
    percent = 0
    if g == 'Fusion': b = translate(b)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for i in range(quantities):
            future = executor.submit(lambda x: sketch(a['composite'], b, c, d, e, f), i)
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

def submit(a, b, c, d, e, f, g):
    # input, output, submit, try again, sketch
    return ui.ImageEditor(visible=False), ui.Gallery(visible=True), ui.Button(visible=False), ui.Button(visible=True), queue_sketch(a, b, c, d, e, f, g), ui.Button(visible=False)

def reset():
    # input, output, submit, try again
    return ui.ImageEditor(visible=True), ui.Gallery(visible=False), ui.Button(visible=True), ui.Button(visible=False), ui.Button(visible=True)

def update(a):
    return describe_png(a['composite'])