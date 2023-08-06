'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._892 import ZerolBevelGearDesign
    from ._893 import ZerolBevelGearMeshDesign
    from ._894 import ZerolBevelGearSetDesign
    from ._895 import ZerolBevelMeshedGearDesign
