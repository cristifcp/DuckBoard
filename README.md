# DuckBoard

DuckBoard is a privacy-first Android keyboard with Duck Reader's palette. It is
a fork of [HeliBoard](https://github.com/HeliBorg/HeliBoard), which descends from
the AOSP keyboard.

**No `INTERNET` permission.** Not "offline by default", not "network features
are opt-in": the capability is absent from the manifest, so nothing can leave
the device. Android cloud backup and device transfer are disabled too.

| Keyboard, dark | Keyboard, light | Emoji | Settings |
| :---: | :---: | :---: | :---: |
| <img src="docs/screenshots/keyboard-dark.png" width="200" alt="DuckBoard dark keyboard" /> | <img src="docs/screenshots/keyboard-light.png" width="200" alt="DuckBoard light keyboard with suggestions" /> | <img src="docs/screenshots/emoji.png" width="200" alt="DuckBoard emoji panel" /> | <img src="docs/screenshots/settings.png" width="200" alt="DuckBoard settings" /> |

## Download

Install the signed APK from Releases, or build it yourself. Requires Android
5.0 (API 21) or newer.

To get updates without the keyboard checking the network (which it cannot do),
use [Obtainium](https://github.com/ImranR98/Obtainium) and point it at this
repository. Version names carry a monotonic build number.

## Install

1. Install the APK.
2. Settings → System → Languages & input → On-screen keyboard → Manage
   keyboards → enable **DuckBoard**.
3. Pick DuckBoard as the current keyboard.

## What DuckBoard changes

DuckBoard keeps everything that makes HeliBoard a good keyboard — gesture
typing, suggestions and autocorrect, dictionaries, clipboard history, emoji,
multilingual layouts, one-handed and split modes — and changes the identity and
the out-of-box look:

- **Duck Paper and Duck Night themes**, built on Duck Reader's warm paper,
  deep teal and amber. Duck Night is the default at night, Duck Paper by day.
- **Rounded, filled keys by default.** HeliBoard's Material style draws
  transparent key backgrounds unless key borders are on; DuckBoard ships with
  rounded filled keys because floating letters are not a keyboard.
- **Gboard-like defaults:** a dedicated emoji key in the bottom row, key hints
  off, autocorrect and gesture typing on, vibration on, sound off.
- **A cheerful duck-and-keyboard launcher icon** in adaptive, legacy and round
  forms, from the artwork in `branding/duckboard-icon.png`.
- **Clipboard history is off by default**, so copied text is not retained unless
  you turn it on.
- **No Android backup.** Learned words, clipboard history and settings stay in
  the app's private storage instead of going to a cloud backup.
- **Romanian dictionary kept in debug builds.** Upstream strips `main_ro.dict`
  from debug APKs to save space; DuckBoard keeps it.
- **DuckBoard identity everywhere:** app and IME name, settings title,
  spell-checker, About screen, provider authorities and package id
  (`com.cristifcp.duckboard`), so it installs alongside HeliBoard.

The full list, with files, is in [MODIFICATIONS.md](MODIFICATIONS.md).

## Features from HeliBoard

- Glide typing with open gesture data, suggestion strip, autocorrect, learned
  words, user dictionary and per-language dictionaries.
- Multilingual typing and subtypes, including Romanian.
- Emoji panel with search and recents, clipboard history with pinning (off by
  default), and incognito mode that pauses clipboard history.
- Number row, long-press popups, one-handed mode, split keyboard, floating
  keyboard, custom layouts, key borders, theme colours and height scaling.
- No ads, no analytics, no account, no network permission.

## Build

Needs JDK 17 or newer and the Android SDK with `compileSdk 37`.

```bash
./gradlew assembleDebug          # debug build, installs as DuckBoard
./gradlew assembleRelease        # signed only if a keystore is configured
```

`assembleRelease` signs when `keystore.properties` exists at the repository root
(git-ignored) or the `RELEASE_STORE_FILE`, `RELEASE_STORE_PASSWORD`,
`RELEASE_KEY_ALIAS` and `RELEASE_KEY_PASSWORD` environment variables are set.

## Tests

```bash
./gradlew testDebugUnitTest      # JVM tests
./gradlew lintDebug              # Android lint
```

## Privacy

No account, analytics, ads or network permission. The keyboard's learned words,
clipboard history and settings live in the app's private, device-protected
storage; Android backup and device-to-device transfer are excluded. Clipboard
history pauses while incognito is active. A backup can still be written
manually through Settings → Advanced → Backup, and it goes only where you point
it.

## Licence and credits

GNU GPL v3.0 — see [LICENSE](LICENSE). DuckBoard is based on HeliBoard (© the
HeliBoard contributors) and the AOSP keyboard. Because this is a modified GPL
work, anyone who receives a build is entitled to the source it was built from.

The duck artwork and the Duck Paper / Duck Night palettes are part of this
project's artwork, shared with Duck Reader.
