from modules.engine_eraser import *
feature = 'Image Eraser'
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
        input_eraser = ui.ImageEditor(
            show_label=False, transforms=[],
            brush=ui.Brush(default_size=24, colors=['#ffffff'], color_mode=['fixed']),
            eraser=ui.Eraser(default_size=24), sources=['upload', 'webcam'])
        
        output_eraser = ui.Gallery(preview=True, show_label=False, object_fit="cover", columns=1, rows=1, height="50vh", show_share_button=False, visible=False)                  
        
        with ui.Row():
            clear_eraser = ui.ClearButton(value="Reset", components=[input_eraser, output_eraser])
            submit_eraser = ui.Button("Submit", variant="primary")
            retry_eraser = ui.Button("Try Again", variant="primary", visible=False)

    process_eraser = submit_eraser.click(fn=submit, inputs=[input_eraser], outputs=[input_eraser, output_eraser, submit_eraser, retry_eraser, output_eraser])
    clear_eraser.click(fn=reset, inputs=None, outputs=[input_eraser, output_eraser, submit_eraser, retry_eraser])
    retry_eraser.click(fn=reset, inputs=None, outputs=[input_eraser, output_eraser, submit_eraser, retry_eraser])
    

if __name__ == "__main__":
    stella.queue(default_concurrency_limit=100).launch(inbrowser=True, favicon_path="favicon.ico")