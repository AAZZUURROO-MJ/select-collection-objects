# Select Collection Objects

A small Blender add-on that makes it quick to select everything in a
collection, without changing how a normal click works.

## What it does

| Action | Result |
|---|---|
| Double-click an object in the 3D Viewport | Selects every object in that object's collection, child collections included |
| Shift + double-click an object | Adds the object's whole collection to the current selection |
| Click a collection in the Outliner | Selects every object in the collection, child collections included |

Everything else is plain Blender: a single click selects one object,
Shift+click adds or removes an object, Alt+click opens the menu of objects
under the cursor.

Objects that sit directly in the Scene Collection stay selected on their own,
so a double-click never selects the entire scene. The add-on only acts in
Object Mode.

## Settings

*Preferences > Add-ons > Select Collection Objects* has one checkbox for the
Outliner click and one for the viewport double-click.

## Installation

1. Download the repository as a ZIP (*Code > Download ZIP*).
2. In Blender open *Edit > Preferences > Get Extensions*, open the menu in the
   top right corner and choose *Install from Disk*.
3. Pick the downloaded ZIP and enable the add-on.

## Known limits

- Double-clicking exactly where you clicked a moment ago makes Blender cycle
  to the object behind; the add-on then selects that object's collection.
- Shift + double-click on empty space adds the collection of the active object.
- An object linked to several collections selects all of them.
- Tested on Blender 5.3 (macOS) only. The manifest allows 4.2 and newer, but
  older versions are untested.

## License

GPL-3.0-or-later, see [LICENSE](LICENSE).
