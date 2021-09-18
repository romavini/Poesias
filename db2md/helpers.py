import traceback
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException,
)
import os
from dotenv import load_dotenv


def get_env(info_name):
    """Return an information stored in dotenv"""
    load_dotenv()
    return os.getenv(info_name)


def print_message(status: str, text: str, message_type: str = "n"):
    """Print message.

    Keyword argument: \n
    status -- message type \n
    text -- text of message \n
    message_type -- type of message print. can be 'e' for error, 's' for
    success, and 'n' for notification.
    """
    if message_type == "e":
        message_color = "\033[91m"
        eom = ""
    elif message_type == "s":
        message_color = "\033[32m"
        eom = "\n"
    elif message_type == "n":
        message_color = "\033[33m"
        eom = ""

    print(
        "["
        + message_color
        + f"{status}"
        + "\033[0m"
        + "]"
        + message_color
        + " -> "
        + "\033[0m"
        + f"{text}{eom}"
    )


def exception_handler(func):
    def wrapper(*args, **kwargs):
        res = None
        exception_raised = 1

        try:
            res = func(*args, **kwargs)
        except NoSuchElementException:
            print_message(
                "NoSuchElementException",
                f"\n{traceback.format_exc()}",
                "e",
            )
        except WebDriverException:
            print_message(
                "WebDriverException",
                f"\n{traceback.format_exc()}",
                "e",
            )
        except KeyError:
            print_message(
                "KeyError",
                f"Error in track info.\n{traceback.format_exc()}",
                "e",
            )
        except TypeError:
            print_message(
                "TypeError",
                f"Error in track info.\n{traceback.format_exc()}",
                "e",
            )
        except ConnectionResetError:
            print_message(
                "ConnectionResetError",
                f"Connection reset by peer.\n{traceback.format_exc()}",
                "e",
            )
        except ConnectionError:
            print_message(
                "ConnectionError",
                f"Connection aborted.\n{traceback.format_exc()}",
                "e",
            )
        except KeyboardInterrupt:
            print_message(
                "KeyboardInterrupt",
                "Step stopped by user.",
                "e",
            )
            exception_raised = 2
        else:
            exception_raised = 0

        return res, exception_raised

    return wrapper
