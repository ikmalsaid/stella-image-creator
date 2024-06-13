from modules.engine_v1 import *
feature = 'Text-to-Image - V1'
'''
_____________________________________________________________________

  Copyright © 2023-2024 Ikmal Said. All rights reserved.
   
  This program is the property of Ikmal Said. You may not reproduce
  distribute, or modify this code without the express permission of 
  the author, Ikmal Said.
_____________________________________________________________________
                                                                     
'''
with ui.Blocks(css=css, title=title(feature), theme=theme, analytics_enabled=False) as stella:
    with ui.Group():  
        result_v1 = ui.Gallery(show_label=False, object_fit="contain", height="50vh", show_share_button=False)  
        prompt_v1 = ui.Textbox(label=sprompt, placeholder=spholder)
        with ui.Row():
            clear_v1 = ui.ClearButton(value="Reset", components=[result_v1, prompt_v1])
            submit_v1= ui.Button("Submit", variant="primary")
      
        with ui.Accordion('More options'):
            style_v1 = ui.Dropdown(label=sstyle, choices=list(stella_v1.keys()), value='None', filterable=False)
            model_v1 = ui.Dropdown(label=smodel, choices=list(ckpt_v1.keys()), value='Dream Shaper', filterable=False)
            ratio_v1 = ui.Dropdown(label=sratio, choices=list(ratio.keys()), value='Square (1:1)', filterable=False)
            quality_v1 = ui.Dropdown(label=squality, choices=quality, value='Enhanced', filterable=False)
            smart_v1 = ui.Dropdown(label=ssmart, choices=['Disabled', 'Fusion'], value='Disabled', filterable=False)
            with ui.Row():
                seedtype_v1 = ui.Dropdown(label='Seed type:', choices=['Randomized', 'Fixed'], value='Randomized', filterable=False)
                seedno_v1 = ui.Number(label='Seed value:', value=0, minimum=0, maximum=max_seed, visible=False)

    process_v1 = submit_v1.click(fn=queue_v1, inputs=[prompt_v1, model_v1, style_v1, ratio_v1, quality_v1, smart_v1, seedtype_v1, seedno_v1], outputs=[result_v1, result_v1])
    prompt_v1.submit(fn=queue_v1, inputs=[prompt_v1, model_v1, style_v1, ratio_v1, quality_v1, smart_v1, seedtype_v1, seedno_v1], outputs=[result_v1, result_v1])
    seedtype_v1.select(fn=seeds, inputs=seedtype_v1, outputs=seedno_v1)

if __name__ == "__main__":
    stella.queue(default_concurrency_limit=100).launch(inbrowser=True, favicon_path="favicon.ico")