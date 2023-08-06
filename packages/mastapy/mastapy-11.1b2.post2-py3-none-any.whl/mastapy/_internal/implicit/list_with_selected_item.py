'''list_with_selected_item.py

Implementations of 'ListWithSelectedItem' in Python.
As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
'''


from typing import List, Generic, TypeVar

from mastapy._internal import mixins, constructor, conversion
from mastapy._internal.python_net import python_net_import
from mastapy.gears.ltca.cylindrical import _800, _799
from mastapy.gears.manufacturing.cylindrical import _579
from mastapy.gears.manufacturing.bevel import _745
from mastapy.utility import _1377
from mastapy.utility.units_and_measurements import (
    _1387, _1379, _1380, _1381,
    _1385, _1386, _1388, _1382
)
from mastapy._internal.cast_exception import CastException
from mastapy.utility.units_and_measurements.measurements import (
    _1389, _1390, _1391, _1392,
    _1393, _1394, _1395, _1396,
    _1397, _1398, _1399, _1400,
    _1401, _1402, _1403, _1404,
    _1405, _1406, _1407, _1408,
    _1409, _1410, _1411, _1412,
    _1413, _1414, _1415, _1416,
    _1417, _1418, _1419, _1420,
    _1421, _1422, _1423, _1424,
    _1425, _1426, _1427, _1428,
    _1429, _1430, _1431, _1432,
    _1433, _1434, _1435, _1436,
    _1437, _1438, _1439, _1440,
    _1441, _1442, _1443, _1444,
    _1445, _1446, _1447, _1448,
    _1449, _1450, _1451, _1452,
    _1453, _1454, _1455, _1456,
    _1457, _1458, _1459, _1460,
    _1461, _1462, _1463, _1464,
    _1465, _1466, _1467, _1468,
    _1469, _1470, _1471, _1472,
    _1473, _1474, _1475, _1476,
    _1477, _1478, _1479, _1480,
    _1481, _1482, _1483, _1484,
    _1485, _1486, _1487, _1488,
    _1489, _1490, _1491, _1492,
    _1493, _1494, _1495, _1496
)
from mastapy.utility.file_access_helpers import _1568
from mastapy.system_model.part_model import (
    _2186, _2163, _2159, _2151,
    _2152, _2155, _2157, _2162,
    _2166, _2167, _2169, _2176,
    _2177, _2178, _2180, _2183,
    _2185, _2191, _2193
)
from mastapy.system_model.analyses_and_results.harmonic_analyses import (
    _5636, _5689, _5690, _5691,
    _5692, _5693, _5694, _5695,
    _5696, _5697, _5698, _5699,
    _5709, _5711, _5712, _5714,
    _5743, _5759, _5784
)
from mastapy._internal.tuple_with_name import TupleWithName
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2467, _2402, _2409, _2414,
    _2428, _2432, _2447, _2448,
    _2449, _2462, _2471, _2476,
    _2479, _2482, _2515, _2521,
    _2524, _2544, _2547, _2453,
    _2454, _2455, _2458
)
from mastapy.system_model.part_model.gears import (
    _2245, _2227, _2229, _2233,
    _2235, _2237, _2239, _2242,
    _2248, _2250, _2252, _2254,
    _2255, _2257, _2259, _2261,
    _2265, _2267, _2226, _2228,
    _2230, _2231, _2232, _2234,
    _2236, _2238, _2240, _2241,
    _2243, _2247, _2249, _2251,
    _2253, _2256, _2258, _2260,
    _2262, _2263, _2264, _2266
)
from mastapy.system_model.fe import _2099, _2097, _2088
from mastapy.system_model.part_model.shaft_model import _2196
from mastapy.system_model.part_model.cycloidal import _2282, _2283
from mastapy.system_model.part_model.couplings import (
    _2292, _2295, _2297, _2300,
    _2302, _2303, _2309, _2311,
    _2314, _2317, _2318, _2319,
    _2321, _2323
)
from mastapy.system_model.fe.links import (
    _2132, _2133, _2135, _2136,
    _2137, _2138, _2139, _2140,
    _2141, _2142, _2143, _2144,
    _2145, _2146
)
from mastapy.system_model.part_model.part_groups import _2201
from mastapy.gears.gear_designs import _890
from mastapy.gears.gear_designs.zerol_bevel import _894
from mastapy.gears.gear_designs.worm import _899
from mastapy.gears.gear_designs.straight_bevel_diff import _903
from mastapy.gears.gear_designs.straight_bevel import _907
from mastapy.gears.gear_designs.spiral_bevel import _911
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _915
from mastapy.gears.gear_designs.klingelnberg_hypoid import _919
from mastapy.gears.gear_designs.klingelnberg_conical import _923
from mastapy.gears.gear_designs.hypoid import _927
from mastapy.gears.gear_designs.face import _935
from mastapy.gears.gear_designs.cylindrical import _967, _978
from mastapy.gears.gear_designs.conical import _1087
from mastapy.gears.gear_designs.concept import _1109
from mastapy.gears.gear_designs.bevel import _1113
from mastapy.gears.gear_designs.agma_gleason_conical import _1126
from mastapy.system_model.analyses_and_results.load_case_groups import _5361, _5362
from mastapy.system_model.analyses_and_results.harmonic_analyses.results import _5800
from mastapy.system_model.analyses_and_results.static_loads import _6492, _6499
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4091

_ARRAY = python_net_import('System', 'Array')
_LIST_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.Utility.Property', 'ListWithSelectedItem')


__docformat__ = 'restructuredtext en'
__all__ = (
    'ListWithSelectedItem_str', 'ListWithSelectedItem_int',
    'ListWithSelectedItem_T', 'ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis',
    'ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis', 'ListWithSelectedItem_CylindricalSetManufacturingConfig',
    'ListWithSelectedItem_ConicalSetManufacturingConfig', 'ListWithSelectedItem_SystemDirectory',
    'ListWithSelectedItem_Unit', 'ListWithSelectedItem_MeasurementBase',
    'ListWithSelectedItem_ColumnTitle', 'ListWithSelectedItem_PowerLoad',
    'ListWithSelectedItem_AbstractPeriodicExcitationDetail', 'ListWithSelectedItem_TupleWithName',
    'ListWithSelectedItem_GearMeshSystemDeflection', 'ListWithSelectedItem_GearSet',
    'ListWithSelectedItem_FESubstructureNode', 'ListWithSelectedItem_Datum',
    'ListWithSelectedItem_Component', 'ListWithSelectedItem_FELink',
    'ListWithSelectedItem_FESubstructure', 'ListWithSelectedItem_CylindricalGear',
    'ListWithSelectedItem_GuideDxfModel', 'ListWithSelectedItem_ConcentricPartGroup',
    'ListWithSelectedItem_CylindricalGearSet', 'ListWithSelectedItem_GearSetDesign',
    'ListWithSelectedItem_ShaftHubConnection', 'ListWithSelectedItem_TSelectableItem',
    'ListWithSelectedItem_CylindricalGearSystemDeflection', 'ListWithSelectedItem_DesignState',
    'ListWithSelectedItem_FEPart', 'ListWithSelectedItem_TPartAnalysis',
    'ListWithSelectedItem_ResultLocationSelectionGroup', 'ListWithSelectedItem_StaticLoadCase',
    'ListWithSelectedItem_DutyCycle', 'ListWithSelectedItem_float',
    'ListWithSelectedItem_ElectricMachineDataSet', 'ListWithSelectedItem_PointLoad'
)


T = TypeVar('T')
TSelectableItem = TypeVar('TSelectableItem')
TPartAnalysis = TypeVar('TPartAnalysis')


class ListWithSelectedItem_str(str, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_str

    A specific implementation of 'ListWithSelectedItem' for 'str' types.
    '''

    __hash__ = None
    __qualname__ = 'str'

    def __new__(cls, instance_to_wrap: 'ListWithSelectedItem_str.TYPE'):
        return str.__new__(cls, instance_to_wrap.SelectedValue if instance_to_wrap.SelectedValue is not None else '')

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_str.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'str':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return str

    @property
    def selected_value(self) -> 'str':
        '''str: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[str]':
        '''List[str]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, str)
        return value


class ListWithSelectedItem_int(int, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_int

    A specific implementation of 'ListWithSelectedItem' for 'int' types.
    '''

    __hash__ = None
    __qualname__ = 'int'

    def __new__(cls, instance_to_wrap: 'ListWithSelectedItem_int.TYPE'):
        return int.__new__(cls, instance_to_wrap.SelectedValue if instance_to_wrap.SelectedValue is not None else 0)

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_int.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'int':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return int

    @property
    def selected_value(self) -> 'int':
        '''int: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[int]':
        '''List[int]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, int)
        return value


