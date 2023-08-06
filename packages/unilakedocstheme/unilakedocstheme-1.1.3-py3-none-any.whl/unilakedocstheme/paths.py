import os.path


def get_pkg_path():
    return os.path.abspath(os.path.dirname(__file__))


def get_html_theme_path():
    """Return the directory containing HTML theme for local builds."""
    return os.path.join(get_pkg_path(), 'theme')


def get_pdf_theme_path(theme='unilakedocs'):
    """Return the directory containing PDF theme for local builds."""
    args = ['theme', theme + '_pdf', 'pdftheme']
    return os.path.join(get_pkg_path(), *args)


def get_theme_logo_path(theme='unilakedocs'):
    """Return the directory containing theme logo for local builds."""
    args = ['theme', theme + '_pdf', 'logo-full.png']
    return os.path.join(get_pkg_path(), *args)


# This function is for compatibility with previous releases.
def get_openstack_logo_path():
    """Return the directory containing OpenStack logo for local builds."""
    return get_theme_logo_path('unilakedocs')
