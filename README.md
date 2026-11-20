# Select Collection Objects

A small Blender add-on that makes collections behave like selection groups:
click a collection, or any object in it, and every object in that collection
gets selected.

## What it does

| Action | Result |
|---|---|
| Click a collection in the Outliner | Selects all objects in the collection, child collections included |
| Click an object in the Outliner | Selects the whole collection the object belongs to |
| Click an object in the 3D Viewport | Selects the whole collection the object belongs to |
| Double-click an object | Selects only that object |
| Cmd+click an object | Selects only that object |
| Shift+click | Unchanged Blender behaviour |

Objects that sit directly in the Scene Collection are selected on their own,
so one click never selects the entire scene. The add-on only acts in Object Mode.

## Settings

Each behaviour has its own checkbox in *Preferences > Add-ons > Select
Collection Objects*, all enabled by default.

With the Outliner double-click option enabled, double-clicking an object no
longer renames it; use F2 instead. Double-clicking a collection still renames it.

## Languages

The interface follows Blender's language setting. Translations are included for
Czech, German, Spanish, French, Italian, Portuguese, Dutch, Polish, Russian,
Ukrainian, Turkish, Japanese, Korean and Chinese (Simplified and Traditional);
everything else falls back to English. Apart from Czech the translations are
machine-made, corrections are welcome.

## Installation

Requires Blender 4.2 or newer.

1. Download the repository as a ZIP (*Code > Download ZIP*).
2. In Blender open *Edit > Preferences > Get Extensions*, open the menu in the
   top right corner and choose *Install from Disk*.
3. Pick the downloaded ZIP and enable the add-on.

To build a release package yourself, run this in the repository folder:

```
blender --command extension build
```

## Notes

- Cmd+click is a macOS shortcut; on Windows and Linux it maps to the
  Windows/Super key.
- Viewport clicks were developed with the Select Box tool active. Tools that
  select on mouse press may bypass the add-on.
- Developed on Blender 5.3 (macOS).

## License

GPL-3.0-or-later, see [LICENSE](LICENSE).
