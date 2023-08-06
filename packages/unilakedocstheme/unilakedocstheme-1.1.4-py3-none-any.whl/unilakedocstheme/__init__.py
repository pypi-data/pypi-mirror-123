from unilakedocstheme import ext
from . import page_context, paths,version
__version__ = version.version_info.version_string()


def setup(app):
    ext.setup(app)
    page_context.setup(app)
    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        'version': __version__,
    }
