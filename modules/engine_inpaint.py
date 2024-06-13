import requests; from requests.exceptions import Timeout, ConnectionError
from io import BytesIO; from PIL import Image; import concurrent.futures, time

from modules.service_endpoints import *
from modules.service_configs import *

def inpaint(input_image, input_mask, prompt):
    image_pil = Image.fromarray(input_image)
    mask_pil = Image.fromarray(input_mask)

    image_bytes = BytesIO()
    mask_bytes = BytesIO()
    image_pil.save(image_bytes, format='PNG', optimize=True)
    mask_pil.save(mask_bytes, format='PNG', optimize=True)
    
    print(f"{receive()} -> {prompt}")
    
    payload = {
        'model_version': (None, '1'),
        'prompt': (None, prompt),
        'neg_prompt': (None, "hands, face, eyes, legs"),
        'inpaint_strength': (None, '0.75'),
        'cfg': (None, '9.5'),
        'priority': (None, '1'),
    }
    
    data = {
        'image': ('input_image.png', image_bytes.getvalue(), 'image/png'),
        'mask': ('input_mask.png', mask_bytes.getvalue(), 'image/png')
    }

    try:
        response = requests.post(mode['inpaint'], headers=head, data=payload, files=data, timeout=(120, 120))

        if len(response.content) < 0 * 1024:
            print(reject())
            return None
        
        print(done())
        return Image.open(BytesIO(response.content))
    
    except Timeout:
        print(timeout())
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        ui.Warning(message=single_error)
        return None

def queue_inpaint(a, b, c, progress=ui.Progress()):
    quantities = 2
    result_list = [None] * quantities
    percent = 0
    if c == 'Fusion': b = translate(b)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for i in range(quantities):
            future = executor.submit(lambda x: inpaint(a["background"], a["layers"][0], b), i)
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

def submit(a, b, c):
    # input, output, submit, try again, inpaint
    return ui.ImageEditor(visible=False), ui.Gallery(visible=True), ui.Button(visible=False), ui.Button(visible=True), queue_inpaint(a, b, c)

def reset():
    # input, output, submit, try again
    return ui.ImageEditor(visible=True), ui.Gallery(visible=False), ui.Button(visible=True), ui.Button(visible=False)