from modules.engine_sketchpad import *
feature = 'AI Sketchpad'

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
        input_sketch = ui.Paint(type='pil', show_label=False, transforms=[],
                                brush=ui.Brush(default_size=12, default_color='#FFFFFF', colors=['#000000', '#FFFFFF', '#FF0000', '#00FF00', '#0000FF']),
                                eraser=ui.Eraser(default_size=12))
        
        output_sketch = ui.Gallery(show_label=False, object_fit="contain", height="50vh", show_share_button=False, visible=False)
        with ui.Row():
            prompt_sketch = ui.Textbox(label=sprompt1, placeholder=spholder)
        with ui.Row():
            clear_sketch = ui.ClearButton(value="Reset", components=[input_sketch, output_sketch, prompt_sketch])
            submit_sketch = ui.Button("Submit", variant="primary")
            retry_sketch = ui.Button("Try Again", variant="primary", visible=False)
     
        with ui.Accordion('More options'):    
            style_sketch = ui.Dropdown(label=sstyle, choices=list(stella_v1.keys()), value='None', filterable=False)
            model_sketch = ui.Dropdown(label=smodel, choices=list(ckpt_remix.keys()), value='Toon V1', filterable=False)
            mode_sketch = ui.Dropdown(label=smode, choices=list(mode_remix), value='Scribble', filterable=False, visible=False)
            quality_sketch = ui.Dropdown(label=squality, choices=quality, value='Enhanced', filterable=False)
            smart_sketch = ui.Dropdown(label=ssmart, choices=['Disabled', 'Fusion'], value='Disabled', filterable=False)
    
    process_sketch = submit_sketch.click(fn=submit, inputs=[input_sketch, prompt_sketch, model_sketch, style_sketch, mode_sketch, quality_sketch, smart_sketch], outputs=[input_sketch, output_sketch, submit_sketch, retry_sketch, output_sketch])
    prompt_sketch.submit(fn=submit, inputs=[input_sketch, prompt_sketch, model_sketch, style_sketch, mode_sketch, quality_sketch, smart_sketch], outputs=[input_sketch, output_sketch, submit_sketch, retry_sketch, output_sketch])
    clear_sketch.click(fn=reset, inputs=None, outputs=[input_sketch, output_sketch, submit_sketch, retry_sketch])
    retry_sketch.click(fn=reset, inputs=None, outputs=[input_sketch, output_sketch, submit_sketch, retry_sketch])
    input_sketch.change(fn=update, inputs=[input_sketch], outputs=[prompt_sketch])

if __name__ == "__main__":
    stella.queue(default_concurrency_limit=100).launch(inbrowser=True, favicon_path="favicon.ico")