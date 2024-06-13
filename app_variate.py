from modules.engine_variate import *
feature = 'Image Variation'
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
        with ui.Row(equal_height=True):
            input_variate = ui.Image(type='pil', show_label=False, height="51.3vh", sources=['upload'], min_width=512)
            output_variate = ui.Gallery(show_label=False, object_fit="contain", height="50vh", show_share_button=False, columns=1, rows=2, min_width=512)
        prompt_variate = ui.Textbox(label=sprompt1, placeholder=spholder, lines=5)
        with ui.Row():
            clear_variate = ui.ClearButton(value="Reset", components=[input_variate, output_variate, prompt_variate])
            submit_variate = ui.Button("Submit", variant="primary")
        
        with ui.Accordion('More options'): 
            style_variate = ui.Dropdown(label=sstyle, choices=list(stella_v1.keys()), value='None', filterable=False)
            model_variate = ui.Dropdown(label=smodel, choices=list(ckpt_variate.keys()), value='Dream Shaper', filterable=False)
            quality_variate = ui.Dropdown(label=squality, choices=quality, value='Enhanced', filterable=False)
            smart_variate = ui.Dropdown(label=ssmart, choices=['Disabled', 'Fusion'], value='Disabled', filterable=False)
                
    process_variate = submit_variate.click(fn=queue_variate, inputs=[input_variate, prompt_variate, model_variate, style_variate, quality_variate, smart_variate], outputs=[output_variate])
    prompt_variate.submit(fn=queue_variate, inputs=[input_variate, prompt_variate, model_variate, style_variate, quality_variate, smart_variate], outputs=[output_variate])
    input_variate.upload(fn=describe, inputs=[input_variate], outputs=[prompt_variate])
    
if __name__ == "__main__":
    stella.queue(default_concurrency_limit=100).launch(inbrowser=True, favicon_path="favicon.ico")