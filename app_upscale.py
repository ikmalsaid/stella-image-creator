from modules.engine_upscale import *
feature = 'Image Upscaler'
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
        input_upscale = ui.Image(type='pil', show_label=False, sources=['upload'], height="40vh")
        output_upscale = ui.Gallery(type='pil', object_fit="cover", height="50vh", show_share_button=False, columns=1, rows=1, show_label=False, preview=True)
        
        with ui.Row():
            ui.ClearButton(value="Reset", components=[input_upscale, output_upscale])
            submit_upscale = ui.Button("Submit", variant="primary")
    
    process_upscale = submit_upscale.click(fn=upscale, inputs=[input_upscale], outputs=[output_upscale])

if __name__ == "__main__":
    stella.queue(default_concurrency_limit=100).launch(inbrowser=True, favicon_path="favicon.ico")