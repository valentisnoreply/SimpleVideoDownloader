from __future__ import annotations

import atexit
import hashlib
import socket
from tkinter import messagebox

import customtkinter as ctk

from controller import AppController


class SingleInstanceGuard:
    def __init__(self, app_id: str) -> None:
        digest = hashlib.sha1(app_id.encode("utf-8")).hexdigest()
        self._port = 42000 + (int(digest[:4], 16) % 2000)
        self._socket: socket.socket | None = None

    def acquire(self) -> bool:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", self._port))
            sock.listen(1)
        except OSError:
            sock.close()
            return False
        self._socket = sock
        return True

    def release(self) -> None:
        if self._socket is None:
            return
        try:
            self._socket.close()
        except OSError:
            pass
        self._socket = None


def main() -> None:
    guard = SingleInstanceGuard("SimpleVideoDonwloader")
    if not guard.acquire():
        messagebox.showwarning(
            "SimpleVideoDonwloader",
            "O SimpleVideoDonwloader ja esta em execucao.",
        )
        return

    atexit.register(guard.release)
    root = ctk.CTk()
    AppController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
