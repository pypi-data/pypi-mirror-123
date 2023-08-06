from . import config
from . import render
from . import dataclasses


def get_fragment(name, include_html=True, include_markdown=False) -> dataclasses.Fragment:
    fragment = config.db_connection.get_fragment(name)
    if fragment is None:
        return dataclasses.Fragment(
            html="",
            content="",
        )
    if include_html:
        fragment.html = render.render_markdown(fragment.content)
    if not include_markdown:
        fragment.content = ""
    return fragment
