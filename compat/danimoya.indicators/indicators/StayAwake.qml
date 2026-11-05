import QtQuick
import Quickshell
import Quickshell.Io

CommandIndicator {
  id: root
  objectName: "stayAwakeIndicator"
  statusCommand: ["omarchy", "toggle", "idle", "status"]
  toggleCommand: ["omarchy", "toggle", "idle"]
  statusFormat: "json"
  activeText: "󰅶"
  inactiveText: activeText
  enabledTooltip: "Allow Idle Lock & Screensaver"
  disabledTooltip: "Stay Awake"

  FileView {
    path: Quickshell.env("HOME") + "/.local/state/omarchy/indicators"
    watchChanges: true
    printErrors: false
    onFileChanged: root.refresh()
  }
}
