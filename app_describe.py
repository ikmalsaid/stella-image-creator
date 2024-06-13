from modules.engine_describe import *
feature = 'Prompt Generator'
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
        input_describe = ui.Image(type='pil', show_label=False, height="40vh", sources=['upload'])
        output_describe = ui.Textbox(label=sprompt2, placeholder='Upload an image to see the prompt!', lines=1)
        
        with ui.Row():
            ui.ClearButton(value="Reset", components=[input_describe, output_describe])
            submit_describe = ui.Button("Submit", variant="primary")
            
    process_describe = submit_describe.click(fn=describe, inputs=[input_describe], outputs=[output_describe])
    input_describe.upload(fn=describe, inputs=[input_describe], outputs=[output_describe])

if __name__ == "__main__":
    stella.queue(default_concurrency_limit=100).launch(inbrowser=True, favicon_path="favicon.ico")