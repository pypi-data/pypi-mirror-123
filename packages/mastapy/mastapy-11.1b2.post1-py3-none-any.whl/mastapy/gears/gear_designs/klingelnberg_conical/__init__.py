'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._921 import KlingelnbergConicalGearDesign
    from ._922 import KlingelnbergConicalGearMeshDesign
    from ._923 import KlingelnbergConicalGearSetDesign
    from ._924 import KlingelnbergConicalMeshedGearDesign
