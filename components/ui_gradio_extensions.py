# based on https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/v1.6.0/modules/ui_gradio_extensions.py

import os
import gradio as gr
import args_manager

from modules.localization import localization_js


GradioTemplateResponseOriginal = gr.routes.templates.TemplateResponse

modules_path = os.path.dirname(os.path.realpath(__file__))
script_path = os.path.dirname(modules_path)


def webpath(fn):
    if fn.startswith(script_path):
        web_path = os.path.relpath(fn, script_path).replace('\\', '/')
    else:
        web_path = os.path.abspath(fn)

    return f'file={web_path}?{os.path.getmtime(fn)}'


def javascript_html():
    script_js_path = webpath('assets/js/script.js')
    context_menus_js_path = webpath('assets/js/contextMenus.js')
    localization_js_path = webpath('assets/js/localization.js')
    zoom_js_path = webpath('assets/js/zoom.js')
    edit_attention_js_path = webpath('assets/js/edit-attention.js')
    viewer_js_path = webpath('assets/js/viewer.js')
    image_viewer_js_path = webpath('assets/js/imageviewer.js')
    analytics_js_path = webpath('assets/js/analytics.js')
    notice_js_path = webpath('assets/js/notice.js')

    head = f'<script type="text/javascript">{localization_js(args_manager.args.language)}</script>\n'
    head += f'<script type="text/javascript" src="{script_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{context_menus_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{localization_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{zoom_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{edit_attention_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{viewer_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{image_viewer_js_path}"></script>\n'

   # head += f'<script type="text/js" src="{analytics_js_path}"></script>\n'
    #head += f'<script type="text/js" src="{notice_js_path}"></script>\n'

    if args_manager.args.theme:
        head += f'<script type="text/js">set_theme(\"{args_manager.args.theme}\");</script>\n'

    return head


def css_html():
    style_css_path = webpath('assets/css/style.css')
    custom_css_path = webpath('assets/css/custom.css')
    head = f'<link rel="stylesheet" property="stylesheet" href="{style_css_path}">'
   # head += f'<link rel="stylesheet" property="stylesheet" href="{custom_css_path}">'

    return head


def reload_javascript():
    js = javascript_html()
    css = css_html()

    def template_response(*args, **kwargs):
        res = GradioTemplateResponseOriginal(*args, **kwargs)
        res.body = res.body.replace(b'</head>', f'{js}</head>'.encode("utf8"))
        res.body = res.body.replace(b'</body>', f'{css}</body>'.encode("utf8"))
        res.init_headers()
        return res

    gr.routes.templates.TemplateResponse = template_response