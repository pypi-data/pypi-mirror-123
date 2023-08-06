'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._896 import WormDesign
    from ._897 import WormGearDesign
    from ._898 import WormGearMeshDesign
    from ._899 import WormGearSetDesign
    from ._900 import WormWheelDesign
