'''_2429.py

ConceptGearSetSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2235
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6530
from mastapy.system_model.analyses_and_results.power_flows import _3769
from mastapy.gears.rating.concept import _507
from mastapy.system_model.analyses_and_results.system_deflections import _2430, _2428, _2468
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ConceptGearSetSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetSystemDeflection',)


class ConceptGearSetSystemDeflection(_2468.GearSetSystemDeflection):
    '''ConceptGearSetSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2235.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2235.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6530.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6530.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def power_flow_results(self) -> '_3769.ConceptGearSetPowerFlow':
        '''ConceptGearSetPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3769.ConceptGearSetPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults is not None else None

    @property
    def rating(self) -> '_507.ConceptGearSetRating':
        '''ConceptGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_507.ConceptGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating is not None else None

    @property
    def component_detailed_analysis(self) -> '_507.ConceptGearSetRating':
        '''ConceptGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_507.ConceptGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis is not None else None

    @property
    def concept_gears_system_deflection(self) -> 'List[_2430.ConceptGearSystemDeflection]':
        '''List[ConceptGearSystemDeflection]: 'ConceptGearsSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsSystemDeflection, constructor.new(_2430.ConceptGearSystemDeflection))
        return value

    @property
    def concept_meshes_system_deflection(self) -> 'List[_2428.ConceptGearMeshSystemDeflection]':
        '''List[ConceptGearMeshSystemDeflection]: 'ConceptMeshesSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesSystemDeflection, constructor.new(_2428.ConceptGearMeshSystemDeflection))
        return value