class ListWithSelectedItem_T(Generic[T], mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_T

    A specific implementation of 'ListWithSelectedItem' for 'T' types.
    '''

    __hash__ = None
    __qualname__ = 'T'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_T.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'T':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return T

    @property
    def selected_value(self) -> 'T':
        '''T: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[T]':
        '''List[T]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues)
        return value


class ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis(_800.CylindricalGearMeshLoadDistributionAnalysis, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearMeshLoadDistributionAnalysis' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearMeshLoadDistributionAnalysis'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_800.CylindricalGearMeshLoadDistributionAnalysis.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _800.CylindricalGearMeshLoadDistributionAnalysis.TYPE

    @property
    def selected_value(self) -> '_800.CylindricalGearMeshLoadDistributionAnalysis':
        '''CylindricalGearMeshLoadDistributionAnalysis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_800.CylindricalGearMeshLoadDistributionAnalysis)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_800.CylindricalGearMeshLoadDistributionAnalysis]':
        '''List[CylindricalGearMeshLoadDistributionAnalysis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_800.CylindricalGearMeshLoadDistributionAnalysis))
        return value


class ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis(_799.CylindricalGearLoadDistributionAnalysis, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearLoadDistributionAnalysis' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearLoadDistributionAnalysis'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_799.CylindricalGearLoadDistributionAnalysis.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _799.CylindricalGearLoadDistributionAnalysis.TYPE

    @property
    def selected_value(self) -> '_799.CylindricalGearLoadDistributionAnalysis':
        '''CylindricalGearLoadDistributionAnalysis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_799.CylindricalGearLoadDistributionAnalysis)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_799.CylindricalGearLoadDistributionAnalysis]':
        '''List[CylindricalGearLoadDistributionAnalysis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_799.CylindricalGearLoadDistributionAnalysis))
        return value


class ListWithSelectedItem_CylindricalSetManufacturingConfig(_579.CylindricalSetManufacturingConfig, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalSetManufacturingConfig

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalSetManufacturingConfig' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalSetManufacturingConfig'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalSetManufacturingConfig.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_579.CylindricalSetManufacturingConfig.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _579.CylindricalSetManufacturingConfig.TYPE

    @property
    def selected_value(self) -> '_579.CylindricalSetManufacturingConfig':
        '''CylindricalSetManufacturingConfig: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_579.CylindricalSetManufacturingConfig)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_579.CylindricalSetManufacturingConfig]':
        '''List[CylindricalSetManufacturingConfig]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_579.CylindricalSetManufacturingConfig))
        return value


class ListWithSelectedItem_ConicalSetManufacturingConfig(_745.ConicalSetManufacturingConfig, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ConicalSetManufacturingConfig

    A specific implementation of 'ListWithSelectedItem' for 'ConicalSetManufacturingConfig' types.
    '''

    __hash__ = None
    __qualname__ = 'ConicalSetManufacturingConfig'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ConicalSetManufacturingConfig.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_745.ConicalSetManufacturingConfig.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _745.ConicalSetManufacturingConfig.TYPE

    @property
    def selected_value(self) -> '_745.ConicalSetManufacturingConfig':
        '''ConicalSetManufacturingConfig: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_745.ConicalSetManufacturingConfig)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_745.ConicalSetManufacturingConfig]':
        '''List[ConicalSetManufacturingConfig]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_745.ConicalSetManufacturingConfig))
        return value


class ListWithSelectedItem_SystemDirectory(_1377.SystemDirectory, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_SystemDirectory

    A specific implementation of 'ListWithSelectedItem' for 'SystemDirectory' types.
    '''

    __hash__ = None
    __qualname__ = 'SystemDirectory'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_SystemDirectory.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_1377.SystemDirectory.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1377.SystemDirectory.TYPE

    @property
    def selected_value(self) -> '_1377.SystemDirectory':
        '''SystemDirectory: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1377.SystemDirectory)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_1377.SystemDirectory]':
        '''List[SystemDirectory]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1377.SystemDirectory))
        return value


class ListWithSelectedItem_Unit(_1387.Unit, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_Unit

    A specific implementation of 'ListWithSelectedItem' for 'Unit' types.
    '''

    __hash__ = None
    __qualname__ = 'Unit'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_Unit.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_1387.Unit.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1387.Unit.TYPE

    @property
    def selected_value(self) -> '_1387.Unit':
        '''Unit: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1387.Unit.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Unit. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_1387.Unit]':
        '''List[Unit]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1387.Unit))
        return value


