bl_info = {
    "name": "Select Collection Objects",
    "author": "Jáchym Moravec",
    "version": (1, 3, 1),
    "blender": (3, 2, 0),
    "location": "Outliner, 3D Viewport",
    "description": "Clicking a collection or an object selects every object in that collection; double-click and Cmd+click select a single object",
    "category": "Object",
}

import bpy
from bpy.props import BoolProperty, EnumProperty

_keymaps = []


# ---------------------------------------------------------------- strings and translations
# Source strings are English. Blender translates them according to the interface
# language (Preferences > Interface > Language); other languages fall back to English.

S_OUTLINER_COLLECTION = "Outliner: clicking a collection selects all its objects"
S_OUTLINER_OBJECT = "Outliner: clicking an object selects its whole collection"
S_VIEWPORT_OBJECT = "Viewport: clicking an object selects its whole collection"
S_OUTLINER_DOUBLE = "Outliner: double-clicking an object selects only that object"
S_VIEWPORT_DOUBLE = "Viewport: double-clicking an object selects only that object"
S_CMD_SINGLE = "Cmd+click selects only one object (Outliner and viewport)"
S_HEADER_COLLECTION = "Click selects the whole collection:"
S_HEADER_SINGLE = "Select only one object:"
S_DOUBLE_TOOLTIP = (
    "Double-click no longer renames objects, use F2 instead. "
    "Double-clicking a collection still renames it"
)
S_OP_COLLECTION = "Select Collection Objects"
S_OP_SINGLE = "Select Single Object"

_MSGIDS = (
    S_OUTLINER_COLLECTION,
    S_OUTLINER_OBJECT,
    S_VIEWPORT_OBJECT,
    S_OUTLINER_DOUBLE,
    S_VIEWPORT_DOUBLE,
    S_CMD_SINGLE,
    S_HEADER_COLLECTION,
    S_HEADER_SINGLE,
    S_DOUBLE_TOOLTIP,
    S_OP_COLLECTION,
    S_OP_SINGLE,
)

