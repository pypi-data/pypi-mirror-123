"""
The prefix printer factory is based on the tutorial
'Introduction to Decorators' given
by Geir Arne Hjelle at PyCon 21.
Found at: https://www.youtube.com/watch?v=VWZAh1QrqRE&amp;t=17m0s
"""


from click import echo

from confprint import _exceptions, err_print


def prefix_printer(
    prefix: str,
    stderr: bool = False,
    click: bool = False,
    upper: bool = True,
    frame_left: str = "[",
    frame_right: str = "]",
) -> callable:
    """
    Function factory for prefixing text.

    Args:
        prefix (str): The prefix to use.
        stderr (bool, optional):
            If True, the printer will print to sys.stderr instead of sys.stdout
            Defaults to False.
        click (bool, optional): If True, the printer will print to click.echo
            instead of sys.stdout. Defaults to False.
        upper (bool, optional): If True, the prefix will be printed in upper
        frame_left (str, optional): The left frame. Defaults to "[".
        frame_right (str, optional): The right frame. Defaults to "]".

    Returns:
        callable: A function that prints text prefixed with the prefix.
    """
    if upper:
        prefix = f"{frame_left}{prefix.upper()}{frame_right}"
    else:
        prefix = f"{frame_left}{prefix}{frame_right}"

    def prefixed_printer(text: str = "") -> None:
        """
        Prints a message prefixed with a prefix.

        Args:
            text (str): The text to print. Defaults to None.
        """

        if stderr and click:
            raise _exceptions.PropertyError(
                "stderr and click cannot be True at the same time"
            )
        elif stderr:
            # If stderr is True, print to stderr
            print_func = err_print
        elif click:
            print_func = echo
        else:
            # If stderr and click are False, print to stdout
            print_func = print

        if "\n" in text:
            lines = text.split("\n")
            first_line_len = len(lines[0])
            lines[0] = f"{prefix}: {lines[0]}"
            indent_len = len(lines[0]) - first_line_len
            print_func(lines[0])
            [print_func((" " * indent_len) + line) for line in lines[1:]]

        elif not text:
            print_func(f"{prefix}")
        else:
            print_func(f"{prefix}: {text}")

    return prefixed_printer
