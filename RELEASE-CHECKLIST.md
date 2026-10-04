# Before v0.1.0

Status: development preparation; no stable release or directory listing is claimed.

- [ ] Expose user artwork, palette, effects, frame rate, and hold duration as supported settings; the development snapshot uses the HeliosDB preset.
- [ ] Replace stock-launcher text rewriting with a maintained launcher contract; avoid global process-name kills and scope teardown to owned child processes.
- [ ] Make rotation updates atomic across displays, and test paths containing spaces and simultaneous monitor launches.
- [ ] Verify Stay Awake routing on supported Omarchy versions; use the companion adaptation only where required.
- [ ] Test idle cancellation, all supported terminals, multi-monitor behavior, removal/restoration, and CPU/battery impact; capture a preview.
- [ ] Run `omarchy plugin validate .` and QML checks against the target shell.
- [ ] Verify installation, upgrade, disable, and removal in a disposable user session.
- [ ] Add a real preview image and record exact tested Omarchy/Hyprland versions.
- [ ] Review tracked files for account data and preserve upstream license notices.
- [ ] Set the release version only after these checks pass; tag the tested commit.
- [ ] Submit the repository to both directories and record submission links.

See README.md for the present development setup. Passing manifest validation alone does not establish runtime correctness.
