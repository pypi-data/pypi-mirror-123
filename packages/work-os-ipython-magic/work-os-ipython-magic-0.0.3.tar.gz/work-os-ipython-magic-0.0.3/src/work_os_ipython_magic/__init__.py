"""Work OS IPython magic"""
__version__ = '0.0.1'

from .work_os_magic import WorkOsMagic

# In order to actually use these magics, you must register them with a
# running IPython.

def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    # This class must then be registered with a manually created instance,
    # since it holds custom state.
    magic = WorkOsMagic(ipython)
    ipython.register_magics(magic)
