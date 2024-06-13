import os

mode = {
    'generate'  : os.getenv('generate'),
    'remix'     : os.getenv('remix'),
    'describe'  : os.getenv('describe'),
    'upscale'   : os.getenv('upscale'),
    'inpaint'   : os.getenv('inpaint'),
    'variate'   : os.getenv('variate'),
    'bgremove'  : os.getenv('bgremove'),
    'eraser'    : os.getenv('eraser'),
    'fusion'    : os.getenv('fusion'),
    'story'    : os.getenv('story'),
    'expander'  : os.getenv('expander')
}

head = {
    'bearer'    : os.getenv('bearer')
}