class ListWithSelectedItem_MeasurementBase(_1382.MeasurementBase, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_MeasurementBase

    A specific implementation of 'ListWithSelectedItem' for 'MeasurementBase' types.
    '''

    __hash__ = None
    __qualname__ = 'MeasurementBase'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_MeasurementBase.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_1382.MeasurementBase.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1382.MeasurementBase.TYPE

    @property
    def selected_value(self) -> '_1382.MeasurementBase':
        '''MeasurementBase: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1382.MeasurementBase.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MeasurementBase. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_acceleration(self) -> '_1389.Acceleration':
        '''Acceleration: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1389.Acceleration.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Acceleration. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angle(self) -> '_1390.Angle':
        '''Angle: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1390.Angle.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Angle. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angle_per_unit_temperature(self) -> '_1391.AnglePerUnitTemperature':
        '''AnglePerUnitTemperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1391.AnglePerUnitTemperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AnglePerUnitTemperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angle_small(self) -> '_1392.AngleSmall':
        '''AngleSmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1392.AngleSmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngleSmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angle_very_small(self) -> '_1393.AngleVerySmall':
        '''AngleVerySmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1393.AngleVerySmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngleVerySmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angular_acceleration(self) -> '_1394.AngularAcceleration':
        '''AngularAcceleration: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1394.AngularAcceleration.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularAcceleration. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angular_compliance(self) -> '_1395.AngularCompliance':
        '''AngularCompliance: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1395.AngularCompliance.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularCompliance. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angular_jerk(self) -> '_1396.AngularJerk':
        '''AngularJerk: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1396.AngularJerk.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularJerk. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angular_stiffness(self) -> '_1397.AngularStiffness':
        '''AngularStiffness: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1397.AngularStiffness.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularStiffness. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_angular_velocity(self) -> '_1398.AngularVelocity':
        '''AngularVelocity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1398.AngularVelocity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularVelocity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_area(self) -> '_1399.Area':
        '''Area: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1399.Area.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Area. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_area_small(self) -> '_1400.AreaSmall':
        '''AreaSmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1400.AreaSmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AreaSmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cycles(self) -> '_1401.Cycles':
        '''Cycles: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1401.Cycles.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Cycles. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_damage(self) -> '_1402.Damage':
        '''Damage: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1402.Damage.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Damage. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_damage_rate(self) -> '_1403.DamageRate':
        '''DamageRate: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1403.DamageRate.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to DamageRate. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_data_size(self) -> '_1404.DataSize':
        '''DataSize: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1404.DataSize.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to DataSize. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_decibel(self) -> '_1405.Decibel':
        '''Decibel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1405.Decibel.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Decibel. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_density(self) -> '_1406.Density':
        '''Density: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1406.Density.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Density. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_energy(self) -> '_1407.Energy':
        '''Energy: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1407.Energy.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Energy. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_energy_per_unit_area(self) -> '_1408.EnergyPerUnitArea':
        '''EnergyPerUnitArea: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1408.EnergyPerUnitArea.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to EnergyPerUnitArea. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_energy_per_unit_area_small(self) -> '_1409.EnergyPerUnitAreaSmall':
        '''EnergyPerUnitAreaSmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1409.EnergyPerUnitAreaSmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to EnergyPerUnitAreaSmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_energy_small(self) -> '_1410.EnergySmall':
        '''EnergySmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1410.EnergySmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to EnergySmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_enum(self) -> '_1411.Enum':
        '''Enum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1411.Enum.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Enum. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_flow_rate(self) -> '_1412.FlowRate':
        '''FlowRate: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1412.FlowRate.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FlowRate. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_force(self) -> '_1413.Force':
        '''Force: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1413.Force.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Force. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_force_per_unit_length(self) -> '_1414.ForcePerUnitLength':
        '''ForcePerUnitLength: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1414.ForcePerUnitLength.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ForcePerUnitLength. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_force_per_unit_pressure(self) -> '_1415.ForcePerUnitPressure':
        '''ForcePerUnitPressure: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1415.ForcePerUnitPressure.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ForcePerUnitPressure. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_force_per_unit_temperature(self) -> '_1416.ForcePerUnitTemperature':
        '''ForcePerUnitTemperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1416.ForcePerUnitTemperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ForcePerUnitTemperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_fraction_measurement_base(self) -> '_1417.FractionMeasurementBase':
        '''FractionMeasurementBase: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1417.FractionMeasurementBase.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FractionMeasurementBase. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_frequency(self) -> '_1418.Frequency':
        '''Frequency: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1418.Frequency.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Frequency. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_fuel_consumption_engine(self) -> '_1419.FuelConsumptionEngine':
        '''FuelConsumptionEngine: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1419.FuelConsumptionEngine.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FuelConsumptionEngine. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_fuel_efficiency_vehicle(self) -> '_1420.FuelEfficiencyVehicle':
        '''FuelEfficiencyVehicle: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1420.FuelEfficiencyVehicle.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FuelEfficiencyVehicle. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_gradient(self) -> '_1421.Gradient':
        '''Gradient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1421.Gradient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Gradient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_heat_conductivity(self) -> '_1422.HeatConductivity':
        '''HeatConductivity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1422.HeatConductivity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HeatConductivity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_heat_transfer(self) -> '_1423.HeatTransfer':
        '''HeatTransfer: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1423.HeatTransfer.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HeatTransfer. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_heat_transfer_coefficient_for_plastic_gear_tooth(self) -> '_1424.HeatTransferCoefficientForPlasticGearTooth':
        '''HeatTransferCoefficientForPlasticGearTooth: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1424.HeatTransferCoefficientForPlasticGearTooth.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HeatTransferCoefficientForPlasticGearTooth. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_heat_transfer_resistance(self) -> '_1425.HeatTransferResistance':
        '''HeatTransferResistance: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1425.HeatTransferResistance.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HeatTransferResistance. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_impulse(self) -> '_1426.Impulse':
        '''Impulse: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1426.Impulse.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Impulse. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_index(self) -> '_1427.Index':
        '''Index: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1427.Index.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Index. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_integer(self) -> '_1428.Integer':
        '''Integer: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1428.Integer.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Integer. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_inverse_short_length(self) -> '_1429.InverseShortLength':
        '''InverseShortLength: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1429.InverseShortLength.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to InverseShortLength. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_inverse_short_time(self) -> '_1430.InverseShortTime':
        '''InverseShortTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1430.InverseShortTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to InverseShortTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_jerk(self) -> '_1431.Jerk':
        '''Jerk: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1431.Jerk.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Jerk. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_kinematic_viscosity(self) -> '_1432.KinematicViscosity':
        '''KinematicViscosity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1432.KinematicViscosity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KinematicViscosity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_length_long(self) -> '_1433.LengthLong':
        '''LengthLong: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1433.LengthLong.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthLong. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_length_medium(self) -> '_1434.LengthMedium':
        '''LengthMedium: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1434.LengthMedium.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthMedium. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_length_per_unit_temperature(self) -> '_1435.LengthPerUnitTemperature':
        '''LengthPerUnitTemperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1435.LengthPerUnitTemperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthPerUnitTemperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_length_short(self) -> '_1436.LengthShort':
        '''LengthShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1436.LengthShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_length_to_the_fourth(self) -> '_1437.LengthToTheFourth':
        '''LengthToTheFourth: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1437.LengthToTheFourth.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthToTheFourth. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_length_very_long(self) -> '_1438.LengthVeryLong':
        '''LengthVeryLong: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1438.LengthVeryLong.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthVeryLong. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_length_very_short(self) -> '_1439.LengthVeryShort':
        '''LengthVeryShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1439.LengthVeryShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthVeryShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_length_very_short_per_length_short(self) -> '_1440.LengthVeryShortPerLengthShort':
        '''LengthVeryShortPerLengthShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1440.LengthVeryShortPerLengthShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthVeryShortPerLengthShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_linear_angular_damping(self) -> '_1441.LinearAngularDamping':
        '''LinearAngularDamping: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1441.LinearAngularDamping.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearAngularDamping. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_linear_angular_stiffness_cross_term(self) -> '_1442.LinearAngularStiffnessCrossTerm':
        '''LinearAngularStiffnessCrossTerm: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1442.LinearAngularStiffnessCrossTerm.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearAngularStiffnessCrossTerm. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_linear_damping(self) -> '_1443.LinearDamping':
        '''LinearDamping: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1443.LinearDamping.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearDamping. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_linear_flexibility(self) -> '_1444.LinearFlexibility':
        '''LinearFlexibility: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1444.LinearFlexibility.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearFlexibility. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_linear_stiffness(self) -> '_1445.LinearStiffness':
        '''LinearStiffness: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1445.LinearStiffness.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearStiffness. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_mass(self) -> '_1446.Mass':
        '''Mass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1446.Mass.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Mass. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_mass_per_unit_length(self) -> '_1447.MassPerUnitLength':
        '''MassPerUnitLength: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1447.MassPerUnitLength.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MassPerUnitLength. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_mass_per_unit_time(self) -> '_1448.MassPerUnitTime':
        '''MassPerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1448.MassPerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MassPerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_moment_of_inertia(self) -> '_1449.MomentOfInertia':
        '''MomentOfInertia: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1449.MomentOfInertia.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MomentOfInertia. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_moment_of_inertia_per_unit_length(self) -> '_1450.MomentOfInertiaPerUnitLength':
        '''MomentOfInertiaPerUnitLength: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1450.MomentOfInertiaPerUnitLength.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MomentOfInertiaPerUnitLength. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_moment_per_unit_pressure(self) -> '_1451.MomentPerUnitPressure':
        '''MomentPerUnitPressure: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1451.MomentPerUnitPressure.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MomentPerUnitPressure. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_number(self) -> '_1452.Number':
        '''Number: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1452.Number.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Number. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_percentage(self) -> '_1453.Percentage':
        '''Percentage: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1453.Percentage.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Percentage. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_power(self) -> '_1454.Power':
        '''Power: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1454.Power.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Power. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_power_per_small_area(self) -> '_1455.PowerPerSmallArea':
        '''PowerPerSmallArea: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1455.PowerPerSmallArea.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerPerSmallArea. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_power_per_unit_time(self) -> '_1456.PowerPerUnitTime':
        '''PowerPerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1456.PowerPerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerPerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_power_small(self) -> '_1457.PowerSmall':
        '''PowerSmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1457.PowerSmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerSmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_power_small_per_area(self) -> '_1458.PowerSmallPerArea':
        '''PowerSmallPerArea: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1458.PowerSmallPerArea.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerSmallPerArea. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_power_small_per_unit_area_per_unit_time(self) -> '_1459.PowerSmallPerUnitAreaPerUnitTime':
        '''PowerSmallPerUnitAreaPerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1459.PowerSmallPerUnitAreaPerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerSmallPerUnitAreaPerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_power_small_per_unit_time(self) -> '_1460.PowerSmallPerUnitTime':
        '''PowerSmallPerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1460.PowerSmallPerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerSmallPerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_pressure(self) -> '_1461.Pressure':
        '''Pressure: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1461.Pressure.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Pressure. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_pressure_per_unit_time(self) -> '_1462.PressurePerUnitTime':
        '''PressurePerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1462.PressurePerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PressurePerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_pressure_velocity_product(self) -> '_1463.PressureVelocityProduct':
        '''PressureVelocityProduct: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1463.PressureVelocityProduct.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PressureVelocityProduct. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_pressure_viscosity_coefficient(self) -> '_1464.PressureViscosityCoefficient':
        '''PressureViscosityCoefficient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1464.PressureViscosityCoefficient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PressureViscosityCoefficient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_price(self) -> '_1465.Price':
        '''Price: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1465.Price.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Price. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_quadratic_angular_damping(self) -> '_1466.QuadraticAngularDamping':
        '''QuadraticAngularDamping: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1466.QuadraticAngularDamping.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to QuadraticAngularDamping. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_quadratic_drag(self) -> '_1467.QuadraticDrag':
        '''QuadraticDrag: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1467.QuadraticDrag.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to QuadraticDrag. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_rescaled_measurement(self) -> '_1468.RescaledMeasurement':
        '''RescaledMeasurement: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1468.RescaledMeasurement.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to RescaledMeasurement. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_rotatum(self) -> '_1469.Rotatum':
        '''Rotatum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1469.Rotatum.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Rotatum. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_safety_factor(self) -> '_1470.SafetyFactor':
        '''SafetyFactor: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1470.SafetyFactor.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SafetyFactor. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_specific_acoustic_impedance(self) -> '_1471.SpecificAcousticImpedance':
        '''SpecificAcousticImpedance: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1471.SpecificAcousticImpedance.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpecificAcousticImpedance. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_specific_heat(self) -> '_1472.SpecificHeat':
        '''SpecificHeat: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1472.SpecificHeat.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpecificHeat. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_square_root_of_unit_force_per_unit_area(self) -> '_1473.SquareRootOfUnitForcePerUnitArea':
        '''SquareRootOfUnitForcePerUnitArea: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1473.SquareRootOfUnitForcePerUnitArea.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SquareRootOfUnitForcePerUnitArea. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_stiffness_per_unit_face_width(self) -> '_1474.StiffnessPerUnitFaceWidth':
        '''StiffnessPerUnitFaceWidth: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1474.StiffnessPerUnitFaceWidth.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StiffnessPerUnitFaceWidth. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_stress(self) -> '_1475.Stress':
        '''Stress: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1475.Stress.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Stress. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_temperature(self) -> '_1476.Temperature':
        '''Temperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1476.Temperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Temperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_temperature_difference(self) -> '_1477.TemperatureDifference':
        '''TemperatureDifference: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1477.TemperatureDifference.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TemperatureDifference. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_temperature_per_unit_time(self) -> '_1478.TemperaturePerUnitTime':
        '''TemperaturePerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1478.TemperaturePerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TemperaturePerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_text(self) -> '_1479.Text':
        '''Text: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1479.Text.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Text. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_thermal_contact_coefficient(self) -> '_1480.ThermalContactCoefficient':
        '''ThermalContactCoefficient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1480.ThermalContactCoefficient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ThermalContactCoefficient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_thermal_expansion_coefficient(self) -> '_1481.ThermalExpansionCoefficient':
        '''ThermalExpansionCoefficient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1481.ThermalExpansionCoefficient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ThermalExpansionCoefficient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_thermo_elastic_factor(self) -> '_1482.ThermoElasticFactor':
        '''ThermoElasticFactor: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1482.ThermoElasticFactor.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ThermoElasticFactor. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_time(self) -> '_1483.Time':
        '''Time: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1483.Time.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Time. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_time_short(self) -> '_1484.TimeShort':
        '''TimeShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1484.TimeShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TimeShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_time_very_short(self) -> '_1485.TimeVeryShort':
        '''TimeVeryShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1485.TimeVeryShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TimeVeryShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_torque(self) -> '_1486.Torque':
        '''Torque: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1486.Torque.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Torque. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_torque_converter_inverse_k(self) -> '_1487.TorqueConverterInverseK':
        '''TorqueConverterInverseK: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1487.TorqueConverterInverseK.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorqueConverterInverseK. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_torque_converter_k(self) -> '_1488.TorqueConverterK':
        '''TorqueConverterK: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1488.TorqueConverterK.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorqueConverterK. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_torque_per_unit_temperature(self) -> '_1489.TorquePerUnitTemperature':
        '''TorquePerUnitTemperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1489.TorquePerUnitTemperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorquePerUnitTemperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_velocity(self) -> '_1490.Velocity':
        '''Velocity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1490.Velocity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Velocity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_velocity_small(self) -> '_1491.VelocitySmall':
        '''VelocitySmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1491.VelocitySmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to VelocitySmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_viscosity(self) -> '_1492.Viscosity':
        '''Viscosity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1492.Viscosity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Viscosity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_voltage(self) -> '_1493.Voltage':
        '''Voltage: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1493.Voltage.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Voltage. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_volume(self) -> '_1494.Volume':
        '''Volume: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1494.Volume.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Volume. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_wear_coefficient(self) -> '_1495.WearCoefficient':
        '''WearCoefficient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1495.WearCoefficient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WearCoefficient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_yank(self) -> '_1496.Yank':
        '''Yank: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1496.Yank.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Yank. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_1382.MeasurementBase]':
        '''List[MeasurementBase]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1382.MeasurementBase))
        return value


class ListWithSelectedItem_ColumnTitle(_1568.ColumnTitle, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ColumnTitle

    A specific implementation of 'ListWithSelectedItem' for 'ColumnTitle' types.
    '''

    __hash__ = None
    __qualname__ = 'ColumnTitle'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ColumnTitle.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_1568.ColumnTitle.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1568.ColumnTitle.TYPE

    @property
    def selected_value(self) -> '_1568.ColumnTitle':
        '''ColumnTitle: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1568.ColumnTitle)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_1568.ColumnTitle]':
        '''List[ColumnTitle]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1568.ColumnTitle))
        return value