# Per language: Blender locale codes (they differ between versions) and texts in _MSGIDS order.
_LANGUAGES = (
    (("cs", "cs_CZ"), (
        "Outliner: klik na kolekci označí všechny její objekty",
        "Outliner: klik na objekt označí celou jeho kolekci",
        "Viewport: klik na objekt označí celou jeho kolekci",
        "Outliner: dvojklik na objekt označí jen ten jeden objekt",
        "Viewport: dvojklik na objekt označí jen ten jeden objekt",
        "Cmd+klik označí jen jeden objekt (Outliner i viewport)",
        "Klik označí celou kolekci:",
        "Výběr jen jednoho objektu:",
        "Dvojklik pak objekty nepřejmenovává, použij F2. Dvojklik na kolekci ji přejmenovává dál",
        "Označit objekty kolekce",
        "Označit jeden objekt",
    )),
    (("de", "de_DE"), (
        "Outliner: Klick auf eine Sammlung wählt alle ihre Objekte aus",
        "Outliner: Klick auf ein Objekt wählt seine gesamte Sammlung aus",
        "Viewport: Klick auf ein Objekt wählt seine gesamte Sammlung aus",
        "Outliner: Doppelklick auf ein Objekt wählt nur dieses Objekt aus",
        "Viewport: Doppelklick auf ein Objekt wählt nur dieses Objekt aus",
        "Cmd+Klick wählt nur ein Objekt aus (Outliner und Viewport)",
        "Klick wählt die gesamte Sammlung aus:",
        "Nur ein Objekt auswählen:",
        "Doppelklick benennt Objekte dann nicht mehr um, stattdessen F2 verwenden. Doppelklick auf eine Sammlung benennt sie weiterhin um",
        "Objekte der Sammlung auswählen",
        "Einzelnes Objekt auswählen",
    )),
    (("es", "es_ES"), (
        "Outliner: hacer clic en una colección selecciona todos sus objetos",
        "Outliner: hacer clic en un objeto selecciona toda su colección",
        "Viewport: hacer clic en un objeto selecciona toda su colección",
        "Outliner: hacer doble clic en un objeto selecciona solo ese objeto",
        "Viewport: hacer doble clic en un objeto selecciona solo ese objeto",
        "Cmd+clic selecciona solo un objeto (Outliner y viewport)",
        "El clic selecciona toda la colección:",
        "Seleccionar solo un objeto:",
        "El doble clic deja de renombrar objetos; usa F2. El doble clic en una colección sigue renombrándola",
        "Seleccionar objetos de la colección",
        "Seleccionar un solo objeto",
    )),
    (("fr", "fr_FR"), (
        "Outliner : un clic sur une collection sélectionne tous ses objets",
        "Outliner : un clic sur un objet sélectionne toute sa collection",
        "Viewport : un clic sur un objet sélectionne toute sa collection",
        "Outliner : un double-clic sur un objet sélectionne uniquement cet objet",
        "Viewport : un double-clic sur un objet sélectionne uniquement cet objet",
        "Cmd+clic sélectionne un seul objet (Outliner et viewport)",
        "Le clic sélectionne toute la collection :",
        "Sélectionner un seul objet :",
        "Le double-clic ne renomme alors plus les objets, utilisez F2. Le double-clic sur une collection la renomme toujours",
        "Sélectionner les objets de la collection",
        "Sélectionner un seul objet",
    )),
    (("it", "it_IT"), (
        "Outliner: il clic su una collezione seleziona tutti i suoi oggetti",
        "Outliner: il clic su un oggetto seleziona l'intera collezione",
        "Viewport: il clic su un oggetto seleziona l'intera collezione",
        "Outliner: il doppio clic su un oggetto seleziona solo quell'oggetto",
        "Viewport: il doppio clic su un oggetto seleziona solo quell'oggetto",
        "Cmd+clic seleziona un solo oggetto (Outliner e viewport)",
        "Il clic seleziona l'intera collezione:",
        "Selezionare un solo oggetto:",
        "Il doppio clic non rinomina più gli oggetti, usa F2. Il doppio clic su una collezione continua a rinominarla",
        "Seleziona oggetti della collezione",
        "Seleziona un solo oggetto",
    )),
    (("pt", "pt_BR", "pt_PT"), (
        "Outliner: clicar em uma coleção seleciona todos os seus objetos",
        "Outliner: clicar em um objeto seleciona toda a sua coleção",
        "Viewport: clicar em um objeto seleciona toda a sua coleção",
        "Outliner: clicar duas vezes em um objeto seleciona apenas esse objeto",
        "Viewport: clicar duas vezes em um objeto seleciona apenas esse objeto",
        "Cmd+clique seleciona apenas um objeto (Outliner e viewport)",
        "O clique seleciona toda a coleção:",
        "Selecionar apenas um objeto:",
        "O clique duplo deixa de renomear objetos, use F2. O clique duplo em uma coleção continua a renomeá-la",
        "Selecionar objetos da coleção",
        "Selecionar um único objeto",
    )),
    (("nl", "nl_NL"), (
        "Outliner: klikken op een collectie selecteert alle objecten erin",
        "Outliner: klikken op een object selecteert de hele collectie",
        "Viewport: klikken op een object selecteert de hele collectie",
        "Outliner: dubbelklikken op een object selecteert alleen dat object",
        "Viewport: dubbelklikken op een object selecteert alleen dat object",
        "Cmd+klik selecteert slechts één object (Outliner en viewport)",
        "Klik selecteert de hele collectie:",
        "Slechts één object selecteren:",
        "Dubbelklikken hernoemt objecten dan niet meer, gebruik F2. Dubbelklikken op een collectie hernoemt die nog wel",
        "Objecten van collectie selecteren",
        "Eén object selecteren",
    )),
    (("pl", "pl_PL"), (
        "Outliner: kliknięcie kolekcji zaznacza wszystkie jej obiekty",
        "Outliner: kliknięcie obiektu zaznacza całą jego kolekcję",
        "Viewport: kliknięcie obiektu zaznacza całą jego kolekcję",
        "Outliner: dwukrotne kliknięcie obiektu zaznacza tylko ten obiekt",
        "Viewport: dwukrotne kliknięcie obiektu zaznacza tylko ten obiekt",
        "Cmd+kliknięcie zaznacza tylko jeden obiekt (Outliner i viewport)",
        "Kliknięcie zaznacza całą kolekcję:",
        "Zaznaczanie tylko jednego obiektu:",
        "Dwukrotne kliknięcie nie zmienia już nazw obiektów, użyj F2. Dwukrotne kliknięcie kolekcji nadal zmienia jej nazwę",
        "Zaznacz obiekty kolekcji",
        "Zaznacz jeden obiekt",
    )),
    (("ru", "ru_RU"), (
        "Outliner: щелчок по коллекции выделяет все её объекты",
        "Outliner: щелчок по объекту выделяет всю его коллекцию",
        "Viewport: щелчок по объекту выделяет всю его коллекцию",
        "Outliner: двойной щелчок по объекту выделяет только этот объект",
        "Viewport: двойной щелчок по объекту выделяет только этот объект",
        "Cmd+щелчок выделяет только один объект (Outliner и Viewport)",
        "Щелчок выделяет всю коллекцию:",
        "Выделение только одного объекта:",
        "Двойной щелчок больше не переименовывает объекты, используйте F2. Двойной щелчок по коллекции по-прежнему переименовывает её",
        "Выделить объекты коллекции",
        "Выделить один объект",
    )),
    (("uk", "uk_UA"), (
        "Outliner: клацання по колекції виділяє всі її об'єкти",
        "Outliner: клацання по об'єкту виділяє всю його колекцію",
        "Viewport: клацання по об'єкту виділяє всю його колекцію",
        "Outliner: подвійне клацання по об'єкту виділяє лише цей об'єкт",
        "Viewport: подвійне клацання по об'єкту виділяє лише цей об'єкт",
        "Cmd+клацання виділяє лише один об'єкт (Outliner і Viewport)",
        "Клацання виділяє всю колекцію:",
        "Виділення лише одного об'єкта:",
        "Подвійне клацання більше не перейменовує об'єкти, використовуйте F2. Подвійне клацання по колекції й надалі перейменовує її",
        "Виділити об'єкти колекції",
        "Виділити один об'єкт",
    )),
    (("tr", "tr_TR"), (
        "Outliner: bir koleksiyona tıklamak içindeki tüm nesneleri seçer",
        "Outliner: bir nesneye tıklamak tüm koleksiyonunu seçer",
        "Viewport: bir nesneye tıklamak tüm koleksiyonunu seçer",
        "Outliner: bir nesneye çift tıklamak yalnızca o nesneyi seçer",
        "Viewport: bir nesneye çift tıklamak yalnızca o nesneyi seçer",
        "Cmd+tıklama yalnızca bir nesneyi seçer (Outliner ve viewport)",
        "Tıklama tüm koleksiyonu seçer:",
        "Yalnızca bir nesne seçme:",
        "Çift tıklama artık nesneleri yeniden adlandırmaz, F2 kullanın. Bir koleksiyona çift tıklamak onu yeniden adlandırmaya devam eder",
        "Koleksiyon nesnelerini seç",
        "Tek nesne seç",
    )),
    (("ja", "ja_JP"), (
        "アウトライナー: コレクションをクリックすると中のオブジェクトをすべて選択",
        "アウトライナー: オブジェクトをクリックするとコレクション全体を選択",
        "ビューポート: オブジェクトをクリックするとコレクション全体を選択",
        "アウトライナー: オブジェクトをダブルクリックするとそのオブジェクトだけを選択",
        "ビューポート: オブジェクトをダブルクリックするとそのオブジェクトだけを選択",
        "Cmd+クリックでオブジェクトを1つだけ選択（アウトライナーとビューポート）",
        "クリックでコレクション全体を選択:",
        "オブジェクトを1つだけ選択:",
        "ダブルクリックではオブジェクト名を変更できなくなります。F2を使ってください。コレクションのダブルクリックは引き続き名前変更です",
        "コレクションのオブジェクトを選択",
        "オブジェクトを1つ選択",
    )),
    (("ko", "ko_KR"), (
        "아웃라이너: 컬렉션을 클릭하면 그 안의 모든 오브젝트를 선택",
        "아웃라이너: 오브젝트를 클릭하면 해당 컬렉션 전체를 선택",
        "뷰포트: 오브젝트를 클릭하면 해당 컬렉션 전체를 선택",
        "아웃라이너: 오브젝트를 더블 클릭하면 그 오브젝트만 선택",
        "뷰포트: 오브젝트를 더블 클릭하면 그 오브젝트만 선택",
        "Cmd+클릭으로 오브젝트 하나만 선택 (아웃라이너와 뷰포트)",
        "클릭하면 컬렉션 전체를 선택:",
        "오브젝트 하나만 선택:",
        "더블 클릭으로 오브젝트 이름을 바꿀 수 없게 됩니다. F2를 사용하세요. 컬렉션을 더블 클릭하면 계속 이름을 바꿉니다",
        "컬렉션 오브젝트 선택",
        "단일 오브젝트 선택",
    )),
    (("zh_HANS", "zh_CN"), (
        "大纲视图：单击集合会选中其中的所有物体",
        "大纲视图：单击物体会选中其所在的整个集合",
        "3D视图：单击物体会选中其所在的整个集合",
        "大纲视图：双击物体只选中该物体",
        "3D视图：双击物体只选中该物体",
        "Cmd+单击只选中一个物体（大纲视图和3D视图）",
        "单击选中整个集合：",
        "只选中一个物体：",
        "双击将不再重命名物体，请使用 F2。双击集合仍会重命名",
        "选中集合中的物体",
        "选中单个物体",
    )),
    (("zh_HANT", "zh_TW"), (
        "大綱視圖：點擊集合會選取其中的所有物體",
        "大綱視圖：點擊物體會選取其所在的整個集合",
        "3D視圖：點擊物體會選取其所在的整個集合",
        "大綱視圖：雙擊物體只選取該物體",
        "3D視圖：雙擊物體只選取該物體",
        "Cmd+點擊只選取一個物體（大綱視圖和3D視圖）",
        "點擊選取整個集合：",
        "只選取一個物體：",
        "雙擊將不再重新命名物體，請使用 F2。雙擊集合仍會重新命名",
        "選取集合中的物體",
        "選取單個物體",
    )),
)


