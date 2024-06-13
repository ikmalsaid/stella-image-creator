from modules.engine_inpaint import *
feature = 'Image Inpainting'
'''
_____________________________________________________________________

  Copyright © 2023-2024 Ikmal Said. All rights reserved.
   
  This program is the property of Ikmal Said. You may not reproduce
  distribute, or modify this code without the express permission of 
  the author, Ikmal Said.
_____________________________________________________________________
                                                                     
'''
with ui.Blocks(css=adj+css, title=title(feature), theme=theme, analytics_enabled=False) as stella:
    with ui.Group():
        input_inpaint = ui.ImageEditor(
            show_label=False, transforms=[],
            brush=ui.Brush(default_size=24, colors=['#ffffff'], color_mode=['fixed']),
            eraser=ui.Eraser(default_size=24), sources=['upload', 'webcam'])
        
        output_inpaint = ui.Gallery(preview=True, show_label=False, object_fit="contain", height="50vh", show_share_button=False, visible=False)  
        prompt_inpaint = ui.Textbox(label="What to change:", placeholder=spholder1)
        prompt_example = ui.Examples(label="Enhance keywords:", examples=['highly detailed face', 'detailed girl face', 'detailed man face', 'detailed hand'], inputs=[prompt_inpaint])
        smart_inpaint = ui.Dropdown(label=ssmart, choices=['Disabled', 'Fusion'], value='Disabled', filterable=False)
                
        with ui.Row():
            clear_inpaint = ui.ClearButton(value="Reset", components=[input_inpaint, output_inpaint, prompt_inpaint])
            submit_inpaint = ui.Button("Submit", variant="primary")
            retry_inpaint = ui.Button("Try Again", variant="primary", visible=False)

    process_inpaint = submit_inpaint.click(fn=submit, inputs=[input_inpaint, prompt_inpaint, smart_inpaint], outputs=[input_inpaint, output_inpaint, submit_inpaint, retry_inpaint, output_inpaint])
    prompt_inpaint.submit(fn=submit, inputs=[input_inpaint, prompt_inpaint, smart_inpaint], outputs=[input_inpaint, output_inpaint, submit_inpaint, retry_inpaint, output_inpaint])
    clear_inpaint.click(fn=reset, inputs=None, outputs=[input_inpaint, output_inpaint, submit_inpaint, retry_inpaint])
    retry_inpaint.click(fn=reset, inputs=None, outputs=[input_inpaint, output_inpaint, submit_inpaint, retry_inpaint])
    
if __name__ == "__main__":
    print(css+adj)
    stella.queue(default_concurrency_limit=100).launch(inbrowser=True, favicon_path="favicon.ico")
    