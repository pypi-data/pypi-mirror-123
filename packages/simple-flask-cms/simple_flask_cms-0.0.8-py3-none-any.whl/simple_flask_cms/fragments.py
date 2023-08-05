from . import config
from . import render


def get_fragment(name, include_html=True, include_markdown=False):
    fragment = config.db_connection.get_fragment(name)
    if include_html:
        fragment.html = render.render_markdown(fragment.content)
    if not include_markdown:
        fragment.content = ""
    return fragment
