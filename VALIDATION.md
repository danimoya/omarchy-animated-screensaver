# Validation record

Prepared on 2026-10-04 against the laptop's installed Omarchy 4.0.0.alpha.

- `omarchy plugin validate .`: passed.
- Bash syntax checks for bundled scripts: passed.
- Source scan: no access tokens, refresh tokens, private keys, or machine-specific home paths detected in non-documentation source.
- QML lint completed with warnings. The tool was given an import root mapping `qs` to the installed Omarchy shell. Warnings include Quickshell process signal metadata and, for inherited panels/views, dynamic properties. This is not a clean semantic-lint result.
- Artwork listing returns all six bundled presets. No fullscreen animation, idle timeout, or multi-monitor runtime test was performed on the publishing copy.

No publishing copy was installed into the active desktop. No runtime lock/display changes were made. Current-stable compatibility, fresh-account installation/removal, visual preview, and the repository's RELEASE-CHECKLIST.md remain required before a supported release.

## Stay Awake correction — 2026-10-06

- Corrected the installed indicator override to request the built-in `omarchy.idle` service ID, which the shell resolves to the enabled `danimoya.idle` clone; copied that exact correction into the compatibility reference.
- Automatic plugin reload retained the old indicator code; restarting the shell loaded the correction.
- Toggled the live idle service in both directions and verified the bar's active-indicator state followed it. Stay Awake enabled reported idle disabled with screensaver and lock timers stopped.
- The user confirmed the button issue was solved. No full idle-timeout or multi-monitor regression test was performed.
