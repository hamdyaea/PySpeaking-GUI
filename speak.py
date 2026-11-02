#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-or-later
"""Speak text locally using a safe, lightweight Tkinter interface."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import ttk

LANGUAGES = {
    "English": "en", "French": "fr", "German": "de",
    "Spanish": "es", "Japanese": "ja", "Chinese": "zh",
    "Italian": "it", "Arabic": "ar", "Russian": "ru",
}


def build_command(text: str, language: str, backend: str | None = None) -> list[str]:
    if not text.strip() or len(text) > 5000:
        raise ValueError("Enter 1 to 5000 characters")
    if language not in LANGUAGES.values():
        raise ValueError("Unsupported language")
    backend = backend or ("espeak-ng" if shutil.which("espeak-ng") else "google_speech")
    if backend not in ("espeak-ng", "google_speech"):
        raise ValueError("Unsupported speech engine")
    if not shutil.which(backend):
        raise FileNotFoundError("Install espeak-ng or google_speech")
    if backend == "espeak-ng":
        return [backend, "-v", language, "--", text]
    return [backend, "-l", language, text]


class SpeechApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("PySpeaking — Hamdy Abou El Anein")
        self.geometry("580x430")
        self.minsize(410, 330)
        self.configure(bg="#101827")
        self.language = tk.StringVar(value="English")
        self.status = tk.StringVar(value="Ready")
        frame = tk.Frame(self, bg="#101827", padx=24, pady=22)
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="PYSPEAKING", font=("DejaVu Sans", 16, "bold"),
                 bg="#101827", fg="#8bd6c1").pack(anchor="w")
        tk.Label(frame, text="Text-to-speech without EasyGUI", bg="#101827",
                 fg="#bac9d9").pack(anchor="w", pady=(0, 14))
        ttk.Combobox(frame, textvariable=self.language, values=list(LANGUAGES),
                     state="readonly").pack(fill="x", pady=6)
        self.editor = tk.Text(frame, height=6, wrap="word", bg="#1b2b42",
                              fg="white", insertbackground="white", padx=10, pady=10)
        self.editor.pack(fill="both", expand=True, pady=12)
        self.button = tk.Button(frame, text="Speak", command=self.play, bg="#7ddcc0",
                                fg="#10211c", relief="flat", padx=20, pady=9)
        self.button.pack(anchor="w")
        tk.Label(frame, textvariable=self.status, bg="#101827", fg="#d1ddeb").pack(
            anchor="w", pady=12)

    def play(self) -> None:
        try:
            command = build_command(self.editor.get("1.0", "end").strip(),
                                    LANGUAGES[self.language.get()])
        except (ValueError, FileNotFoundError) as exc:
            self.status.set(str(exc))
            return
        self.button.config(state="disabled")
        self.status.set("Speaking…")

        def worker() -> None:
            try:
                subprocess.run(command, check=True, timeout=90)
                result = "Finished"
            except (OSError, subprocess.SubprocessError) as exc:
                result = "Playback failed: " + str(exc)
            try:
                self.after(0, lambda: (self.status.set(result),
                                      self.button.config(state="normal")))
            except RuntimeError:
                pass
        threading.Thread(target=worker, daemon=True).start()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Speak text from the terminal")
    parser.add_argument("--language", default="en", choices=list(LANGUAGES.values()))
    args = parser.parse_args()
    if args.text is None:
        SpeechApp().mainloop()
    else:
        subprocess.run(build_command(args.text, args.language), check=True, timeout=90)


if __name__ == "__main__":
    main()
