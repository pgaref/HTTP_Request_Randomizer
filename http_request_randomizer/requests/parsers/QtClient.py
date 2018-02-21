import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
#
app = QApplication([])


# def render(source_html):
#     """Fully render HTML, JavaScript and all."""
#
#     class Render(QWebEngineView):
#         def __init__(self, html):
#             self.html = None
#             self.app = app
#             QWebEngineView.__init__(self)
#             self.loadFinished.connect(self._loadFinished)
#             self.setHtml(html)
#             self.app.exec_()
#
#         def _loadFinished(self, result):
#             # This is an async call, you need to wait for this
#             # to be called before closing the app
#             self.page().toHtml(self.callable)
#
#         def callable(self, data):
#             self.html = data
#             # Data has been stored, it's safe to quit the app
#             self.app.quit()
#
#     return Render(source_html).html


import os
import sys
from contextlib import contextmanager
from multiprocessing import Pool

try:
    TimeoutError
except NameError:
    from multiprocessing import TimeoutError  # Python 2


def _render(source_html):
    """Return rendered HTML."""
    from PyQt5.QtCore import QEventLoop
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtWidgets import QApplication

    class Render(QWebEngineView):
        """Render HTML with PyQt5 WebEngine."""

        def __init__(self, html):
            self.html = None
            self.app = app
            QWebEngineView.__init__(self)
            self.loadFinished.connect(self._loadFinished)
            self.setHtml(html)
            while self.html is None:
                self.app.processEvents(
                    QEventLoop.ExcludeUserInputEvents |
                    QEventLoop.ExcludeSocketNotifiers |
                    QEventLoop.WaitForMoreEvents)
            self.app.quit()

        def _callable(self, data):
            self.html = data

        def _loadFinished(self, result):
            self.page().toHtml(self._callable)

    # with devnull():
    return Render(source_html).html


@contextmanager
def devnull():
    """Temporarily redirect stdout and stderr to /dev/null."""

    try:
        original_stderr = os.dup(sys.stderr.fileno())
        original_stdout = os.dup(sys.stdout.fileno())
        null = open(os.devnull, 'w')
        os.dup2(null.fileno(), sys.stderr.fileno())
        os.dup2(null.fileno(), sys.stdout.fileno())
        yield

    finally:
        if original_stderr is not None:
            os.dup2(original_stderr, sys.stderr.fileno())
        if original_stdout is not None:
            os.dup2(original_stdout, sys.stdout.fileno())
        if null is not None:
            null.close()


def render(html):
    """Perform render in a new process to prevent hangs."""

    tries = 3

    for _ in range(tries):
        pool = Pool(2)
        try:
            return pool.apply_async(_render, args=(html,)).get(timeout=10)
            print("really?")
        except TimeoutError:
            print("really? T")
            continue
        finally:
            pool.terminate()

    raise TimeoutError('Timed out attempting to render HTML %d times' % tries)