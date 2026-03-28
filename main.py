from __future__ import annotations

import sys
from typing import Callable, Optional

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QGridLayout, QLineEdit, QPushButton, QWidget

_OPS: dict[str, Callable[[np.floating, np.floating], np.floating]] = {
    "+": np.add,
    "-": np.subtract,
    "*": np.multiply,
    "/": np.divide,
}


def _fmt(value: np.floating) -> str:
    f = float(value)
    if np.isfinite(f) and f == int(f) and abs(f) < 1e15:
        return str(int(f))
    return f"{f:.10g}"


class Calculator(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("電卓")

        self._display = QLineEdit("0")
        self._display.setReadOnly(True)
        self._display.setAlignment(Qt.AlignmentFlag.AlignRight)

        self._current = "0"
        self._stored: Optional[np.floating] = None
        self._pending: Optional[str] = None
        self._new_entry = True
        self._error = False

        grid = QGridLayout(self)
        grid.addWidget(self._display, 0, 0, 1, 4)

        def add_btn(text: str, row: int, col: int, slot, *, colspan: int = 1) -> None:
            b = QPushButton(text)
            b.clicked.connect(slot)
            grid.addWidget(b, row, col, 1, colspan)

        add_btn("C", 1, 0, self._on_clear, colspan=4)

        digits = [
            ("7", 2, 0),
            ("8", 2, 1),
            ("9", 2, 2),
            ("4", 3, 0),
            ("5", 3, 1),
            ("6", 3, 2),
            ("1", 4, 0),
            ("2", 4, 1),
            ("3", 4, 2),
        ]
        for text, r, c in digits:
            add_btn(
                text,
                r,
                c,
                lambda checked=False, t=text: self._on_digit(t),
            )

        add_btn("/", 2, 3, lambda _c=False: self._on_op("/"))
        add_btn("*", 3, 3, lambda _c=False: self._on_op("*"))
        add_btn("-", 4, 3, lambda _c=False: self._on_op("-"))

        add_btn("0", 5, 0, lambda _c=False: self._on_digit("0"), colspan=2)
        add_btn(".", 5, 2, self._on_dot)
        add_btn("+", 5, 3, lambda _c=False: self._on_op("+"))

        add_btn("=", 6, 0, self._on_equals, colspan=4)

    def _sync_display(self) -> None:
        self._display.setText(self._current)

    def _reset_state(self) -> None:
        self._current = "0"
        self._stored = None
        self._pending = None
        self._new_entry = True
        self._error = False
        self._sync_display()

    def _on_clear(self, _checked: bool = False) -> None:
        self._reset_state()

    def _on_digit(self, d: str) -> None:
        if self._error:
            return
        if self._new_entry:
            self._current = d
            self._new_entry = False
        else:
            if self._current == "0" and d != "0":
                self._current = d
            elif self._current == "0" and d == "0":
                pass
            else:
                self._current += d
        self._sync_display()

    def _on_dot(self, _checked: bool = False) -> None:
        if self._error:
            return
        if self._new_entry:
            self._current = "0."
            self._new_entry = False
        elif "." not in self._current:
            self._current += "."
        self._sync_display()

    def _parse_current(self) -> np.float64:
        if self._current in ("", ".", "-", "-."):
            return np.float64(0.0)
        return np.float64(self._current)

    def _apply(self, left: np.floating, right: np.floating, op: str) -> np.floating:
        if op == "/" and right == 0:
            raise ZeroDivisionError
        return _OPS[op](left, right)

    def _commit_pending(self) -> bool:
        assert self._pending is not None and self._stored is not None
        try:
            right = self._parse_current()
            result = self._apply(self._stored, right, self._pending)
        except ZeroDivisionError:
            self._current = "Error"
            self._error = True
            self._stored = None
            self._pending = None
            self._new_entry = True
            self._sync_display()
            return False
        self._stored = result
        self._current = _fmt(result)
        self._new_entry = True
        self._sync_display()
        return True

    def _on_op(self, op: str) -> None:
        if self._error:
            return
        if not self._new_entry and self._pending is not None and self._stored is not None:
            if not self._commit_pending():
                return
        elif self._new_entry and self._pending is not None and self._stored is not None:
            self._pending = op
            return

        self._stored = self._parse_current()
        self._pending = op
        self._new_entry = True

    def _on_equals(self, _checked: bool = False) -> None:
        if self._error:
            return
        if self._pending is None or self._stored is None:
            return
        if self._new_entry:
            return
        self._commit_pending()
        self._pending = None


def main() -> None:
    app = QApplication(sys.argv)
    win = Calculator()
    win.resize(280, 360)
    win.show()
    raise SystemExit(app.exec())


if __name__ == "__main__":
    main()
