'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2057 import ClutchConnection
    from ._2058 import ClutchSocket
    from ._2059 import ConceptCouplingConnection
    from ._2060 import ConceptCouplingSocket
    from ._2061 import CouplingConnection
    from ._2062 import CouplingSocket
    from ._2063 import PartToPartShearCouplingConnection
    from ._2064 import PartToPartShearCouplingSocket
    from ._2065 import SpringDamperConnection
    from ._2066 import SpringDamperSocket
    from ._2067 import TorqueConverterConnection
    from ._2068 import TorqueConverterPumpSocket
    from ._2069 import TorqueConverterTurbineSocket