def _build_translations():
    result = {}
    for codes, texts in _LANGUAGES:
        table = {}
        for msgid, text in zip(_MSGIDS, texts):
            # "*" = regular UI text, "Operator" = operator labels
            table[("*", msgid)] = text
            table[("Operator", msgid)] = text
        for code in codes:
            result[code] = table
    return result


# ---------------------------------------------------------------- preferences

class SelectCollectionObjectsPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    outliner_collection: BoolProperty(
        name=S_OUTLINER_COLLECTION,
        default=True,
    )
    outliner_object: BoolProperty(
        name=S_OUTLINER_OBJECT,
        default=True,
    )
    viewport_object: BoolProperty(
        name=S_VIEWPORT_OBJECT,
        default=True,
    )
    outliner_double: BoolProperty(
        name=S_OUTLINER_DOUBLE,
        description=S_DOUBLE_TOOLTIP,
        default=True,
    )
    viewport_double: BoolProperty(
        name=S_VIEWPORT_DOUBLE,
        default=True,
    )
    cmd_single: BoolProperty(
        name=S_CMD_SINGLE,
        default=True,
    )

    def draw(self, context):
        column = self.layout.column()
        column.label(text=S_HEADER_COLLECTION)
        column.prop(self, "outliner_collection")
        column.prop(self, "outliner_object")
        column.prop(self, "viewport_object")
        column.separator()
        column.label(text=S_HEADER_SINGLE)
        column.prop(self, "outliner_double")
        column.prop(self, "viewport_double")
        column.prop(self, "cmd_single")


