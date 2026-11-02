# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-or-later
import importlib.util
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("app", Path(__file__).resolve().parents[1] / "speak.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class Tests(TestCase):
    def test_shell_metacharacters_remain_literal(self):
        with patch.object(app.shutil, "which", return_value="/usr/bin/espeak-ng"):
            command = app.build_command("Hello; touch /tmp/not-executed", "en")
        self.assertEqual(command[-1], "Hello; touch /tmp/not-executed")
        self.assertEqual(command[:4], ["espeak-ng", "-v", "en", "--"])

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            app.build_command("", "en")
        with self.assertRaises(ValueError):
            app.build_command("Hello", "unknown")

    def test_real_tk_window(self):
        window = app.SpeechApp()
        try:
            self.assertEqual(window.language.get(), "English")
            window.editor.insert("1.0", "Hello")
            self.assertIn("Hello", window.editor.get("1.0", "end"))
        finally:
            window.destroy()
