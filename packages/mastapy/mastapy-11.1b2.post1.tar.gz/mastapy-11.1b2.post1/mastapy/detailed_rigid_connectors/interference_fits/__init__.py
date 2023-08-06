'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1227 import AssemblyMethods
    from ._1228 import CalculationMethods
    from ._1229 import InterferenceFitDesign
    from ._1230 import InterferenceFitHalfDesign
    from ._1231 import StressRegions
    from ._1232 import Table4JointInterfaceTypes
