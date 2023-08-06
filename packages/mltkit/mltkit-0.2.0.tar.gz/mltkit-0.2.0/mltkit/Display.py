# -*- coding: utf-8 -*-

import builtins as __builtin__
from warnings import warn
from time import sleep
from atexit import register as register_exit
import signal

from typing import List, Dict, Union, Optional

# Windows does not support curses(essentially the core of this whole thing).
# This is how we will detect a platform that doesn't support it and handle it
# later if `None` is found.
try:
    import curses
except ImportError:
    curses = None

# Store a reference to the original `print` function for later.
# Once we replace it in `_suppress_print`, we can reset it on exit.
_builtin_print = __builtin__.print
# Again, we will store a reference to the original Python SIGINT
# handler. We are going to override this once we enter our `with`
# block and restore it once __exit__ fires.
_builtin_sigint_handler = signal.getsignal(signal.SIGINT)

# MARK: Type "abbreviations"
_T_notifications = List[Dict[str, Union[str, int]]]

# MARK: Warning flags
_DID_WARN_UNSUPPORTED_OS: Dict[str, bool] = {'value': False}
_DID_WARN_NO_CONTEXT_MANAGER: Dict[str, bool] = {'value': False}


def _suppress_print():
    """
    Suppresses the built-in print for the current process.

    To force printing on a suppressed process, pass
    "force=True" to print().
    """

    def _print(*args, **kwargs):
        force = kwargs.pop('force', False)
        if force:
            _builtin_print(*args, **kwargs)

    if __builtin__.print is _builtin_print:
        __builtin__.print = _print


def _reinstate_print():
    if __builtin__.print is not _builtin_print:
        __builtin__.print = _builtin_print


@register_exit
def exit_display():
    # noinspection PyBroadException
    try:
        _reinstate_print()
        curses.echo()
        curses.nocbreak()
        curses.endwin()
    except Exception:
        pass


def _create_progress_bar(current, total, message, bar_length):
    if current > total:
        raise ValueError('Parameter current can not exceed parameter total.')
    if bar_length < 1:
        raise ValueError('Expected bar length to be greater than 1, '
                         f'but got {bar_length} instead.')
    full_block = chr(9608)
    percent_symbol = '%'
    filled_length = int(round(bar_length * current / float(total)))
    percent = int(100.0 * current / float(total))
    bar = full_block * filled_length
    bar += ' ' * (bar_length - filled_length)
    return f'|{bar}| {percent}{percent_symbol} {message}'


class Display(object):
    __slots__ = [
        '_enabled',
        '_curses_window',
        '_did_warn_no_cm',
        '_is_active',
        '_is_in_with_block',
        '_notifications',
        '_static_items',
        '_bars',
        '_stats',
        '_num_lines',
        '_suppress_print'
    ]

    def __init__(self, enabled: bool = True):

        self._enabled: bool = enabled
        if curses is None and not _DID_WARN_UNSUPPORTED_OS['value']:
            warn('Display is not supported on this platform/OS and will be disabled.',
                 UserWarning, stacklevel=2)
            self._enabled = False
            _DID_WARN_UNSUPPORTED_OS['value'] = True
        # When using this class outside of the context manager "with block"
        # syntax, we are going to warn the user about the potential destruction
        # of their terminal output when incorrectly exiting.
        self._curses_window = None
        self._is_active: bool = False
        self._is_in_with_block: bool = False
        self._notifications: _T_notifications = []
        self._static_items: List[str] = []
        self._bars: List[str] = []
        self._stats: List[str] = []
        self._num_lines: int = 0

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def is_active(self) -> bool:
        return self._is_active

    def push_notification(self, message: str, lifespan: int = 10):
        if not self._enabled:
            return
        self._notifications.append({
            'message': str(message),
            'age': 0,
            'lifespan': lifespan
        })

    def push_static_item(self, value: str):
        if not self._enabled:
            return
        self._static_items.append(value)

    def push_progress_bar(self, current: int, total: int, message: Optional[str] = None,
                          length: int = 50) -> None:
        if not self._enabled:
            return
        if message is None:
            message = ''
        bar: str = _create_progress_bar(current, total, message, length)
        self._bars.append(bar)

    def push_statistic(self, key: str, value: Union[int, float], num_decimals: Optional[int] = None) -> None:
        if not self._enabled:
            return
        if isinstance(value, float) and num_decimals is not None:
            value = round(value, num_decimals)
        self._stats.append(f'{key}: {value}')

    def print_stack(self) -> None:
        if not self._enabled:
            return
        if not self._is_in_with_block and not _DID_WARN_NO_CONTEXT_MANAGER['value']:
            warn(('Using Display outside of a "with" block is not recommended.\n'
                  'This can cause stack traces to be hidden and break the formatting\n'
                  'of your terminal window.'),
                 UserWarning, stacklevel=2)
            sleep(5)
            _DID_WARN_NO_CONTEXT_MANAGER['value'] = True
        self._start_curses()
        self.clear()
        # Add the notifications lines separately as they are
        # not just array<string>
        for i, line in enumerate(self._notifications):
            self._curses_window.addstr(i, 0, line['message'])
            self._notifications[i]['age'] += 1
        # Add all other lines
        lines = self._static_items + self._bars + self._stats
        for i, line in enumerate(lines, start=len(self._notifications)):
            self._curses_window.addstr(i, 0, line)
        # Reset attributes
        self._num_lines = len(self._notifications) + len(lines)
        self._bars = []
        self._stats = []
        self._curses_window.refresh()

    def clear(self) -> None:
        if not self._enabled:
            return
        # Clear lines
        for i in range(self._num_lines):
            self._curses_window.move(i, 0)
            self._curses_window.clrtoeol()
        notifications: _T_notifications = []
        for line in self._notifications:
            if line['age'] < line['lifespan']:
                notifications.append(line)
        self._notifications = notifications

    def __enter__(self) -> 'Display':
        # We use this flag to determine if this class
        # is being used outside of this context manager
        # syntax. If so, we need to warn the user that
        # things might not work right.
        self._is_in_with_block = True
        # While we are inside our with block, we suppress
        # SIGINT to exit keyboard interrupts more gracefully.
        # We will reset this in `__exit__`
        signal.signal(signal.SIGINT, lambda signum, frame: exit(0))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore the builtin Python SIGINT handler
        signal.signal(signal.SIGINT, _builtin_sigint_handler)
        self.exit()
        self._is_in_with_block = False

    def __del__(self):
        # We will call a final exit here in case the display exited unexpectedly.
        # This is a last resort to not break the terminal output.
        self.exit()

    def _start_curses(self) -> None:
        # Suppress outside prints once display is initialized.
        # The default print will be reinstated in exit_display.
        # This should be done for ALL processes, not just slaves.
        if not self._is_active and curses is not None:
            _suppress_print()
            self._curses_window = curses.initscr()
            curses.noecho()
            curses.cbreak()
            self._is_active = True

    def exit(self) -> None:
        if self._is_active:
            exit_display()
            self._is_active = False
