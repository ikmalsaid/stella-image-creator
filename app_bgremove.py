from modules.engine_bgremove import *
feature = 'Background Remover'
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
        input_bgremove = ui.Image(type='pil', show_label=False, sources=['upload'], height="40vh")
        output_bgremove = ui.Gallery(type='pil', object_fit="cover", height="43.4vh", show_share_button=False, columns=1, rows=1, show_label=False, preview=True)
        
        with ui.Row():
            reset_bgremove = ui.ClearButton(value="Reset", components=[input_bgremove, output_bgremove])
            submit_bgremove = ui.Button("Submit", variant="primary")
    
    process_bgremove = submit_bgremove.click(fn=bgremove, inputs=[input_bgremove], outputs=[output_bgremove])
    input_bgremove.upload(fn=bgremove, inputs=[input_bgremove], outputs=[output_bgremove])

if __name__ == "__main__":
    stella.queue(default_concurrency_limit=100).launch(inbrowser=True, favicon_path="favicon.ico")