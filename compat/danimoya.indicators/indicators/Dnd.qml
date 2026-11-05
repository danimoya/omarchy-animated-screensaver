import QtQuick

CommandIndicator {
  id: root
  objectName: "dndIndicator"
  statusCommand: ["omarchy-shell", "notifications", "isDnd"]
  toggleCommand: ["omarchy", "toggle", "notification", "silencing"]
  statusFormat: "on-off"
  activeText: "󰂛"
  inactiveText: activeText
  enabledTooltip: "Allow Notifications"
  disabledTooltip: "Silence Notifications"
}
