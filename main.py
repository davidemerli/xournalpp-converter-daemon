from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import subprocess
import click
import time
import os


def update_pdf(event):
    """
    Takes a event from watchdog Observer, with a .xopp file, then calls
    `xournalpp FILE.xopp -p FILE.pdf`

    where FILE is obtained from the event

    TODO: currently invoked twice for every file update, and whilst it is not that cpu intensive,
    it is not intended behaviour and is not very clean.
    """

    path = event.src_path

    pdf_path = os.path.splitext(path)[0] + '.pdf'

    print(path, '->', pdf_path)

    subprocess.run(['xournalpp', path, '-p', pdf_path])


@click.command()
@click.option('--path', default='/home', show_default=True, help='Base path where file changes will be detected')
@click.option('--recursive', default=True, show_default=True, help='Detect recursively')
def main(path, recursive):
    # look for every .xopp file update
    patterns = ["*.xopp"]
    # avoid looking for autosave files
    ignore_patterns = ['*.autosave.xopp']
    ignore_directories = True
    case_sensitive = False

    # setup EventHandler
    my_event_handler = PatternMatchingEventHandler(
        patterns,
        ignore_patterns,
        ignore_directories,
        case_sensitive
    )

    # setup events
    my_event_handler.on_created = update_pdf
    my_event_handler.on_modified = update_pdf

    # setup observer
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=recursive)

    my_observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()


if __name__ == "__main__":
    main()