class ListWithSelectedItem_PowerLoad(_2186.PowerLoad, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_PowerLoad

    A specific implementation of 'ListWithSelectedItem' for 'PowerLoad' types.
    '''

    __hash__ = None
    __qualname__ = 'PowerLoad'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_PowerLoad.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2186.PowerLoad.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2186.PowerLoad.TYPE

    @property
    def selected_value(self) -> '_2186.PowerLoad':
        '''PowerLoad: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2186.PowerLoad)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2186.PowerLoad]':
        '''List[PowerLoad]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2186.PowerLoad))
        return value


class ListWithSelectedItem_AbstractPeriodicExcitationDetail(_5636.AbstractPeriodicExcitationDetail, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_AbstractPeriodicExcitationDetail

    A specific implementation of 'ListWithSelectedItem' for 'AbstractPeriodicExcitationDetail' types.
    '''

    __hash__ = None
    __qualname__ = 'AbstractPeriodicExcitationDetail'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_AbstractPeriodicExcitationDetail.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_5636.AbstractPeriodicExcitationDetail.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5636.AbstractPeriodicExcitationDetail.TYPE

    @property
    def selected_value(self) -> '_5636.AbstractPeriodicExcitationDetail':
        '''AbstractPeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5636.AbstractPeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AbstractPeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_periodic_excitation_detail(self) -> '_5689.ElectricMachinePeriodicExcitationDetail':
        '''ElectricMachinePeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5689.ElectricMachinePeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachinePeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_rotor_x_force_periodic_excitation_detail(self) -> '_5690.ElectricMachineRotorXForcePeriodicExcitationDetail':
        '''ElectricMachineRotorXForcePeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5690.ElectricMachineRotorXForcePeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineRotorXForcePeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_rotor_x_moment_periodic_excitation_detail(self) -> '_5691.ElectricMachineRotorXMomentPeriodicExcitationDetail':
        '''ElectricMachineRotorXMomentPeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5691.ElectricMachineRotorXMomentPeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineRotorXMomentPeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_rotor_y_force_periodic_excitation_detail(self) -> '_5692.ElectricMachineRotorYForcePeriodicExcitationDetail':
        '''ElectricMachineRotorYForcePeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5692.ElectricMachineRotorYForcePeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineRotorYForcePeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_rotor_y_moment_periodic_excitation_detail(self) -> '_5693.ElectricMachineRotorYMomentPeriodicExcitationDetail':
        '''ElectricMachineRotorYMomentPeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5693.ElectricMachineRotorYMomentPeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineRotorYMomentPeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_rotor_z_force_periodic_excitation_detail(self) -> '_5694.ElectricMachineRotorZForcePeriodicExcitationDetail':
        '''ElectricMachineRotorZForcePeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5694.ElectricMachineRotorZForcePeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineRotorZForcePeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_stator_tooth_axial_loads_excitation_detail(self) -> '_5695.ElectricMachineStatorToothAxialLoadsExcitationDetail':
        '''ElectricMachineStatorToothAxialLoadsExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5695.ElectricMachineStatorToothAxialLoadsExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineStatorToothAxialLoadsExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_stator_tooth_loads_excitation_detail(self) -> '_5696.ElectricMachineStatorToothLoadsExcitationDetail':
        '''ElectricMachineStatorToothLoadsExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5696.ElectricMachineStatorToothLoadsExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineStatorToothLoadsExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_stator_tooth_radial_loads_excitation_detail(self) -> '_5697.ElectricMachineStatorToothRadialLoadsExcitationDetail':
        '''ElectricMachineStatorToothRadialLoadsExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5697.ElectricMachineStatorToothRadialLoadsExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineStatorToothRadialLoadsExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_stator_tooth_tangential_loads_excitation_detail(self) -> '_5698.ElectricMachineStatorToothTangentialLoadsExcitationDetail':
        '''ElectricMachineStatorToothTangentialLoadsExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5698.ElectricMachineStatorToothTangentialLoadsExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineStatorToothTangentialLoadsExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_torque_ripple_periodic_excitation_detail(self) -> '_5699.ElectricMachineTorqueRipplePeriodicExcitationDetail':
        '''ElectricMachineTorqueRipplePeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5699.ElectricMachineTorqueRipplePeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineTorqueRipplePeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_gear_mesh_excitation_detail(self) -> '_5709.GearMeshExcitationDetail':
        '''GearMeshExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5709.GearMeshExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearMeshExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_gear_mesh_misalignment_excitation_detail(self) -> '_5711.GearMeshMisalignmentExcitationDetail':
        '''GearMeshMisalignmentExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5711.GearMeshMisalignmentExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearMeshMisalignmentExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_gear_mesh_te_excitation_detail(self) -> '_5712.GearMeshTEExcitationDetail':
        '''GearMeshTEExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5712.GearMeshTEExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearMeshTEExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_general_periodic_excitation_detail(self) -> '_5714.GeneralPeriodicExcitationDetail':
        '''GeneralPeriodicExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5714.GeneralPeriodicExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GeneralPeriodicExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_periodic_excitation_with_reference_shaft(self) -> '_5743.PeriodicExcitationWithReferenceShaft':
        '''PeriodicExcitationWithReferenceShaft: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5743.PeriodicExcitationWithReferenceShaft.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PeriodicExcitationWithReferenceShaft. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_single_node_periodic_excitation_with_reference_shaft(self) -> '_5759.SingleNodePeriodicExcitationWithReferenceShaft':
        '''SingleNodePeriodicExcitationWithReferenceShaft: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5759.SingleNodePeriodicExcitationWithReferenceShaft.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SingleNodePeriodicExcitationWithReferenceShaft. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_unbalanced_mass_excitation_detail(self) -> '_5784.UnbalancedMassExcitationDetail':
        '''UnbalancedMassExcitationDetail: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5784.UnbalancedMassExcitationDetail.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to UnbalancedMassExcitationDetail. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_5636.AbstractPeriodicExcitationDetail]':
        '''List[AbstractPeriodicExcitationDetail]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_5636.AbstractPeriodicExcitationDetail))
        return value


