from construct import *
import construct_editor.core.custom as custom

custom.add_custom_adapter(ExprAdapter, "Int16ul_x100", custom.AdapterObjEditorType.String)
Int16ul_x100 = ExprAdapter(Int16ul, obj_ / 100, lambda obj, ctx: int(float(obj) * 100))

construct_format = GreedyRange(
    Struct(
        "temperature" / Int16ul_x100,
        "counter" / Int8ul,
    )
)

