'''_6880.py

CylindricalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2239, _2255
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6878, _6879, _6891
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6750
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'CylindricalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation',)


class CylindricalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation(_6891.GearSetCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''CylindricalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2239.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2239.CylindricalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

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
    def cylindrical_gears_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6878.CylindricalGearCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CylindricalGearCompoundAdvancedTimeSteppingAnalysisForModulation]: 'CylindricalGearsCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6878.CylindricalGearCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cylindrical_meshes_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6879.CylindricalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CylindricalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]: 'CylindricalMeshesCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6879.CylindricalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6750.CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6750.CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6750.CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6750.CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value