class ListWithSelectedItem_TupleWithName(TupleWithName, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_TupleWithName

    A specific implementation of 'ListWithSelectedItem' for 'TupleWithName' types.
    '''

    __hash__ = None
    __qualname__ = 'TupleWithName'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_TupleWithName.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'TupleWithName.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return TupleWithName.TYPE

    @property
    def selected_value(self) -> 'TupleWithName':
        '''TupleWithName: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_tuple_with_name(self.enclosing.SelectedValue, (None))
        return constructor.new(TupleWithName)(value) if value is not None else None

    @property
    def available_values(self) -> 'TupleWithName':
        '''TupleWithName: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(TupleWithName))
        return constructor.new(TupleWithName)(value) if value is not None else None


class ListWithSelectedItem_GearMeshSystemDeflection(_2467.GearMeshSystemDeflection, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_GearMeshSystemDeflection

    A specific implementation of 'ListWithSelectedItem' for 'GearMeshSystemDeflection' types.
    '''

    __hash__ = None
    __qualname__ = 'GearMeshSystemDeflection'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_GearMeshSystemDeflection.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2467.GearMeshSystemDeflection.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2467.GearMeshSystemDeflection.TYPE

    @property
    def selected_value(self) -> '_2467.GearMeshSystemDeflection':
        '''GearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2467.GearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_agma_gleason_conical_gear_mesh_system_deflection(self) -> '_2402.AGMAGleasonConicalGearMeshSystemDeflection':
        '''AGMAGleasonConicalGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2402.AGMAGleasonConicalGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AGMAGleasonConicalGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_differential_gear_mesh_system_deflection(self) -> '_2409.BevelDifferentialGearMeshSystemDeflection':
        '''BevelDifferentialGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2409.BevelDifferentialGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_gear_mesh_system_deflection(self) -> '_2414.BevelGearMeshSystemDeflection':
        '''BevelGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2414.BevelGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_concept_gear_mesh_system_deflection(self) -> '_2428.ConceptGearMeshSystemDeflection':
        '''ConceptGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2428.ConceptGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_conical_gear_mesh_system_deflection(self) -> '_2432.ConicalGearMeshSystemDeflection':
        '''ConicalGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2432.ConicalGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConicalGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_gear_mesh_system_deflection(self) -> '_2447.CylindricalGearMeshSystemDeflection':
        '''CylindricalGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2447.CylindricalGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_gear_mesh_system_deflection_timestep(self) -> '_2448.CylindricalGearMeshSystemDeflectionTimestep':
        '''CylindricalGearMeshSystemDeflectionTimestep: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2448.CylindricalGearMeshSystemDeflectionTimestep.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearMeshSystemDeflectionTimestep. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_gear_mesh_system_deflection_with_ltca_results(self) -> '_2449.CylindricalGearMeshSystemDeflectionWithLTCAResults':
        '''CylindricalGearMeshSystemDeflectionWithLTCAResults: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2449.CylindricalGearMeshSystemDeflectionWithLTCAResults.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearMeshSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_face_gear_mesh_system_deflection(self) -> '_2462.FaceGearMeshSystemDeflection':
        '''FaceGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2462.FaceGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FaceGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_hypoid_gear_mesh_system_deflection(self) -> '_2471.HypoidGearMeshSystemDeflection':
        '''HypoidGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2471.HypoidGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HypoidGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh_system_deflection(self) -> '_2476.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidConicalGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2476.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidConicalGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_system_deflection(self) -> '_2479.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2479.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_system_deflection(self) -> '_2482.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2482.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_spiral_bevel_gear_mesh_system_deflection(self) -> '_2515.SpiralBevelGearMeshSystemDeflection':
        '''SpiralBevelGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2515.SpiralBevelGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_diff_gear_mesh_system_deflection(self) -> '_2521.StraightBevelDiffGearMeshSystemDeflection':
        '''StraightBevelDiffGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2521.StraightBevelDiffGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelDiffGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_gear_mesh_system_deflection(self) -> '_2524.StraightBevelGearMeshSystemDeflection':
        '''StraightBevelGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2524.StraightBevelGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_worm_gear_mesh_system_deflection(self) -> '_2544.WormGearMeshSystemDeflection':
        '''WormGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2544.WormGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WormGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_zerol_bevel_gear_mesh_system_deflection(self) -> '_2547.ZerolBevelGearMeshSystemDeflection':
        '''ZerolBevelGearMeshSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2547.ZerolBevelGearMeshSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ZerolBevelGearMeshSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2467.GearMeshSystemDeflection]':
        '''List[GearMeshSystemDeflection]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2467.GearMeshSystemDeflection))
        return value


class ListWithSelectedItem_GearSet(_2245.GearSet, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_GearSet

    A specific implementation of 'ListWithSelectedItem' for 'GearSet' types.
    '''

    __hash__ = None
    __qualname__ = 'GearSet'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_GearSet.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2245.GearSet.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2245.GearSet.TYPE

    @property
    def selected_value(self) -> '_2245.GearSet':
        '''GearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2245.GearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_agma_gleason_conical_gear_set(self) -> '_2227.AGMAGleasonConicalGearSet':
        '''AGMAGleasonConicalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2227.AGMAGleasonConicalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AGMAGleasonConicalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_differential_gear_set(self) -> '_2229.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2229.BevelDifferentialGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_gear_set(self) -> '_2233.BevelGearSet':
        '''BevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2233.BevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_concept_gear_set(self) -> '_2235.ConceptGearSet':
        '''ConceptGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2235.ConceptGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_conical_gear_set(self) -> '_2237.ConicalGearSet':
        '''ConicalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2237.ConicalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConicalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_gear_set(self) -> '_2239.CylindricalGearSet':
        '''CylindricalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2239.CylindricalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_face_gear_set(self) -> '_2242.FaceGearSet':
        '''FaceGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2242.FaceGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FaceGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_hypoid_gear_set(self) -> '_2248.HypoidGearSet':
        '''HypoidGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2248.HypoidGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HypoidGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> '_2250.KlingelnbergCycloPalloidConicalGearSet':
        '''KlingelnbergCycloPalloidConicalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2250.KlingelnbergCycloPalloidConicalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidConicalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_2252.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2252.KlingelnbergCycloPalloidHypoidGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_2254.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2254.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_planetary_gear_set(self) -> '_2255.PlanetaryGearSet':
        '''PlanetaryGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2255.PlanetaryGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetaryGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_spiral_bevel_gear_set(self) -> '_2257.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2257.SpiralBevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpiralBevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_diff_gear_set(self) -> '_2259.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2259.StraightBevelDiffGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelDiffGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_gear_set(self) -> '_2261.StraightBevelGearSet':
        '''StraightBevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2261.StraightBevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_worm_gear_set(self) -> '_2265.WormGearSet':
        '''WormGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2265.WormGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WormGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_zerol_bevel_gear_set(self) -> '_2267.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2267.ZerolBevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ZerolBevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2245.GearSet]':
        '''List[GearSet]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2245.GearSet))
        return value


class ListWithSelectedItem_FESubstructureNode(_2099.FESubstructureNode, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_FESubstructureNode

    A specific implementation of 'ListWithSelectedItem' for 'FESubstructureNode' types.
    '''

    __hash__ = None
    __qualname__ = 'FESubstructureNode'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_FESubstructureNode.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2099.FESubstructureNode.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2099.FESubstructureNode.TYPE

    @property
    def selected_value(self) -> '_2099.FESubstructureNode':
        '''FESubstructureNode: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2099.FESubstructureNode)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2099.FESubstructureNode]':
        '''List[FESubstructureNode]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2099.FESubstructureNode))
        return value


