from modules.engine_v2 import *
feature = 'Text-to-Image - V2'

# _____________________________________________________________________
#   Copyright © 2023-2024 Ikmal Said. All rights reserved.
#
#   This program is the property of Ikmal Said. You may not reproduce
#   distribute, or modify this code without the express permission of 
#   the author, Ikmal Said.
# _____________________________________________________________________
#                                                                   

with ui.Blocks(title=title(feature), theme=ui.themes.Monochrome(), analytics_enabled=False) as stella:
    with ui.Tab(feature):
        result_v2 = ui.Gallery(format='png', show_label=False, object_fit="contain", height="94.7615324472244vh", show_share_button=False)
        prompt_v2 = ui.Textbox(label=sprompt, placeholder=spholder)
        clear_v2 = ui.ClearButton(value="Clear", components=[result_v2, prompt_v2])
        cancel_v2 = ui.Button(value='Cancel')
        submit_v2= ui.Button("Submit", variant="primary", scale=3)

    with ui.Tab('Settings'):        
        with ui.Accordion('More options'):        
            with ui.Row(equal_height=True):
                style_v2 = ui.Dropdown(label=sstyle, choices=list(stella_v2.keys()), value='None', filterable=False, min_width=512)
                model_v2 = ui.Dropdown(label=smodel, choices=list(ckpt_v2.keys()), value='Dreamshaper XL Lightning', filterable=False, min_width=512)
            with ui.Row(equal_height=True):
                ratio_v2 = ui.Dropdown(label=sratio, choices=list(ratio.keys()), value='Square (1:1)', filterable=False, min_width=512)
                with ui.Column():
                    quality_v2 = ui.Dropdown(label=squality, choices=quality+['Transparent', 'Face Avatar (Testing)', 'Creative Upscale (Testing)'], value='Enhanced', filterable=False, min_width=512)
                    face_v2 = ui.Image(type='filepath', min_width=512, height=256, label='Face Avatar Input', show_label=False)
            with ui.Row(equal_height=True):
                smart_v2 = ui.Dropdown(label=ssmart, choices=smart, value='Disabled', filterable=False, min_width=512)
                with ui.Row(equal_height=True):    
                    seedtype_v2 = ui.Dropdown(label='Seed type:', choices=['Randomized', 'Fixed'], value='Randomized', filterable=False, min_width=512)
                    seedno_v2 = ui.Number(label='Seed value:', value=0, minimum=0, maximum=max_seed, visible=False, min_width=80)

    process_v2 = submit_v2.click(fn=queue_v2, inputs=[prompt_v2, model_v2, style_v2, ratio_v2, quality_v2, smart_v2, seedtype_v2, seedno_v2, face_v2], outputs=[result_v2, result_v2])
    prompt_v2.submit(fn=queue_v2, inputs=[prompt_v2, model_v2, style_v2, ratio_v2, quality_v2, smart_v2, seedtype_v2, seedno_v2, face_v2], outputs=[result_v2, result_v2])
    seedtype_v2.select(fn=seeds, inputs=seedtype_v2, outputs=seedno_v2)
    cancel_v2.click(fn=None, inputs=None, outputs=None, cancels=process_v2)

if __name__ == "__main__":
    stella.queue(default_concurrency_limit=100).launch(inbrowser=True, favicon_path="favicon.ico")
    