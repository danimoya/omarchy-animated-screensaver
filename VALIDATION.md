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

## Scoped API compatibility — 2026-11-05

Target: Omarchy 4.5.0-3, Hyprland 0.56.2.

- Stay Awake, DND, and Night Light now use public commands instead of first-party service proxies, which are unavailable to custom bar widgets. All three share validated status parsing, failed-query feedback, and polling for external changes.
- The idle service reads scoped `shell.idleConfig`, retaining the old full-shell fallback.
- `python3 tests/check-indicators.py`: passed in offscreen Quickshell using synthetic state. Covers all three components, both click directions, external state changes, malformed output, command failure, and recovery.
- Live bar checks: Stay Awake and Night Light toggled in both directions and their indicators followed the service state. DND also toggled in both directions after checking the canonical `omarchy toggle notification silencing` route. Original functional states restored: Stay Awake on, DND off, Night Light off.
- `omarchy plugin validate .` and bundled Bash syntax checks: passed.
- This does not complete idle-timeout, hardware, multi-monitor, fresh-install, or release testing.

## Locked idle startup correction — 2026-11-07

- Live logs show the idle deadline fired while the session was locked, but the
  previous command explicitly skipped `heliosdb-screensaver launch` when
  `lock isLocked` returned true. It exited successfully without starting animation.
- The idle service now requests the optional `lock idleScreensaver` approval hook
  when locked, launches normally when explicitly unlocked, and refuses unknown
  lock state. No lock acquisition, authentication or unlock behavior was added.
- The renderer no longer dismisses because a lock surface owns focus. It keeps
  the cursor visible while locked, retaining ordinary unlocked dismissal.
- Seven mocked IPC/input regression tests pass; Bash syntax, manifest validation
  and whitespace checks pass. Real locked rendering and multi-monitor behavior
  still require runtime verification.
- The installed copy was updated by patching only the idle launch function and
  renderer `run()` block, preserving local artwork and launcher paths.
  Both plugin validations and installed Bash syntax passed;
  the shell restarted without QML errors. Idle reports enabled with Stay Awake
  off and screensaver timeout 150 seconds. Real locked animation remains to test.