class ListWithSelectedItem_Datum(_2163.Datum, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_Datum

    A specific implementation of 'ListWithSelectedItem' for 'Datum' types.
    '''

    __hash__ = None
    __qualname__ = 'Datum'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_Datum.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2163.Datum.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2163.Datum.TYPE

    @property
    def selected_value(self) -> '_2163.Datum':
        '''Datum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2163.Datum)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2163.Datum]':
        '''List[Datum]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2163.Datum))
        return value


class ListWithSelectedItem_Component(_2159.Component, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_Component

    A specific implementation of 'ListWithSelectedItem' for 'Component' types.
    '''

    __hash__ = None
    __qualname__ = 'Component'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_Component.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2159.Component.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2159.Component.TYPE

    @property
    def selected_value(self) -> '_2159.Component':
        '''Component: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2159.Component.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Component. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_abstract_shaft(self) -> '_2151.AbstractShaft':
        '''AbstractShaft: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2151.AbstractShaft.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AbstractShaft. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_abstract_shaft_or_housing(self) -> '_2152.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2152.AbstractShaftOrHousing.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AbstractShaftOrHousing. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bearing(self) -> '_2155.Bearing':
        '''Bearing: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2155.Bearing.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Bearing. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bolt(self) -> '_2157.Bolt':
        '''Bolt: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2157.Bolt.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Bolt. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_connector(self) -> '_2162.Connector':
        '''Connector: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2162.Connector.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Connector. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_datum(self) -> '_2163.Datum':
        '''Datum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2163.Datum.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Datum. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_external_cad_model(self) -> '_2166.ExternalCADModel':
        '''ExternalCADModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2166.ExternalCADModel.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ExternalCADModel. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_fe_part(self) -> '_2167.FEPart':
        '''FEPart: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2167.FEPart.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FEPart. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_guide_dxf_model(self) -> '_2169.GuideDxfModel':
        '''GuideDxfModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2169.GuideDxfModel.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GuideDxfModel. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_mass_disc(self) -> '_2176.MassDisc':
        '''MassDisc: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2176.MassDisc.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MassDisc. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_measurement_component(self) -> '_2177.MeasurementComponent':
        '''MeasurementComponent: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2177.MeasurementComponent.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MeasurementComponent. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_mountable_component(self) -> '_2178.MountableComponent':
        '''MountableComponent: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2178.MountableComponent.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MountableComponent. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_oil_seal(self) -> '_2180.OilSeal':
        '''OilSeal: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2180.OilSeal.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to OilSeal. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_planet_carrier(self) -> '_2183.PlanetCarrier':
        '''PlanetCarrier: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2183.PlanetCarrier.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetCarrier. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_point_load(self) -> '_2185.PointLoad':
        '''PointLoad: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2185.PointLoad.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PointLoad. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_power_load(self) -> '_2186.PowerLoad':
        '''PowerLoad: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2186.PowerLoad.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerLoad. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_unbalanced_mass(self) -> '_2191.UnbalancedMass':
        '''UnbalancedMass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2191.UnbalancedMass.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to UnbalancedMass. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_virtual_component(self) -> '_2193.VirtualComponent':
        '''VirtualComponent: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2193.VirtualComponent.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to VirtualComponent. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_shaft(self) -> '_2196.Shaft':
        '''Shaft: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2196.Shaft.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Shaft. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_agma_gleason_conical_gear(self) -> '_2226.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2226.AGMAGleasonConicalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AGMAGleasonConicalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_differential_gear(self) -> '_2228.BevelDifferentialGear':
        '''BevelDifferentialGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2228.BevelDifferentialGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_differential_planet_gear(self) -> '_2230.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2230.BevelDifferentialPlanetGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialPlanetGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_differential_sun_gear(self) -> '_2231.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2231.BevelDifferentialSunGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialSunGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_gear(self) -> '_2232.BevelGear':
        '''BevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2232.BevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_concept_gear(self) -> '_2234.ConceptGear':
        '''ConceptGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2234.ConceptGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_conical_gear(self) -> '_2236.ConicalGear':
        '''ConicalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2236.ConicalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConicalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_gear(self) -> '_2238.CylindricalGear':
        '''CylindricalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2238.CylindricalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_planet_gear(self) -> '_2240.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2240.CylindricalPlanetGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalPlanetGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_face_gear(self) -> '_2241.FaceGear':
        '''FaceGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2241.FaceGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FaceGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_gear(self) -> '_2243.Gear':
        '''Gear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2243.Gear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Gear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_hypoid_gear(self) -> '_2247.HypoidGear':
        '''HypoidGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2247.HypoidGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HypoidGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2249.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2249.KlingelnbergCycloPalloidConicalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2251.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2251.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2253.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2253.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_spiral_bevel_gear(self) -> '_2256.SpiralBevelGear':
        '''SpiralBevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2256.SpiralBevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpiralBevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_diff_gear(self) -> '_2258.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2258.StraightBevelDiffGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelDiffGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_gear(self) -> '_2260.StraightBevelGear':
        '''StraightBevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2260.StraightBevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_planet_gear(self) -> '_2262.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2262.StraightBevelPlanetGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelPlanetGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_sun_gear(self) -> '_2263.StraightBevelSunGear':
        '''StraightBevelSunGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2263.StraightBevelSunGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelSunGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_worm_gear(self) -> '_2264.WormGear':
        '''WormGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2264.WormGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WormGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_zerol_bevel_gear(self) -> '_2266.ZerolBevelGear':
        '''ZerolBevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2266.ZerolBevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ZerolBevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cycloidal_disc(self) -> '_2282.CycloidalDisc':
        '''CycloidalDisc: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2282.CycloidalDisc.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CycloidalDisc. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_ring_pins(self) -> '_2283.RingPins':
        '''RingPins: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2283.RingPins.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to RingPins. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_clutch_half(self) -> '_2292.ClutchHalf':
        '''ClutchHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2292.ClutchHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ClutchHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_concept_coupling_half(self) -> '_2295.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2295.ConceptCouplingHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptCouplingHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_coupling_half(self) -> '_2297.CouplingHalf':
        '''CouplingHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2297.CouplingHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CouplingHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cvt_pulley(self) -> '_2300.CVTPulley':
        '''CVTPulley: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2300.CVTPulley.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CVTPulley. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_part_to_part_shear_coupling_half(self) -> '_2302.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2302.PartToPartShearCouplingHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PartToPartShearCouplingHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_pulley(self) -> '_2303.Pulley':
        '''Pulley: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2303.Pulley.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Pulley. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_rolling_ring(self) -> '_2309.RollingRing':
        '''RollingRing: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2309.RollingRing.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to RollingRing. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_shaft_hub_connection(self) -> '_2311.ShaftHubConnection':
        '''ShaftHubConnection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2311.ShaftHubConnection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ShaftHubConnection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_spring_damper_half(self) -> '_2314.SpringDamperHalf':
        '''SpringDamperHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2314.SpringDamperHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpringDamperHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_synchroniser_half(self) -> '_2317.SynchroniserHalf':
        '''SynchroniserHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2317.SynchroniserHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SynchroniserHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_synchroniser_part(self) -> '_2318.SynchroniserPart':
        '''SynchroniserPart: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2318.SynchroniserPart.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SynchroniserPart. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_synchroniser_sleeve(self) -> '_2319.SynchroniserSleeve':
        '''SynchroniserSleeve: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2319.SynchroniserSleeve.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SynchroniserSleeve. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_torque_converter_pump(self) -> '_2321.TorqueConverterPump':
        '''TorqueConverterPump: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2321.TorqueConverterPump.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorqueConverterPump. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_torque_converter_turbine(self) -> '_2323.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2323.TorqueConverterTurbine.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorqueConverterTurbine. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2159.Component]':
        '''List[Component]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2159.Component))
        return value


