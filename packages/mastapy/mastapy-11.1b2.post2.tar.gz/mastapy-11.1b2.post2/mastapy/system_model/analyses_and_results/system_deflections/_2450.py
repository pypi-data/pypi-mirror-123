'''_2450.py

CylindricalGearSetSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2239, _2255
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6552, _6624
from mastapy.system_model.analyses_and_results.power_flows import _3788, _3823
from mastapy.gears.rating.cylindrical import _427
from mastapy.gears.manufacturing.cylindrical import _575
from mastapy.system_model.analyses_and_results.system_deflections import _2453, _2447, _2468
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CylindricalGearSetSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetSystemDeflection',)


class CylindricalGearSetSystemDeflection(_2468.GearSetSystemDeflection):
    '''CylindricalGearSetSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2239.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2239.CylindricalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6552.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6552.CylindricalGearSetLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to CylindricalGearSetLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def power_flow_results(self) -> '_3788.CylindricalGearSetPowerFlow':
        '''CylindricalGearSetPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3788.CylindricalGearSetPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to CylindricalGearSetPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults is not None else None

    @property
    def rating(self) -> '_427.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_427.CylindricalGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating is not None else None

    @property
    def component_detailed_analysis(self) -> '_427.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_427.CylindricalGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis is not None else None

    @property
    def manufacturing_analysis(self) -> '_575.CylindricalManufacturedGearSetLoadCase':
        '''CylindricalManufacturedGearSetLoadCase: 'ManufacturingAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_575.CylindricalManufacturedGearSetLoadCase)(self.wrapped.ManufacturingAnalysis) if self.wrapped.ManufacturingAnalysis is not None else None

    @property
    def cylindrical_gears_system_deflection(self) -> 'List[_2453.CylindricalGearSystemDeflection]':
        '''List[CylindricalGearSystemDeflection]: 'CylindricalGearsSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsSystemDeflection, constructor.new(_2453.CylindricalGearSystemDeflection))
        return value

    @property
    def cylindrical_meshes_system_deflection(self) -> 'List[_2447.CylindricalGearMeshSystemDeflection]':
        '''List[CylindricalGearMeshSystemDeflection]: 'CylindricalMeshesSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesSystemDeflection, constructor.new(_2447.CylindricalGearMeshSystemDeflection))
        return value
