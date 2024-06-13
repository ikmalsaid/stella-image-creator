from modules.engine_remix import *
feature = 'Image Remix'

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
        input_remix = ui.Image(type='pil', show_label=False, height="40vh", sources=['upload'])
        output_remix = ui.Gallery(show_label=False, object_fit="contain", height="50vh", show_share_button=False)
        prompt_remix = ui.Textbox(label=sprompt1, placeholder=spholder)
        with ui.Row():
            ui.ClearButton(value="Reset", components=[input_remix, output_remix, prompt_remix])
            submit_remix = ui.Button("Submit", variant="primary")
     
        with ui.Accordion('More options'):    
            style_remix = ui.Dropdown(label=sstyle, choices=list(stella_v1.keys()), value='None', filterable=False)
            model_remix = ui.Dropdown(label=smodel, choices=list(ckpt_remix.keys()), value='Toon V1', filterable=False)
            mode_remix = ui.Dropdown(label=smode, choices=list(mode_remix), value='Scribble', filterable=False)
            quality_remix = ui.Dropdown(label=squality, choices=quality, value='Enhanced', filterable=False)
            smart_remix = ui.Dropdown(label=ssmart, choices=['Disabled', 'Fusion'], value='Disabled', filterable=False)

    process_remix = submit_remix.click(fn=queue_remix, inputs=[input_remix, prompt_remix, model_remix, style_remix, mode_remix, quality_remix, smart_remix], outputs=[output_remix])
    prompt_remix.submit(fn=queue_remix, inputs=[input_remix, prompt_remix, model_remix, style_remix, mode_remix, quality_remix, smart_remix], outputs=[output_remix])
    input_remix.upload(fn=describe, inputs=[input_remix], outputs=[prompt_remix])

if __name__ == "__main__":
    stella.queue(default_concurrency_limit=100).launch(inbrowser=True, favicon_path="favicon.ico")