import QtQuick
import Quickshell.Io
import qs.Ui

// Public commands work without access to the host shell's service objects.
BarIndicator {
  id: root
  property var statusCommand: []
  property var toggleCommand: []
  property string statusFormat: "json"
  property bool stateKnown: false
  property bool commandActive: false
  property string enabledTooltip: ""
  property string disabledTooltip: ""

  active: stateKnown && commandActive
  activeTooltipText: enabledTooltip
  inactiveTooltipText: stateKnown ? disabledTooltip : disabledTooltip + " — status unavailable; click to retry"

  function refresh() {
    if (!statusProcess.running) statusProcess.running = true
  }

  function toggle() {
    if (!stateKnown) { refresh(); return }
    if (!toggleProcess.running) toggleProcess.running = true
  }

  onPressed: root.toggle()

  Process {
    id: statusProcess
    command: root.statusCommand
    stdout: StdioCollector {
      onStreamFinished: {
        try {
          var value
          if (root.statusFormat === "on-off") {
            var state = text.trim()
            if (state !== "on" && state !== "off") throw new Error("Invalid status")
            value = state === "on"
          } else {
            value = JSON.parse(text).enabled
            if (typeof value !== "boolean") throw new Error("Invalid status")
          }
          root.commandActive = value
          root.stateKnown = true
        } catch (error) {
          root.stateKnown = false
        }
      }
    }
    onExited: function(exitCode) {
      if (exitCode !== 0) root.stateKnown = false
    }
  }

  Process {
    id: toggleProcess
    command: root.toggleCommand
    onExited: root.refresh()
  }

  // Follow external changes from menus, keybindings, and other monitors.
  Timer {
    interval: 5000
    running: true
    repeat: true
    triggeredOnStart: true
    onTriggered: root.refresh()
  }
}
