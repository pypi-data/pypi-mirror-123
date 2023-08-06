'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._917 import KlingelnbergCycloPalloidHypoidGearDesign
    from ._918 import KlingelnbergCycloPalloidHypoidGearMeshDesign
    from ._919 import KlingelnbergCycloPalloidHypoidGearSetDesign
    from ._920 import KlingelnbergCycloPalloidHypoidMeshedGearDesign
