import gradio as ui; from datetime import datetime; import logging, requests, json, random
from modules.service_endpoints import *; import numpy as np

# enable debug
logging.basicConfig(level=logging.DEBUG)

# global theme
theme = ui.themes.Default(
    font=[ui.themes.GoogleFont('Myriad Pro')], font_mono=[ui.themes.GoogleFont('Myriad Pro')],
    text_size=ui.themes.Size(lg="18px", md="18px", sm="18px", xl="18px", xs="18px", xxl="18px", xxs="18px"),
    primary_hue='rose', secondary_hue='rose', neutral_hue='zinc')

# global locale - english
success         = 'That worked successfully!'
single_error    = 'That did not work!'
queue_error     = 'Some images cannot be processed!'
empty_error     = 'Prompt field cannot be empty!'
pf_error        = 'Prompt fusion error. Proceeding...'
pe_error        = 'Prompt expansion error. Proceeding...'
pe_cmd          = '(Important Instruction: The prompt must intricately describe every part of the image in concrete, objective detail. THINK about what the end goal of the description is, and extrapolate that to what would make satisfying images.)'
received        = 'Request Received'
timed           = 'Request Timeout'
rejected        = 'Request Error/Rejected'
complete        = 'Request Completed'
liability       = 'STELLA can make mistakes and inaccuracies.'
rights          = '© 2023-2024 Ikmal Said. All rights reserved.'
spholder        = 'Imagine a person, place or anything!'
spholder1       = 'Elements to add into the image!'
spholder2       = 'Things to get rid of!'
spholder3       = 'Put wonders into the generated prompt!'
sprompt         = 'Generate images of:'
sprompt1        = 'Based on image, create:'
sprompt2        = 'Based on image, it shows:'
smodel          = 'Using the AI model:'
smode           = 'Using the mode:'
sratio          = 'In the size of:'
sstyle          = 'Inspired by the style of:'
squality        = 'At a quality level of:'
snumber         = 'With a quantity of:'
ssmart          = 'Using SmartPrompt™ mode:'

# global function
def timestamp():        return f"[{datetime.now().strftime('%d/%m/%y at %H:%M:%S')}]"
def receive():          return f"{timestamp()} \U0001F680 {received}"
def timeout():          return f"{timestamp()} \U000023F0 {timed}"
def reject():           return f"{timestamp()} \U0000274C {rejected}"
def done():             return f"{timestamp()} \U0001F618 {complete}"
def header(feature):    ui.HTML(f'<center><h4 style="font-size: 1em; margin: 5px 0px 5px">{feature}</h4></center>')
def footer():           ui.HTML(f'<center><h4 style="font-size: 1em; margin: 5px 0px 0px">{liability}<br></h4>{rights}</center>')
def title(feature):     return f"{feature}"

# seed generator
max_seed = np.iinfo(np.int32).max

def seeds(a, i: ui.SelectData):
    print(f"Seed mode: {a}")
    if i.value == 'Fixed': return ui.Slider(value=random.randint(0, max_seed), visible=True)
    else: return ui.Slider(visible=False)
    
# prompt fusion to en
def translate(fusion, progress=ui.Progress()):
    progress(0.05, desc="Initiating fusion")
    try: print(f"{receive()} -> {fusion}"); return requests.get(f"{mode['fusion']}{fusion}", timeout=15).json()[0][0]
    except Exception as e: print(pf_error, e); return fusion

# prompt expander
def expand(expand, progress=ui.Progress()):
    progress(0.10, desc="Initiating expansion")
    # return str(input)
    head = {'Content-Type': 'application/json'}
    body = json.dumps({"sentence": f"{expand} {pe_cmd}", "target_word_count": 30})
    # body = json.dumps({"topic": input, "word_count": 30, "writing_mode": "Simple", "story_genre": "Descriptive"}) # ['story']
    try: print(f"{receive()} -> {expand}"); return requests.post(url=mode['expander'], headers=head, data=body, timeout=15).json()['expanded_sentence']
    except Exception as e: print(pe_error, e); return expand

# global head script
jsx = '''
<script>
    window.onbeforeunload = function (event) {
        event.returnValue = "Are you sure you want to leave?";
    };
</script>
'''

# specific css modifiers
adj = '''
/* remove layers button */
.layer-wrap.svelte-g7pfx4.svelte-g7pfx4 {
    display: none !important;
}
'''

adj2 = '''
.grid-wrap.svelte-hpz95u.svelte-hpz95u {
    height: 49.8vh;
}
'''