def _prefs(context):
    return context.preferences.addons[__package__].preferences


# ---------------------------------------------------------------- helpers

def _without_scene_collection(context, collections):
    """Skip the Scene Collection, otherwise the whole scene would get selected."""
    scene_collection = context.scene.collection
    result = []
    for collection in collections:
        if collection != scene_collection and collection not in result:
            result.append(collection)
    return result


def _select_collections(context, collections):
    """Select every object in the given collections (child collections included), deselect the rest."""
    if not collections:
        return
    view_layer = context.view_layer
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

    if selected and view_layer.objects.active not in selected:
        view_layer.objects.active = selected[0]


def _select_only(context, keep):
    """Keep only one object selected."""
    view_layer = context.view_layer
    for obj in view_layer.objects:
        if obj != keep and obj.select_get(view_layer=view_layer):
            obj.select_set(False, view_layer=view_layer)
    keep.select_set(True, view_layer=view_layer)
    view_layer.objects.active = keep


def _outliner_clicked_ids(context):
    return list(getattr(context, "selected_ids", []))


_TRIGGER_ITEMS = (
    ('DOUBLE', "Double-click", ""),
    ('CMD', "Cmd+click", ""),
)


# ---------------------------------------------------------------- Outliner

class OUTLINER_OT_select_collection_objects(bpy.types.Operator):
    """Click in the Outliner that also selects every object in the collection"""
    bl_idname = "outliner.select_collection_objects"
    bl_label = S_OP_COLLECTION
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.area is not None and context.area.type == 'OUTLINER'

    def invoke(self, context, event):
        prefs = _prefs(context)
        if not (prefs.outliner_collection or prefs.outliner_object):
            return {'PASS_THROUGH'}

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

        collections = []
        for item in _outliner_clicked_ids(context):
            if isinstance(item, bpy.types.Collection) and prefs.outliner_collection:
                collections.append(item)
            elif isinstance(item, bpy.types.Object) and prefs.outliner_object:
                collections.extend(item.users_collection)

        _select_collections(context, _without_scene_collection(context, collections))
        return {'FINISHED'}


