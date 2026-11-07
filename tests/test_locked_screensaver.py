"""Mock lock IPC and terminal input; never acquire a real desktop lock."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
MOCK = '''#!/usr/bin/python3
import json,os,pathlib,sys
name=pathlib.Path(sys.argv[0]).name
with open(os.environ["CALL_LOG"],"a") as log:
    log.write(json.dumps([name,*sys.argv[1:]])+"\\n")
if name == "omarchy-shell":
    if sys.argv[1:] == ["lock","isLocked"]:
        print(os.environ.get("MOCK_LOCKED","false"))
    elif sys.argv[1:] == ["lock","idleScreensaver"]:
        print(os.environ.get("MOCK_APPROVAL","ok"))
'''


class LockedScreensaverTests(unittest.TestCase):
    def run_bash(self, program, **settings):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ('omarchy-shell', 'heliosdb-screensaver'):
                target = root / name
                target.write_text(MOCK)
                target.chmod(0o755)
            log = root / 'calls.jsonl'
            env = {**os.environ, 'PATH': f'{root}:/usr/bin', 'CALL_LOG': str(log), **settings}
            result = subprocess.run(['bash', '-c', program], env=env, capture_output=True, text=True, timeout=5)
            calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
            return result, calls

    def launch_command(self):
        source = (PROJECT / 'Service.qml').read_text()
        match = re.search(r'runProcess\(screensaverProcess, "screensaver", (".*")\)', source)
        self.assertIsNotNone(match)
        return json.loads(match[1])

    def dismissal_program(self, key=False, focused=False):
        source = (PROJECT / 'scripts/heliosdb-screensaver').read_text()
        match = re.search(r'  check_dismissed\(\) \{([\s\S]*?)\n  \}', source)
        self.assertIsNotNone(match)
        return f'''read() {{ return {0 if key else 1}; }}
screensaver_in_focus() {{ return {0 if focused else 1}; }}
exit_screensaver() {{ echo DISMISSED; exit 33; }}
set_cursor_hidden() {{ echo cursor-hidden="$1"; }}
check_dismissed() {{{match[1]}
}}
check_dismissed
'''

    def test_unlocked_idle_starts_animation(self):
        result, calls = self.run_bash(self.launch_command())
        self.assertEqual(result.returncode, 0)
        self.assertIn(['heliosdb-screensaver', 'launch'], calls)

    def test_locked_idle_requests_lock_service_approval(self):
        result, calls = self.run_bash(self.launch_command(), MOCK_LOCKED='true')
        self.assertEqual(result.returncode, 0)
        self.assertIn(['omarchy-shell', 'lock', 'idleScreensaver'], calls)
        self.assertNotIn(['heliosdb-screensaver', 'launch'], calls)

    def test_unavailable_or_denied_lock_state_does_not_launch(self):
        for state, approval in [('unknown','ok'), ('true','not-allowed'), ('true','Function not found.')]:
            with self.subTest(state=state, approval=approval):
                result, calls = self.run_bash(self.launch_command(), MOCK_LOCKED=state, MOCK_APPROVAL=approval)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn(['heliosdb-screensaver', 'launch'], calls)

    def test_locked_animation_survives_focus_loss_and_keeps_pointer_visible(self):
        result, _ = self.run_bash(self.dismissal_program(), MOCK_LOCKED='true')
        self.assertEqual(result.returncode, 0)
        self.assertNotIn('DISMISSED', result.stdout)
        self.assertIn('cursor-hidden=false', result.stdout)

    def test_locked_terminal_input_cannot_dismiss_animation(self):
        result, _ = self.run_bash(self.dismissal_program(key=True), MOCK_LOCKED='true')
        self.assertEqual(result.returncode, 0)
        self.assertNotIn('DISMISSED', result.stdout)

    def test_unlocked_focus_loss_and_keypress_still_dismiss(self):
        for key, focused in [(False,False),(True,True)]:
            with self.subTest(key=key, focused=focused):
                result, _ = self.run_bash(self.dismissal_program(key=key, focused=focused))
                self.assertEqual(result.returncode, 33)
                self.assertIn('DISMISSED', result.stdout)

    def test_unlocked_focused_animation_still_hides_pointer(self):
        result, _ = self.run_bash(self.dismissal_program(focused=True))
        self.assertEqual(result.returncode, 0)
        self.assertIn('cursor-hidden=true', result.stdout)


if __name__ == '__main__':
    unittest.main()
