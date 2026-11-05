import QtQuick

CommandIndicator {
  id: root
  objectName: "nightLightIndicator"
  statusCommand: ["omarchy", "toggle", "nightlight", "--status"]
  toggleCommand: ["omarchy", "toggle", "nightlight"]
  statusFormat: "json"
  activeText: "󰔎"
  inactiveText: activeText
  enabledTooltip: "Day Light"
  disabledTooltip: "Night Light"
}