class OUTLINER_OT_select_single_object(bpy.types.Operator):
    """Select a single object in the Outliner, without the rest of its collection"""
    bl_idname = "outliner.select_single_object"
    bl_label = S_OP_SINGLE
    bl_options = {'UNDO'}

    trigger: EnumProperty(items=_TRIGGER_ITEMS, default='DOUBLE')

    @classmethod
    def poll(cls, context):
        return context.area is not None and context.area.type == 'OUTLINER'

    def invoke(self, context, event):
        prefs = _prefs(context)
        enabled = prefs.outliner_double if self.trigger == 'DOUBLE' else prefs.cmd_single
        if not enabled:
            return {'PASS_THROUGH'}

        try:
            result = bpy.ops.outliner.item_activate('INVOKE_DEFAULT', deselect_all=True)
        except RuntimeError:
            return {'PASS_THROUGH'}
        if 'FINISHED' not in result:
            return {'PASS_THROUGH'}

        objects = [i for i in _outliner_clicked_ids(context) if isinstance(i, bpy.types.Object)]
        if objects:
            if context.mode == 'OBJECT':
                try:
                    _select_only(context, objects[0])
                except RuntimeError:
                    pass
        elif self.trigger == 'DOUBLE':
            # double-click on a collection or other rows: keep renaming
            try:
                bpy.ops.outliner.item_rename('INVOKE_DEFAULT')
            except RuntimeError:
                pass
        return {'FINISHED'}


# ---------------------------------------------------------------- 3D viewport

