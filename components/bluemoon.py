# https://bluemoonai.github.io
import platform

import gradio as gr

import bluemoonai_version

python_version = platform.python_version()
gradio_version = gr.__version__

def bluemoon_footer():

    heading_html = "<h1 style='font-size: 36px;'>BlueMoon AI</h1>"
    description_html = (
        "<div style='font-size: 18px;'>"
        "<p>BlueMoon AI is a latent text-to-image diffusion model capable of generating "
        "photo-realistic images given any text input. It cultivates autonomous freedom to produce incredible imagery, "
        "empowering billions of people to create stunning art within seconds.</p>"
        "<br>"
        "Create beautiful images with our AI Image Generator (Text to Image) for free and Open Source."
        "<br>"
        "Let Your Creativity Flow."
        "</div>"
    )
    license_html = (
        "<br><br><p style='font-size: 16px; text-align: center;'>"
        "Licensed under the <a href='https://www.gnu.org/licenses/agpl-3.0.html'>GNU Affero General Public License v3.0</a> "
        "AND <a href='https://github.com/BlueMoonAI/BlueMoonAI/blob/main/LICENSE.md'>Open Rail -m License</a>."
        "</p>"
    )

    footer_html = f"""
        <div style="color: #333; padding: 10px; text-align: center; ">
            <span style="margin-right: 20px;">Website:
                <a style="color: #007bff;" href="https://bluemoonai.github.io" target="_blank">https://bluemoonai.github.io</a>
            </span>
            <span style="margin-right: 20px;">GitHub: 
                <a style="color: #007bff;" href="https://github.com/BlueMoonAI/BlueMoonAI" target="_blank">BlueMoonAI</a>
            </span>
           <span style="margin-right: 20px;">BlueMoon AI:
                <a style="color: #007bff;" href="https://github.com/BlueMoonAI/BlueMoonAI/" target="_blank">v{bluemoonai_version.get_version()}</a>
            </span>
            <span style="margin-right: 20px;">Gradio Version: 
                <a style="color: #007bff;" href="https://github.com/gradio-app/gradio" target="_blank">{gr.__version__}</a>
            </span>
            <span style="margin-right: 20px;">Python Version: 
                <a style="color: #007bff;" href="https://www.python.org/" target="_blank">{platform.python_version()}</a>
            </span>
        </div>
    """

    gr.HTML(value=heading_html)
    gr.HTML(value=description_html)
    gr.HTML(value=license_html)
    gr.HTML(value=footer_html)

def remove_default_watermark():
        watermark_html = ("<style>footer{visibility: hidden}</style>")
        gr.HTML(value=watermark_html)