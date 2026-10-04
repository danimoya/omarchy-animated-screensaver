import QtQuick
import qs.Ui

BarIndicator {
  id: root

  // The stock id (omarchy.idle) is disabled on this system in favor of a clone
  // (danimoya.idle) that launches the HeliosDB screensaver instead of the
  // stock one — see ~/.config/omarchy/plugins/danimoya.idle/. Point this at
  // the clone so Stay Awake keeps working; re-clone both together if the
  // clone is ever renamed.
  readonly property var idleService: bar?.shell?.firstPartyServiceFor("danimoya.idle")

  active: idleService ? idleService.stayAwake : false
  activeText: "󰅶"
  inactiveText: "󰅶"
  activeTooltipText: "Allow Idle Lock & Screensaver"
  inactiveTooltipText: "Stay Awake"

  function toggle() {
    if (root.idleService) root.idleService.setIdleEnabled(root.active)
  }

  onPressed: function() { root.toggle() }
}