class ListWithSelectedItem_FELink(_2132.FELink, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_FELink

    A specific implementation of 'ListWithSelectedItem' for 'FELink' types.
    '''

    __hash__ = None
    __qualname__ = 'FELink'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_FELink.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2132.FELink.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2132.FELink.TYPE

    @property
    def selected_value(self) -> '_2132.FELink':
        '''FELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2132.FELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_electric_machine_stator_fe_link(self) -> '_2133.ElectricMachineStatorFELink':
        '''ElectricMachineStatorFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2133.ElectricMachineStatorFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineStatorFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_gear_mesh_fe_link(self) -> '_2135.GearMeshFELink':
        '''GearMeshFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2135.GearMeshFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearMeshFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_gear_with_duplicated_meshes_fe_link(self) -> '_2136.GearWithDuplicatedMeshesFELink':
        '''GearWithDuplicatedMeshesFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2136.GearWithDuplicatedMeshesFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearWithDuplicatedMeshesFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_multi_angle_connection_fe_link(self) -> '_2137.MultiAngleConnectionFELink':
        '''MultiAngleConnectionFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2137.MultiAngleConnectionFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MultiAngleConnectionFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_multi_node_connector_fe_link(self) -> '_2138.MultiNodeConnectorFELink':
        '''MultiNodeConnectorFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2138.MultiNodeConnectorFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MultiNodeConnectorFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_multi_node_fe_link(self) -> '_2139.MultiNodeFELink':
        '''MultiNodeFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2139.MultiNodeFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MultiNodeFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_planetary_connector_multi_node_fe_link(self) -> '_2140.PlanetaryConnectorMultiNodeFELink':
        '''PlanetaryConnectorMultiNodeFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2140.PlanetaryConnectorMultiNodeFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetaryConnectorMultiNodeFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_planet_based_fe_link(self) -> '_2141.PlanetBasedFELink':
        '''PlanetBasedFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2141.PlanetBasedFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetBasedFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_planet_carrier_fe_link(self) -> '_2142.PlanetCarrierFELink':
        '''PlanetCarrierFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2142.PlanetCarrierFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetCarrierFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_point_load_fe_link(self) -> '_2143.PointLoadFELink':
        '''PointLoadFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2143.PointLoadFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PointLoadFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_rolling_ring_connection_fe_link(self) -> '_2144.RollingRingConnectionFELink':
        '''RollingRingConnectionFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2144.RollingRingConnectionFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to RollingRingConnectionFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_shaft_hub_connection_fe_link(self) -> '_2145.ShaftHubConnectionFELink':
        '''ShaftHubConnectionFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2145.ShaftHubConnectionFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ShaftHubConnectionFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_single_node_fe_link(self) -> '_2146.SingleNodeFELink':
        '''SingleNodeFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2146.SingleNodeFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SingleNodeFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2132.FELink]':
        '''List[FELink]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2132.FELink))
        return value


class ListWithSelectedItem_FESubstructure(_2097.FESubstructure, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_FESubstructure

    A specific implementation of 'ListWithSelectedItem' for 'FESubstructure' types.
    '''

    __hash__ = None
    __qualname__ = 'FESubstructure'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_FESubstructure.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2097.FESubstructure.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2097.FESubstructure.TYPE

    @property
    def selected_value(self) -> '_2097.FESubstructure':
        '''FESubstructure: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2097.FESubstructure)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2097.FESubstructure]':
        '''List[FESubstructure]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2097.FESubstructure))
        return value


class ListWithSelectedItem_CylindricalGear(_2238.CylindricalGear, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGear

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGear' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGear'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGear.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2238.CylindricalGear.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2238.CylindricalGear.TYPE

    @property
    def selected_value(self) -> '_2238.CylindricalGear':
        '''CylindricalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2238.CylindricalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2238.CylindricalGear]':
        '''List[CylindricalGear]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2238.CylindricalGear))
        return value


class ListWithSelectedItem_GuideDxfModel(_2169.GuideDxfModel, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_GuideDxfModel

    A specific implementation of 'ListWithSelectedItem' for 'GuideDxfModel' types.
    '''

    __hash__ = None
    __qualname__ = 'GuideDxfModel'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_GuideDxfModel.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2169.GuideDxfModel.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2169.GuideDxfModel.TYPE

    @property
    def selected_value(self) -> '_2169.GuideDxfModel':
        '''GuideDxfModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2169.GuideDxfModel)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2169.GuideDxfModel]':
        '''List[GuideDxfModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2169.GuideDxfModel))
        return value


class ListWithSelectedItem_ConcentricPartGroup(_2201.ConcentricPartGroup, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ConcentricPartGroup

    A specific implementation of 'ListWithSelectedItem' for 'ConcentricPartGroup' types.
    '''

    __hash__ = None
    __qualname__ = 'ConcentricPartGroup'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ConcentricPartGroup.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2201.ConcentricPartGroup.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2201.ConcentricPartGroup.TYPE

    @property
    def selected_value(self) -> '_2201.ConcentricPartGroup':
        '''ConcentricPartGroup: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2201.ConcentricPartGroup)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2201.ConcentricPartGroup]':
        '''List[ConcentricPartGroup]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2201.ConcentricPartGroup))
        return value


class ListWithSelectedItem_CylindricalGearSet(_2239.CylindricalGearSet, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGearSet

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearSet' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearSet'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGearSet.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2239.CylindricalGearSet.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2239.CylindricalGearSet.TYPE

    @property
    def selected_value(self) -> '_2239.CylindricalGearSet':
        '''CylindricalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2239.CylindricalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2239.CylindricalGearSet]':
        '''List[CylindricalGearSet]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2239.CylindricalGearSet))
        return value


class ListWithSelectedItem_GearSetDesign(_890.GearSetDesign, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_GearSetDesign

    A specific implementation of 'ListWithSelectedItem' for 'GearSetDesign' types.
    '''

    __hash__ = None
    __qualname__ = 'GearSetDesign'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_GearSetDesign.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_890.GearSetDesign.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _890.GearSetDesign.TYPE

    @property
    def selected_value(self) -> '_890.GearSetDesign':
        '''GearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _890.GearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_zerol_bevel_gear_set_design(self) -> '_894.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _894.ZerolBevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ZerolBevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_worm_gear_set_design(self) -> '_899.WormGearSetDesign':
        '''WormGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _899.WormGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WormGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_diff_gear_set_design(self) -> '_903.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _903.StraightBevelDiffGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_straight_bevel_gear_set_design(self) -> '_907.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _907.StraightBevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_spiral_bevel_gear_set_design(self) -> '_911.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _911.SpiralBevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpiralBevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_915.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _915.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_919.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _919.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_klingelnberg_conical_gear_set_design(self) -> '_923.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _923.KlingelnbergConicalGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_hypoid_gear_set_design(self) -> '_927.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _927.HypoidGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HypoidGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_face_gear_set_design(self) -> '_935.FaceGearSetDesign':
        '''FaceGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _935.FaceGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FaceGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_gear_set_design(self) -> '_967.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _967.CylindricalGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_planetary_gear_set_design(self) -> '_978.CylindricalPlanetaryGearSetDesign':
        '''CylindricalPlanetaryGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _978.CylindricalPlanetaryGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalPlanetaryGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_conical_gear_set_design(self) -> '_1087.ConicalGearSetDesign':
        '''ConicalGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1087.ConicalGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConicalGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_concept_gear_set_design(self) -> '_1109.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1109.ConceptGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_bevel_gear_set_design(self) -> '_1113.BevelGearSetDesign':
        '''BevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1113.BevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_agma_gleason_conical_gear_set_design(self) -> '_1126.AGMAGleasonConicalGearSetDesign':
        '''AGMAGleasonConicalGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1126.AGMAGleasonConicalGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AGMAGleasonConicalGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_890.GearSetDesign]':
        '''List[GearSetDesign]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_890.GearSetDesign))
        return value


