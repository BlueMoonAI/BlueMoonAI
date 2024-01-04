import gradio as gr

import bluemoonai_version


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
        "Licensed under the <a href='https://opensource.org/licenses/GPL-3.0'>GNU General Public License v3.0</a> "
        "AND <a href='https://github.com/BlueMoonAI/BlueMoonAI/blob/main/LICENSE.md'>Open Rail License</a>."
        "</p>"
    )

    version_html = (f"<p style='font-size: 16px; text-align: center;'><a "
                    f"href='https://github.com/BlueMoonAI/BlueMoonAI/'>BlueMoon AI</a>: v{bluemoonai_version.get_version()}</p>")

    gr.HTML(value=heading_html)
    gr.HTML(value=description_html)
    gr.HTML(value=license_html)
    gr.HTML(value=version_html)