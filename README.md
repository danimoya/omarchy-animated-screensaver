# Animated Screensavers for Omarchy

Rotating ASCII screensavers with HeliosDB artwork, readable pauses, and idle integration.

By **Daniel Moya** — [@danimoya](https://github.com/danimoya) · me@danimoya.com

**Development snapshot (0.1.0-dev).** Prepared for public development; not yet a supported release or approved directory listing. See [release checklist](RELEASE-CHECKLIST.md). This code does not change your running desktop merely by being cloned.

## Obtain the plugin

Once this repository is public:

```sh
omarchy plugin add https://github.com/danimoya/omarchy-animated-screensaver.git
```

Choose not to enable it until completing the setup below. Local source validation:

```sh
omarchy plugin validate .
```

## Development setup

Dependencies: Omarchy Quattro idle/lock services, Quickshell, Hyprland, ttfx (TerminalTextEffects), bash, jq, socat, procps-ng, coreutils, and a supported terminal (Alacritty, Ghostty, Foot or Kitty).

This plugin replaces `omarchy.idle`. The root service retains the existing ID `danimoya.idle` for compatibility. Do not install over an existing personal clone without saving it elsewhere.

1. Install the plugin without enabling it first.
2. Create a command link only if that name is unused:

   ```sh
   mkdir -p ~/.local/bin
   ln -s "$HOME/.config/omarchy/plugins/danimoya.idle/scripts/heliosdb-screensaver" "$HOME/.local/bin/heliosdb-screensaver"
   ```

3. Run `heliosdb-screensaver list`, then a manual `heliosdb-screensaver preview heliosdb-logo beams`.
4. Enable the service through `omarchy plugin enable danimoya.idle`. Check that the stock idle service is replaced and Stay Awake still works.
5. Screensaver and lock timeouts come from the existing shell configuration (defaults 150 and 300 seconds). The standard lock is used unless the optional live-lock wrapper is installed.

Artwork is bundled under `art/`. `OMARCHY_SCREENSAVER_ART_DIR` can supply replacement files with the same six names. `FRAME_RATE` and `HOLD_MIN_SECONDS` override 80 fps and 10 seconds. A general artwork/palette selector remains release work.

## Compatibility

`compat/danimoya.indicators/` contains indicator reference code, without a second plugin manifest. It is not another installable plugin. Stay Awake requests `firstPartyServiceFor("omarchy.idle")`; the shell resolves that built-in ID to the enabled clone. Passing `danimoya.idle` directly is rejected by the scoped first-party API and leaves the button inactive. Verify clone-service resolution in the target shell before deciding whether to ship any indicator override.

After updating an existing indicator override, run `omarchy restart shell` from an unlocked session if automatic plugin reload retains the old code. Check that both the idle service and the coffee-cup indicator change state when toggled.

## Removal

Disable/remove `danimoya.idle` using Omarchy's plugin commands and verify the stock `omarchy.idle` service is restored. Remove the command symlink only if it points to this plugin. Stop a running screensaver first. Preserve user artwork and rotation state.

## Preparation changes

Bundled artwork and resolved it relative to the real script path. Added an artwork-directory override, an optional live-lock fallback, and unique temporary launcher files with cleanup. The prototype still rewrites the stock launcher and uses broad process-name teardown; these are release blockers.

## Publishing and attribution

See [publisher account setup and directory workflow](PUBLISHING.md) and the [validation record](VALIDATION.md).

One root manifest identifies this plugin as `danimoya.idle`. [Marketplace submission draft](MARKETPLACE-SUBMISSION.md) is intentionally incomplete until release checks pass. Submit the same public repository to [Omarchy Plugins](https://plugins.omarchy.org/publish.html) and [Omahub](https://omahub.dev/submit).

Source provenance and upstream credits are recorded in [NOTICE.md](NOTICE.md). MIT license; see [LICENSE](LICENSE). Report reproducible issues through this repository, including Omarchy and Hyprland versions and logs with personal information removed.
