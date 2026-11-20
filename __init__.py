bl_info = {
    "name": "Select Collection Objects",
    "author": "Jáchym Moravec",
    "version": (1, 4, 0),
    "blender": (3, 2, 0),
    "location": "Outliner, 3D Viewport",
    "description": "Double-click an object to select its whole collection; click a collection in the Outliner to select its objects",
    "category": "Object",
}

import bpy
from bpy.props import BoolProperty

# preference name -> keymap items that the preference switches on and off
_items = {}


# ---------------------------------------------------------------- helpers

def _without_scene_collection(context, collections):
    """Skip the Scene Collection, otherwise the whole scene would get selected."""
    scene_collection = context.scene.collection
    result = []
    for collection in collections:
        if collection != scene_collection and collection not in result:
            result.append(collection)
    return result


def _select_collections(context, collections, extend=False):
    """Select every object in the given collections (child collections included)."""
    view_layer = context.view_layer
    if not extend:
        for obj in view_layer.objects:
            if obj.select_get(view_layer=view_layer):
                obj.select_set(False, view_layer=view_layer)

    selected = []
    for collection in collections:
        for obj in collection.all_objects:
            try:
                obj.select_set(True, view_layer=view_layer)
            except RuntimeError:
                continue  # object is not in the view layer
            if obj.select_get(view_layer=view_layer):
                selected.append(obj)
    return selected


# ---------------------------------------------------------------- Outliner

class OUTLINER_OT_select_collection_objects(bpy.types.Operator):
    """Click in the Outliner; clicking a collection also selects all its objects"""
    bl_idname = "outliner.select_collection_objects"
    bl_label = "Select Collection Objects"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.area is not None and context.area.type == 'OUTLINER'

    def invoke(self, context, event):
        # let Blender handle the regular click first
        try:
            result = bpy.ops.outliner.item_activate('INVOKE_DEFAULT', deselect_all=True)
        except RuntimeError:
            return {'PASS_THROUGH'}
        if 'FINISHED' not in result:
            # click outside a row (expand arrow, empty space...): leave it to Blender
            return {'PASS_THROUGH'}

        if context.mode != 'OBJECT':
            return {'FINISHED'}

        # clicking an object keeps the selection exactly as Blender made it
        collections = [
            item for item in getattr(context, "selected_ids", [])
            if isinstance(item, bpy.types.Collection)
        ]
        collections = _without_scene_collection(context, collections)
        if collections:
            view_layer = context.view_layer
            selected = _select_collections(context, collections)
            if selected and view_layer.objects.active not in selected:
                view_layer.objects.active = selected[0]
        return {'FINISHED'}


# ---------------------------------------------------------------- 3D viewport

class VIEW3D_OT_select_collection_objects(bpy.types.Operator):
    """Select every object in the collection of the object that was just clicked"""
    bl_idname = "view3d.select_collection_objects"
    bl_label = "Select Collection Objects"
    bl_options = {'UNDO'}

    extend: BoolProperty(
        name="Extend",
        description="Add the collection to the current selection instead of replacing it",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return (
            context.area is not None
            and context.area.type == 'VIEW_3D'
            and context.mode == 'OBJECT'
        )

    def invoke(self, context, event):
        # Blender already handled the first click of the double-click: the clicked object is active.
        # The add-on does no picking, it only extends the selection to the active object's collection.
        view_layer = context.view_layer
        clicked = view_layer.objects.active
        if clicked is None:
            return {'PASS_THROUGH'}
        # Without Shift: after a click on empty space the active object is not selected, nothing to extend.
        # With Shift the first click may have deselected the active object, so this is not checked.
        if not self.extend and not clicked.select_get(view_layer=view_layer):
            return {'PASS_THROUGH'}

        collections = _without_scene_collection(context, clicked.users_collection)
        if not collections:
            # the object is only in the Scene Collection: it stays selected on its own
            return {'PASS_THROUGH'}

        _select_collections(context, collections, extend=self.extend)
        try:
            clicked.select_set(True, view_layer=view_layer)
        except RuntimeError:
            pass
        view_layer.objects.active = clicked
        return {'FINISHED'}


# ---------------------------------------------------------------- preferences

def _apply_preferences(self=None, context=None):
    try:
        prefs = bpy.context.preferences.addons[__package__].preferences
    except (KeyError, AttributeError):
        prefs = None
    for name, items in _items.items():
        enabled = True if prefs is None else bool(getattr(prefs, name, True))
        for _keymap, item in items:
            item.active = enabled


class SelectCollectionObjectsPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    outliner_collection: BoolProperty(
        name="Outliner: clicking a collection selects all its objects",
        default=True,
        update=_apply_preferences,
    )
    viewport_double: BoolProperty(
        name="Viewport: double-clicking an object selects its whole collection",
        description="Shift + double-click adds the collection to the current selection",
        default=True,
        update=_apply_preferences,
    )

    def draw(self, context):
        column = self.layout.column()
        column.prop(self, "outliner_collection")
        column.prop(self, "viewport_double")


# ---------------------------------------------------------------- registration

_classes = (
    SelectCollectionObjectsPreferences,
    OUTLINER_OT_select_collection_objects,
    VIEW3D_OT_select_collection_objects,
)


def _add(pref_name, keymap, idname, value, **modifiers):
    item = keymap.keymap_items.new(idname, 'LEFTMOUSE', value, **modifiers)
    _items.setdefault(pref_name, []).append((keymap, item))
    return item


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)

    keyconfig = bpy.context.window_manager.keyconfigs.addon
    if keyconfig:
        keymap = keyconfig.keymaps.new(name="Outliner", space_type='OUTLINER')
        _add("outliner_collection", keymap,
             OUTLINER_OT_select_collection_objects.bl_idname, 'CLICK')

        # the "Object Mode" keymap only applies in Object Mode, other modes stay untouched
        keymap = keyconfig.keymaps.new(name="Object Mode", space_type='EMPTY')
        idname = VIEW3D_OT_select_collection_objects.bl_idname
        item = _add("viewport_double", keymap, idname, 'DOUBLE_CLICK')
        item.properties.extend = False
        item = _add("viewport_double", keymap, idname, 'DOUBLE_CLICK', shift=True)
        item.properties.extend = True

    _apply_preferences()


def unregister():
    for items in _items.values():
        for keymap, item in items:
            keymap.keymap_items.remove(item)
    _items.clear()
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)