adj3 = '''
/* tab patches */
.tab-nav.svelte-1uw5tnk {
    justify-content: space-around;
    padding: 10px;
}

button.svelte-1uw5tnk {
    margin-bottom: 0px;
    padding: 10px;
    width: 192px;
    border-radius: var(--container-radius);
}
'''
adj4 = '''
/* carousel patches */
.embla.svelte-a675k2.svelte-a675k2 {
    --slide-size: 100%;
    --slide-height: 50vh;
    padding: 0px;

.embla__slide__img.svelte-a675k2.svelte-a675k2 {
    object-fit: contain;
}

.preview.svelte-a675k2.svelte-a675k2 {
    background: #000000b5;
'''

# global css modifiers
css = '''
/* remove scrollbars */
::-webkit-scrollbar {
  display: none;
}

::-webkit-scrollbar-button {
  display: none;
}

body {
  -ms-overflow-style: none;
}

/* remove footer */
footer {
    display: none !important;
}

/* remove all padding */
.app.svelte-182fdeq.svelte-182fdeq {
    padding: 0px;
}

/* remove scroll bar in gallery */
.grid-wrap.svelte-hpz95u.svelte-hpz95u {
    overflow-y: auto;
}

/* remove background */
gradio-app {
    background: #27272a !important;
}

/* remove borders for tabs*/
div.svelte-iyf88w {
    border: 0px;
}

/* remove padding for tabs */
div.svelte-19hvt5v {
    padding: 0px;
    border: 0px;
}

/* remove borders for tab button bottom*/
.tab-nav.svelte-1uw5tnk {
    border: 0px;
}

/* remove borders for tab button*/
button.svelte-1uw5tnk {
    border: 0px;
}

/* modify container padding and bg */
.hide-container.svelte-90oupt {
    padding: var(--block-padding);
    background: var(--block-background-fill);
}

/* set brush to red */
span.svelte-btgkrd {
    background: rgb(255 0 0 / 60%);
}

/* remove example symbol */
svg.svelte-13hsdno.svelte-13hsdno.svelte-13hsdno {
    display: none;
}

/* replace selected tab color */
.selected.svelte-1uw5tnk {
    background: #27272a;
}

/* justify textbox */
input.svelte-1f354aw.svelte-1f354aw,
textarea.svelte-1f354aw.svelte-1f354aw {
    text-align: justify;
}

/* modify feature text */
label.float.svelte-1b6s6s {
    padding-left: 10px;
    padding-top: 6px;
}

/* change feature background */
label.svelte-1b6s6s {
    background: #27272a;
}

/* remove feature icon */
span.svelte-1b6s6s {
    display: none;
}

/* remove options line */
div.svelte-sfqy0y {
    background: none;
}

/* modify layer button */
.layer-wrap.svelte-g7pfx4.svelte-g7pfx4 {
    background: #27272a;
}

/* modify slider color */
.dark, .light {
    --slider-color: var(--color-accent);
}

/* chanhe num input padding and height */
input[type="number"].svelte-pjtc3.svelte-pjtc3 {
    padding: var(--checkbox-label-padding);
    height: 45px;
}

/* disable anti-aliasing on gallery thumb */
.thumbnail-lg.svelte-hpz95u>img {
    image-rendering: auto;
}

/* disable anti-aliasing on gallery view */
.image-button.svelte-hpz95u img {
    image-rendering: auto;
}

/* make gallery buttons bigger */
.icon-buttons.svelte-hpz95u.svelte-hpz95u,
.icon-buttons.svelte-a675k2.svelte-a675k2 {
    scale: 2;
    padding-top: 8px;
    padding-right: 15px;
}

/* make img clear btn bigger */
div.svelte-s6ybro {
    scale: 2;
    padding-right: 5px;
    padding-top: 5px;
}

/* make img dload btn bigger */
.icon-buttons.svelte-1l6wqyv {
    top: 8px;
    right: 8px;
    scale: 2;
    padding-right: 5px;
    padding-top: 5px;
}

/* remove bg completely */
body {
   background: none !important;
}

/* wide mode */
.app.svelte-182fdeq.svelte-182fdeq {
    max-width: 100% !important;
}

/* make prompt consistant */
label.svelte-1f354aw.svelte-1f354aw {
    padding: 12px;
}

/* remove accord label */
.label-wrap.open.svelte-s1r2yt {
    display: none;
}

/* make empty gallery taller */
.unpadded_box.svelte-1oiin9d,
.unpadded_box.svelte-3w3rth {
    min-height: 51.3vh;
}

/* make image contain */
.image-frame.svelte-rrgd5g img {
    object-fit: contain;
}

/* make thumb and progress curved */
.progress-bar.svelte-12bm2fk.svelte-12bm2fk,
.progress-bar-wrap.svelte-12bm2fk.svelte-12bm2fk,
.thumbnail-item.svelte-hpz95u.svelte-hpz95u,
.thumbnail-small.svelte-hpz95u.svelte-hpz95u,
.thumbnail-small.selected.svelte-hpz95u.svelte-hpz95u {
    border-radius: var(--radius-sm) !important;
}

'''