class VIEW3D_OT_select_collection_objects(bpy.types.Operator):
    """Click in the viewport that also selects every object in the same collection"""
    bl_idname = "view3d.select_collection_objects"
    bl_label = S_OP_COLLECTION
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return (
            context.area is not None
            and context.area.type == 'VIEW_3D'
            and context.mode == 'OBJECT'
        )

    def invoke(self, context, event):
        if not _prefs(context).viewport_object:
            return {'PASS_THROUGH'}

        # let the regular click selection run first
        try:
            result = bpy.ops.view3d.select('INVOKE_DEFAULT', deselect_all=True)
        except RuntimeError:
            return {'PASS_THROUGH'}
        if 'FINISHED' not in result:
            return {'PASS_THROUGH'}

        view_layer = context.view_layer
        clicked = view_layer.objects.active
        # click on empty space: nothing selected, nothing to extend
        if clicked is None or not clicked.select_get(view_layer=view_layer):
            return {'FINISHED'}

        collections = _without_scene_collection(context, clicked.users_collection)
        _select_collections(context, collections)
        return {'FINISHED'}


class VIEW3D_OT_select_single_object(bpy.types.Operator):
    """Select a single object in the viewport, without the rest of its collection"""
    bl_idname = "view3d.select_single_object"
    bl_label = S_OP_SINGLE
    bl_options = {'UNDO'}

    trigger: EnumProperty(items=_TRIGGER_ITEMS, default='DOUBLE')

    @classmethod
    def poll(cls, context):
        return (
            context.area is not None
            and context.area.type == 'VIEW_3D'
            and context.mode == 'OBJECT'
        )

    def invoke(self, context, event):
        prefs = _prefs(context)
        view_layer = context.view_layer

        if self.trigger == 'DOUBLE':
            if not prefs.viewport_double:
                return {'PASS_THROUGH'}
            # The first click of the double-click already selected the object under the cursor
            # and made it active. Clicking again would make Blender cycle to the object behind it.
            active = view_layer.objects.active
            if active is None or not active.select_get(view_layer=view_layer):
                return {'PASS_THROUGH'}
            _select_only(context, active)
            return {'FINISHED'}

        if not prefs.cmd_single:
            return {'PASS_THROUGH'}
        try:
            result = bpy.ops.view3d.select('INVOKE_DEFAULT', deselect_all=True)
        except RuntimeError:
            return {'PASS_THROUGH'}
        if 'FINISHED' not in result:
            return {'PASS_THROUGH'}
        return {'FINISHED'}


# ---------------------------------------------------------------- registration

_classes = (
    SelectCollectionObjectsPreferences,
    OUTLINER_OT_select_collection_objects,
    OUTLINER_OT_select_single_object,
    VIEW3D_OT_select_collection_objects,
    VIEW3D_OT_select_single_object,
)


def _add_items(keymap, click_op, single_op):
    item = keymap.keymap_items.new(click_op, 'LEFTMOUSE', 'CLICK')
    _keymaps.append((keymap, item))

    item = keymap.keymap_items.new(single_op, 'LEFTMOUSE', 'DOUBLE_CLICK')
    item.properties.trigger = 'DOUBLE'
    _keymaps.append((keymap, item))

    item = keymap.keymap_items.new(single_op, 'LEFTMOUSE', 'CLICK', oskey=True)
    item.properties.trigger = 'CMD'
    _keymaps.append((keymap, item))


def register():
    try:
        bpy.app.translations.unregister(__package__)  # leftover from an unfinished disable
    except Exception:
        pass
    bpy.app.translations.register(__package__, _build_translations())

    for cls in _classes:
        bpy.utils.register_class(cls)

    keyconfig = bpy.context.window_manager.keyconfigs.addon
    if keyconfig:
        keymap = keyconfig.keymaps.new(name="Outliner", space_type='OUTLINER')
        _add_items(
            keymap,
            OUTLINER_OT_select_collection_objects.bl_idname,
            OUTLINER_OT_select_single_object.bl_idname,
        )
        keymap = keyconfig.keymaps.new(name="3D View", space_type='VIEW_3D')
        _add_items(
            keymap,
            VIEW3D_OT_select_collection_objects.bl_idname,
            VIEW3D_OT_select_single_object.bl_idname,
        )


def unregister():
    for keymap, item in _keymaps:
        keymap.keymap_items.remove(item)
    _keymaps.clear()
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
    try:
        bpy.app.translations.unregister(__package__)
    except Exception:
        pass

