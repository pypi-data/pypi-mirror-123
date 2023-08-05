import traceback
import datetime
import os
from tkinter import messagebox as mb

ERROR_LOG_DIR = "errors"


def log_exception(show_dialog: bool = True) -> str:
    """
    In the event of an exception, this method writes the stacktrace
    out to a file in the "errors" directory (created if not exists)
    And shows a dialog alerting the user of the error (if enabled)
    :param show_dialog: If the dialog box should be shown, informing the user of the error
    :return: the path to the error log file.
    """
    if not os.path.isdir(ERROR_LOG_DIR):
        os.makedirs(ERROR_LOG_DIR)

    current_ts = str(datetime.datetime.now()).replace(":", "-")

    filename = os.path.join(ERROR_LOG_DIR, current_ts + ".log")
    with open(filename, 'w') as f:
        f.write("Datetime:\n")
        f.write(current_ts)

        f.write("\n\nStack Traceback:\n")
        f.write(traceback.format_exc())

    if show_dialog:
        mb.showwarning(
            'Something went wrong!',
            'An unexpected error occurred while running the application.\n'
            'A log was created and was saved as "{}"\n'
            'Please send this to the development team ASAP so we can prevent this error from reoccurring'.format(
                filename
            )
        )

    return filename
