"""Project Short Description (default ini)

Project long description or extended summary goes in here (default ini)
"""

import logging
from pathlib import Path
from termcolor import colored
from beetools.beearchiver import Archiver

_PROJ_DESC = __doc__.split("\n")[0]
_PROJ_PATH = Path(__file__)
_PROJ_NAME = _PROJ_PATH.stem
_PROJ_VERSION = "0.0.1"


class PackageItSampleModule:
    """Class short description one-liner goes here.

    Class multi-liner detail description goes here.
    """

    def __init__(self, p_parent_log_name, p_logger=False, p_verbose=True):
        """Initialize the class

        Parameters
        ----------
        p_parent_log_name : str
            Name of the parent.  In combination witt he class name it will
            form the logger name.
        p_logger : bool, default = False
            Activate the logger
        p_verbose: bool, default = True
            Write messages to the console.

        Returns
        -------

        See Also
        --------

        Notes
        -----

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent
        """
        self.success = True
        if p_logger:
            self.log_name = "{}.{}".format(p_parent_log_name, _PROJ_NAME)
            self.logger = logging.getLogger(self._log_name)
        self.verbose = p_verbose

    def method_1(self):
        """Method short description one-liner goes here.

        Class multi-liner detail description goes here.

        Parameters
        ----------

        Returns
        -------

        See Also
        --------

        Notes
        -----

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent
        """
        print(colored("Testing PackageItSampleModule...", "yellow"))
        return True


def do_examples(p_cls=True):
    """A collection of implementation examples for PackageItSampleModule.

    A collection of implementation examples for PackageItSampleModule. The examples
    illustrate in a practical manner how to use the methods.  Each example
    show a different concept or implementation.

    Parameters
    ----------
    p_cls : bool, default = True
        Clear the screen or not at startup of Archiver

    Returns
    -------

    See Also
    --------

    Notes
    -----

    Examples
    --------
    # No proper doctest (<<<) because it is os dependent
    """
    do_example1(p_cls)
    do_example2(p_cls)


def do_example1(p_cls=True):
    """A working example of the implementation of PackageItSampleModule.

    Example1 illutrate the following concepts:
    1. Bla, bla, bla
    2. Bla, bla, bla

    Parameters
    ----------
    p_cls : bool, default = True
        Clear the screen or not at startup of Archiver

    Returns
    -------

    See Also
    --------

    Notes
    -----

    Examples
    --------
    # No proper doctest (<<<) because it is os dependent
    """
    success = True
    t1_archiver = Archiver(_PROJ_NAME, _PROJ_VERSION, _PROJ_DESC, _PROJ_PATH)
    t1_archiver.print_header(p_cls=p_cls)
    t1_packageitsamplemodule = PackageItSampleModule(_PROJ_NAME)
    t1_packageitsamplemodule.method_1()
    t1_archiver.print_footer()
    return success


def do_example2(p_cls=True):
    """Another working example of the implementation of PackageItSampleModule.

    Example2 illustrate the following concepts:
    1. Bla, bla, bla
    2. Bla, bla, bla

    Parameters
    ----------
    p_cls : bool, default = True
        Clear the screen or not at startup of Archiver

    Returns
    -------

    See Also
    --------

    Notes
    -----

    Examples
    --------
    # No proper doctest (<<<) because it is os dependent
    """
    success = True
    t2_archiver = Archiver(_PROJ_NAME, _PROJ_VERSION, _PROJ_DESC, _PROJ_PATH)
    t2_archiver.print_header(p_cls=p_cls)
    t2_packageitsamplemodule = PackageItSampleModule(_PROJ_NAME)
    t2_packageitsamplemodule.method_1()
    t2_archiver.print_footer()
    return success


if __name__ == "__main__":
    do_examples()
