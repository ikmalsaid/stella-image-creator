from modules.engine_anime import *
feature = 'Text-to-Image - Anime'
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
        result_anime = ui.Gallery(show_label=False, object_fit="contain", height="50vh", show_share_button=False)  
        prompt_anime = ui.Textbox(label=sprompt, placeholder=spholder)
        with ui.Row():
            clear_anime = ui.ClearButton(value="Reset", components=[result_anime, prompt_anime])
            submit_anime= ui.Button("Submit", variant="primary")
      
        with ui.Accordion('More options'):
            style_anime = ui.Dropdown(label=sstyle, choices=list(stella_anime.keys()), value='None', filterable=False)
            model_anime = ui.Dropdown(label=smodel, choices=list(ckpt_anime.keys()), value='Rev Animated', filterable=False)
            ratio_anime = ui.Dropdown(label=sratio, choices=list(ratio.keys()), value='Square (1:1)', filterable=False)
            quality_anime = ui.Dropdown(label=squality, choices=quality, value='Enhanced', filterable=False)
            smart_anime = ui.Dropdown(label=ssmart, choices=['Disabled', 'Fusion'], value='Disabled', filterable=False)
            with ui.Row():
                seedtype_anime = ui.Dropdown(label='Seed type:', choices=['Randomized', 'Fixed'], value='Randomized', filterable=False)
                seedno_anime = ui.Number(label='Seed value:', value=0, minimum=0, maximum=max_seed, visible=False)

    process_anime = submit_anime.click(fn=queue_anime, inputs=[prompt_anime, model_anime, style_anime, ratio_anime, quality_anime, smart_anime, seedtype_anime, seedno_anime], outputs=[result_anime, result_anime])
    prompt_anime.submit(fn=queue_anime, inputs=[prompt_anime, model_anime, style_anime, ratio_anime, quality_anime, smart_anime, seedtype_anime, seedno_anime], outputs=[result_anime, result_anime])
    seedtype_anime.select(fn=seeds, inputs=seedtype_anime, outputs=seedno_anime)

if __name__ == "__main__":
    stella.queue(default_concurrency_limit=100).launch(inbrowser=True, favicon_path="favicon.ico")