class ListWithSelectedItem_ShaftHubConnection(_2311.ShaftHubConnection, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ShaftHubConnection

    A specific implementation of 'ListWithSelectedItem' for 'ShaftHubConnection' types.
    '''

    __hash__ = None
    __qualname__ = 'ShaftHubConnection'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ShaftHubConnection.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2311.ShaftHubConnection.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2311.ShaftHubConnection.TYPE

    @property
    def selected_value(self) -> '_2311.ShaftHubConnection':
        '''ShaftHubConnection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2311.ShaftHubConnection)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2311.ShaftHubConnection]':
        '''List[ShaftHubConnection]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2311.ShaftHubConnection))
        return value


class ListWithSelectedItem_TSelectableItem(Generic[TSelectableItem], mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_TSelectableItem

    A specific implementation of 'ListWithSelectedItem' for 'TSelectableItem' types.
    '''

    __hash__ = None
    __qualname__ = 'TSelectableItem'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_TSelectableItem.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'TSelectableItem':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return TSelectableItem

    @property
    def selected_value(self) -> 'TSelectableItem':
        '''TSelectableItem: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[TSelectableItem]':
        '''List[TSelectableItem]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues)
        return value


class ListWithSelectedItem_CylindricalGearSystemDeflection(_2453.CylindricalGearSystemDeflection, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGearSystemDeflection

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearSystemDeflection' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearSystemDeflection'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGearSystemDeflection.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2453.CylindricalGearSystemDeflection.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2453.CylindricalGearSystemDeflection.TYPE

    @property
    def selected_value(self) -> '_2453.CylindricalGearSystemDeflection':
        '''CylindricalGearSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2453.CylindricalGearSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_gear_system_deflection_timestep(self) -> '_2454.CylindricalGearSystemDeflectionTimestep':
        '''CylindricalGearSystemDeflectionTimestep: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2454.CylindricalGearSystemDeflectionTimestep.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSystemDeflectionTimestep. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_gear_system_deflection_with_ltca_results(self) -> '_2455.CylindricalGearSystemDeflectionWithLTCAResults':
        '''CylindricalGearSystemDeflectionWithLTCAResults: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2455.CylindricalGearSystemDeflectionWithLTCAResults.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def selected_value_of_type_cylindrical_planet_gear_system_deflection(self) -> '_2458.CylindricalPlanetGearSystemDeflection':
        '''CylindricalPlanetGearSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2458.CylindricalPlanetGearSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalPlanetGearSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2453.CylindricalGearSystemDeflection]':
        '''List[CylindricalGearSystemDeflection]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2453.CylindricalGearSystemDeflection))
        return value


class ListWithSelectedItem_DesignState(_5361.DesignState, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_DesignState

    A specific implementation of 'ListWithSelectedItem' for 'DesignState' types.
    '''

    __hash__ = None
    __qualname__ = 'DesignState'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_DesignState.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_5361.DesignState.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5361.DesignState.TYPE

    @property
    def selected_value(self) -> '_5361.DesignState':
        '''DesignState: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5361.DesignState)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_5361.DesignState]':
        '''List[DesignState]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_5361.DesignState))
        return value


class ListWithSelectedItem_FEPart(_2167.FEPart, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_FEPart

    A specific implementation of 'ListWithSelectedItem' for 'FEPart' types.
    '''

    __hash__ = None
    __qualname__ = 'FEPart'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_FEPart.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2167.FEPart.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2167.FEPart.TYPE

    @property
    def selected_value(self) -> '_2167.FEPart':
        '''FEPart: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2167.FEPart)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2167.FEPart]':
        '''List[FEPart]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2167.FEPart))
        return value


class ListWithSelectedItem_TPartAnalysis(Generic[TPartAnalysis], mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_TPartAnalysis

    A specific implementation of 'ListWithSelectedItem' for 'TPartAnalysis' types.
    '''

    __hash__ = None
    __qualname__ = 'TPartAnalysis'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_TPartAnalysis.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'TPartAnalysis':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return TPartAnalysis

    @property
    def selected_value(self) -> 'TPartAnalysis':
        '''TPartAnalysis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[TPartAnalysis]':
        '''List[TPartAnalysis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues)
        return value


class ListWithSelectedItem_ResultLocationSelectionGroup(_5800.ResultLocationSelectionGroup, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ResultLocationSelectionGroup

    A specific implementation of 'ListWithSelectedItem' for 'ResultLocationSelectionGroup' types.
    '''

    __hash__ = None
    __qualname__ = 'ResultLocationSelectionGroup'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ResultLocationSelectionGroup.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_5800.ResultLocationSelectionGroup.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5800.ResultLocationSelectionGroup.TYPE

    @property
    def selected_value(self) -> '_5800.ResultLocationSelectionGroup':
        '''ResultLocationSelectionGroup: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5800.ResultLocationSelectionGroup)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_5800.ResultLocationSelectionGroup]':
        '''List[ResultLocationSelectionGroup]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_5800.ResultLocationSelectionGroup))
        return value


class ListWithSelectedItem_StaticLoadCase(_6492.StaticLoadCase, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_StaticLoadCase

    A specific implementation of 'ListWithSelectedItem' for 'StaticLoadCase' types.
    '''

    __hash__ = None
    __qualname__ = 'StaticLoadCase'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_StaticLoadCase.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_6492.StaticLoadCase.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6492.StaticLoadCase.TYPE

    @property
    def selected_value(self) -> '_6492.StaticLoadCase':
        '''StaticLoadCase: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6492.StaticLoadCase.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StaticLoadCase. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_6492.StaticLoadCase]':
        '''List[StaticLoadCase]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_6492.StaticLoadCase))
        return value


class ListWithSelectedItem_DutyCycle(_5362.DutyCycle, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_DutyCycle

    A specific implementation of 'ListWithSelectedItem' for 'DutyCycle' types.
    '''

    __hash__ = None
    __qualname__ = 'DutyCycle'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_DutyCycle.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_5362.DutyCycle.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5362.DutyCycle.TYPE

    @property
    def selected_value(self) -> '_5362.DutyCycle':
        '''DutyCycle: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5362.DutyCycle)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_5362.DutyCycle]':
        '''List[DutyCycle]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_5362.DutyCycle))
        return value


class ListWithSelectedItem_float(float, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_float

    A specific implementation of 'ListWithSelectedItem' for 'float' types.
    '''

    __hash__ = None
    __qualname__ = 'float'

    def __new__(cls, instance_to_wrap: 'ListWithSelectedItem_float.TYPE'):
        return float.__new__(cls, instance_to_wrap.SelectedValue if instance_to_wrap.SelectedValue is not None else 0.0)

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_float.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'float':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return float

    @property
    def selected_value(self) -> 'float':
        '''float: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[float]':
        '''List[float]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.enclosing.AvailableValues)
        return value


class ListWithSelectedItem_ElectricMachineDataSet(_2088.ElectricMachineDataSet, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ElectricMachineDataSet

    A specific implementation of 'ListWithSelectedItem' for 'ElectricMachineDataSet' types.
    '''

    __hash__ = None
    __qualname__ = 'ElectricMachineDataSet'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ElectricMachineDataSet.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2088.ElectricMachineDataSet.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2088.ElectricMachineDataSet.TYPE

    @property
    def selected_value(self) -> '_2088.ElectricMachineDataSet':
        '''ElectricMachineDataSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2088.ElectricMachineDataSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2088.ElectricMachineDataSet]':
        '''List[ElectricMachineDataSet]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2088.ElectricMachineDataSet))
        return value


class ListWithSelectedItem_PointLoad(_2185.PointLoad, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_PointLoad

    A specific implementation of 'ListWithSelectedItem' for 'PointLoad' types.
    '''

    __hash__ = None
    __qualname__ = 'PointLoad'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_PointLoad.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2185.PointLoad.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2185.PointLoad.TYPE

    @property
    def selected_value(self) -> '_2185.PointLoad':
        '''PointLoad: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2185.PointLoad)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue is not None else None

    @property
    def available_values(self) -> 'List[_2185.PointLoad]':
        '''List[PointLoad]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2185.PointLoad))
        return value
