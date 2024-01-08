import json
import os
import urllib.parse

import args_manager
import modules.config

from PIL import Image

from modules.metadata import save_metadata
from modules.util import generate_temp_filename, get_help_html

from bluemoon.utils.logly import logly

log_cache = {}

global folder_log

def get_help():
    local_troubleshoot = get_help_html(folder=modules.config.path_help)
    troubleshoot = os.path.join(os.path.dirname(local_troubleshoot), 'troubleshoot.html')
    return troubleshoot


def get_current_html_path():
    date_string, local_temp_filename, only_name = generate_temp_filename(folder=modules.config.path_outputs,
                                                                         extension='png')

    html_name = os.path.join(os.path.dirname(local_temp_filename), 'log.html')
    return html_name


def log(img, dic,seed=0):
    if args_manager.args.disable_image_log:
        return
    date_string, local_temp_filename, only_name = generate_temp_filename(seed,folder=modules.config.path_outputs,
                                                                         extension='png')
    save_metadata(os.path.abspath(f'./outputs/{date_string}/metadata.json'), dic)
    folder_log = date_string
    os.makedirs(os.path.dirname(local_temp_filename), exist_ok=True)
    Image.fromarray(img).save(local_temp_filename)
    html_name = os.path.join(os.path.dirname(local_temp_filename), 'log.html')

    css_styles = (
        "<style>"
        "body { background-color: #121212; color: #E0E0E0; } "
        ".container { max-width: 1200px; margin: 0 auto; padding: 20px; box-sizing: border-box; }"
        ".gallery { display: flex; flex-wrap: wrap; justify-content: space-around; }"
        ".image-container { margin: 10px; text-align: center; width: calc(25% - 70px); cursor: pointer; overflow: hidden; border: 1px solid #4d4d4d; border-radius: 10px; transition: transform 0.3s ease-in-out; }"
        ".image-container:hover { transform: scale(1.05); }"
        ".image-container img { max-width: 100%; height: auto; max-height: 200px; border-radius: 10px 10px 0 0; object-fit: cover; }"
        ".image-container div { text-align: center; padding: 4px; background-color: rgba(0, 0, 0, 0.8); color: #FFF; position: absolute; bottom: 0; left: 0; right: 0; border-radius: 0 0 10px 10px; display: none; }"
        ".image-container:hover div { display: block; }"
        "a { color: #BB86FC; } "
        ".metadata { border-collapse: collapse; width: 100%; } "
        ".metadata .key { width: 15%; } "
        ".metadata .value { width: 85%; font-weight: bold; } "
        ".metadata th, .metadata td { border: 1px solid #4d4d4d; padding: 4px; } "
        ".modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.7); } "
        ".modal-content { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: #333; color: #FFF; padding: 20px; z-index: 1000; } "
        ".modal .close { position: absolute; top: 10px; right: 10px; cursor: pointer; color: #FFF; font-size: 20px; } "
        "hr { border-color: gray; } "
        "button { background-color: black; color: white; border: 1px solid grey; border-radius: 5px; padding: 5px 10px; text-align: center; display: inline-block; font-size: 16px; cursor: pointer; } "
        "button:hover { background-color: grey; color: black; } "
        "</style>"
        "<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC\" crossorigin=\"anonymous\">"
    )

    js = (
        """<script>
        function to_clipboard(txt) { 
        txt = decodeURIComponent(txt);
        if (navigator.clipboard && navigator.permissions) {
            navigator.clipboard.writeText(txt)
        } else {
            const textArea = document.createElement('textArea')
            textArea.value = txt
            textArea.style.width = 0
            textArea.style.position = 'fixed'
            textArea.style.left = '-999px'
            textArea.style.top = '10px'
            textArea.setAttribute('readonly', 'readonly')
            document.body.appendChild(textArea)
            textArea.select()
            document.execCommand('copy')
            document.body.removeChild(textArea)
        }
        alert('Copied to Clipboard!\\nPaste to prompt area to load parameters.\\nCurrent clipboard content is:\\n\\n' + txt);
        }

        function showModal(id) {
            var modal = document.getElementById(id);
            modal.style.display = 'block';
        }

        function closeModal(id) {
            var modal = document.getElementById(id);
            modal.style.display = 'none';
        }
        </script>"""
    )

    i = 1
    begin_part = f"<html><head><title>BlueMoon AI Log {date_string}</title>{css_styles}</head><body>{js}<p>BlueMoon AI Log {date_string} (private)</p>\n<p>All images are clean, without any hidden data/meta, and safe to share with others.</p><!--BlueMoon AI-log-split-->\n\n"
    end_part = f'\n<!--BlueMoon AI-log-split--></body></html>'

    middle_part = log_cache.get(html_name, "")

    if middle_part == "":
        if os.path.exists(html_name):
            existing_split = open(html_name, 'r', encoding='utf-8').read().split('<!--BlueMoon AI-log-split-->')
            if len(existing_split) == 3:
                middle_part = existing_split[1]
            else:
                middle_part = existing_split[0]

    div_name = only_name.replace('.', '_')
    item = f"<div class=\"container\">\n"  # Added container class
    item += f"<div class=\"gallery\">"
    item += f"<div class=\"image-container\">\n"
    item += f"<a onclick=\"showModal('{i}')\"><img src='{only_name}' onerror=\"this.closest('.image-container').style.display='none';\" loading='lazy' title='{only_name}'></img></a><div>{only_name}</div>"
    item += f"</div>\n"

    item += "</div>\n"

    item += f"""
                  <div id="{i}" class="modal">
                    <div class="modal-content">
                        <div class="close" onclick="closeModal('{i}')">&times;</div>
                        <h5 class="modal-title">Modal title</h5>
                        <div class="modal-body">
        """
    for key, value in dic:
        item += "<table class='metadata'>"
        value_txt = str(value).replace('\n', ' </br> ')
        item += f"<tr><td class='key'>{key}</td><td class='value'>{value_txt}</td></tr>\n"
        item += "</table>"
    item += f"""    

          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" onclick="closeModal('{i}')">Close</button>
            <button type="button" class="btn btn-primary" onclick="to_clipboard('{urllib.parse.quote(json.dumps({k: v for k, v in dic}, indent=0), safe='')}')">Copy to Clipboard</button>
          </div>
        </div>
      </div>
    </div>
    """
    i += 1

    item += "</div>\n\n"  # Closing container

    middle_part = item + middle_part

    with open(html_name, 'w', encoding='utf-8') as f:
        f.write(begin_part + middle_part + end_part)

    logly.info(f'Image generated with private log at: {html_name}')

    log_cache[html_name] = middle_part

    return
