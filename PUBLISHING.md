# Daniel Moya's Omarchy plugin publication plan

Publisher: [danimoya](https://github.com/danimoya)
Public author/contact: Daniel Moya <me@danimoya.com>
Prepared 2026-10-04. The four repositories are development snapshots, not supported releases.

| Repository | Plugin ID | First-release focus |
| --- | --- | --- |
| omarchy-google-drive | danimoya.gdrive | Private status API, reversible setup, Google onboarding and recovery tests |
| omarchy-animated-screensaver | danimoya.idle | General artwork settings, owned-process cleanup, stable launcher and multi-monitor tests |
| omarchy-monitor-mirror | danimoya.monitor | Managed opt-in automirroring, reconnection/debounce, laptop/dock tests |
| omarchy-live-lock | danimoya.lock | Lock-surface isolation, fail-closed behavior, PAM and suspend/crash/hotplug tests |

The existing service IDs are deliberately retained for compatibility with clone restoration and Stay Awake. All four use a root manifest, MIT licensing with upstream attribution, README, and a release checklist. Companion indicators are reference code within the screensaver repository, not a fifth marketplace submission.

## Publishing accounts

1. Sign into GitHub as **danimoya**. The existing verified secondary email **me@danimoya.com** is the requested commit identity; it does not need to become your primary GitHub email.
2. On this laptop run `gh auth login --hostname github.com --git-protocol https --web`, then `gh api user --jq .login`. The result must be `danimoya`.
3. Each project uses local Git settings `user.name=Daniel Moya` and `user.email=me@danimoya.com`; global settings are preserved. This email appears publicly in published commits.
4. Omarchy Plugins uses GitHub issue submissions. No additional publishing account is described by its current guide. Use [the plugin submission form](https://github.com/omacom/omarchy-plugin-marketplace/issues/new?template=submit-plugin.yml) once a release candidate meets the requirements.
5. Open [Omahub Submit](https://omahub.dev/submit), select **Sign in with GitHub**, and authenticate as `danimoya`. Its sign-in page says it requests your public profile. Review the actual permission screen before authorizing.
6. After login, submit each public repository URL separately. Omahub imports metadata and holds the submission for maintainer review. GitHub CLI authentication does not sign your browser into Omahub.

## Release and directory workflow

1. Complete each repository's RELEASE-CHECKLIST.md. Prioritize Drive as the useful flagship and screensavers as the visual demo; release lock integration after its isolation tests.
2. Run manifest, shell and QML checks, then install/disable/remove in a disposable user session on the supported stable Omarchy version. Record exact versions and results.
3. Add a real screenshot/preview to each repository with no personal filenames, notifications or account details. Keep names and author identity consistent.
4. Update the version from 0.1.0-dev to 0.1.0 only after tests pass, commit, tag the tested revision and publish release notes listing dependencies and known limitations.
5. Finalize each MARKETPLACE-SUBMISSION.md. Check ownership, public-repository status, install/removal behavior and dependency/license statements. Replace the draft maintainer note with the tested commit and supported versions.
6. Submit one GitHub issue per plugin, titled `[Plugin]: <name>`. The form contains repository URL, category, tags, maintainer notes and checklist. Submit only when the checklist statements are accurate.
7. Submit the same four repository URLs at Omahub. Track all eight submission links. A submitted repository is not yet a published directory listing: both directories require maintainers to approve it.
8. Address validation/review comments in the existing submissions. Once listed, announce short demos through Omarchy's community channels and respond to reproducible issues. Keep a portfolio index pointing to all four projects.

## Sources

- [Omarchy publishing guide](https://plugins.omarchy.org/publish.html)
- [Current marketplace submission and review process](https://github.com/omacom/omarchy-plugin-marketplace/blob/main/SUBMISSION.md)
- [Omahub submission and login requirements](https://omahub.dev/submit)
- [Google Drive account setup](https://github.com/danimoya/omarchy-google-drive/blob/main/ACCOUNT-SETUP.md)

Detailed technical blockers live with each repository in RELEASE-CHECKLIST.md. This plan does not claim that manifest validation proves runtime behavior or lock security.
