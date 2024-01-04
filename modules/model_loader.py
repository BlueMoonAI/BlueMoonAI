import os
from urllib.parse import urlparse
from typing import Optional

from bluemoon.utils.logly import logly
from components.html import make_progress_html


def load_file_from_url(
        url: str,
        *,
        model_dir: str,
        progress: bool = True,
        file_name: Optional[str] = None,
) -> str:
    """Download a file from `url` into `model_dir`, using the file present if possible.

    Returns the path to the downloaded file.
    """
    os.makedirs(model_dir, exist_ok=True)
    if not file_name:
        parts = urlparse(url)
        file_name = os.path.basename(parts.path)
    cached_file = os.path.abspath(os.path.join(model_dir, file_name))
    if not os.path.exists(cached_file):
        logly.info(f'Downloading: "{file_name}" to {cached_file}\n')
        try:
            from torch.hub import download_url_to_file
            make_progress_html(0, f'Downloading: "{file_name}"')
            download_url_to_file(url, cached_file, progress=progress)
        except Exception as e:
            logly.error(f'Failed to download "{file_name}" to {cached_file}: {e}')
    return cached_file
