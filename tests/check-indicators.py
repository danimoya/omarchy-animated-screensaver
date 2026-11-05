#!/usr/bin/env python3
"""Run the real indicator QML offscreen, using synthetic command responses."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[1]
shell = Path(os.environ.get('OMARCHY_PATH', '/usr/share/omarchy')) / 'shell'
with tempfile.TemporaryDirectory(prefix='omarchy-indicator-test-') as folder:
    root = Path(folder)
    for name in ('Ui', 'Commons'):
        (root / name).symlink_to(shell / name, target_is_directory=True)
    shutil.copytree(repo / 'compat/danimoya.indicators/indicators', root / 'indicators')
    runtime = root / 'runtime'
    runtime.mkdir(mode=0o700)
    fixture = root / 'fixture.py'
    fixture.write_text('''import json,sys
from pathlib import Path
p=Path(sys.argv[1]); mode=sys.argv[2]; fmt=sys.argv[3]
value=p.exists()
if mode == 'toggle':
    if value: p.unlink()
    else: p.touch()
elif fmt == 'on-off': print('on' if value else 'off')
else: print(json.dumps({'enabled':value}))
''')
    entries = []
    for name, fmt in [('StayAwake', 'json'), ('Dnd', 'on-off'), ('NightLight', 'json')]:
        command = ['python3', str(fixture), str(root / (name + '.state')), 'status', fmt]
        toggle = command.copy()
        toggle[3] = 'toggle'
        entries.append(f'''Indicators.{name} {{
 id: {name.lower()}
 property var originalCommand: {json.dumps(command)}
 statusCommand: originalCommand
 toggleCommand: {json.dumps(toggle)}
}}''')
    harness = '''import QtQuick
import Quickshell
import "indicators" as Indicators
ShellRoot {
 id: test
 property int phase: 0
 property int ticks: 0
 property var widgets: [stayawake, dnd, nightlight]
 __ENTRIES__
 Timer {
  interval: 100; repeat: true; running: true
  onTriggered: {
   test.ticks++
   if (test.ticks > 250) { console.error("FAIL phase", test.phase); Qt.exit(1); return }
   var known = test.widgets.every(function(w) { return w.stateKnown })
   var allOn = known && test.widgets.every(function(w) { return w.active })
   var allOff = known && test.widgets.every(function(w) { return !w.active })
   if (test.phase === 0 && allOff) {
    test.widgets.forEach(function(w) { w.pressed(Qt.LeftButton) }); test.phase = 1
   } else if (test.phase === 1 && allOn) {
    // Simulate another menu or monitor changing the same underlying state.
    test.widgets.forEach(function(w) { Quickshell.execDetached(w.toggleCommand) }); test.phase = 2
   } else if (test.phase === 2 && allOff) {
    test.widgets.forEach(function(w) { w.statusCommand = ["sh", "-c", "printf invalid"]; w.refresh() }); test.phase = 3
   } else if (test.phase === 3 && test.widgets.every(function(w) { return !w.stateKnown })) {
    if (!test.widgets.every(function(w) { return w.tooltipText.indexOf("unavailable") !== -1 })) {
     console.error("FAIL missing unavailable tooltip"); Qt.exit(1); return
    }
    test.widgets.forEach(function(w) { w.statusCommand = ["sh", "-c", "exit 1"]; w.refresh() }); test.phase = 4
   } else if (test.phase === 4) {
    if (test.widgets.some(function(w) { return w.stateKnown })) { console.error("FAIL command failure"); Qt.exit(1); return }
    test.widgets.forEach(function(w) { w.statusCommand = w.originalCommand; w.refresh() }); test.phase = 5
   } else if (test.phase === 5 && allOff) {
    // A second click cycle checks both directions through each real handler.
    test.widgets.forEach(function(w) { w.pressed(Qt.LeftButton) }); test.phase = 6
   } else if (test.phase === 6 && allOn) {
    test.widgets.forEach(function(w) { w.pressed(Qt.LeftButton) }); test.phase = 7
   } else if (test.phase === 7 && allOff) {
    console.log("PASS: three indicators, clicks, external state, invalid status, command failure, recovery"); Qt.exit(0)
   }
  }
 }
}
'''.replace('__ENTRIES__', '\n'.join(entries))
    (root / 'shell.qml').write_text(harness)
    env = dict(os.environ, QT_QPA_PLATFORM='offscreen', HOME=str(root), XDG_RUNTIME_DIR=str(runtime), NO_COLOR='1')
    result = subprocess.run(['qs', '-p', str(root)], env=env, text=True, capture_output=True, timeout=35)
    output = result.stdout + result.stderr
    if result.returncode or 'PASS:' not in output:
        print(output)
        raise SystemExit(result.returncode or 1)
    print(next(line for line in output.splitlines() if 'PASS:' in line))
