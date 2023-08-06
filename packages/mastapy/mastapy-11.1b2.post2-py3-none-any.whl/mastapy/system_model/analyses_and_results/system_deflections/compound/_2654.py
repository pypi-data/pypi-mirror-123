'''_2654.py

RootAssemblyCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.analyses_and_results.system_deflections.compound import _2611, _2566
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _3965
from mastapy.system_model.analyses_and_results.system_deflections import _2508
from mastapy.system_model.fe import _2121
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'RootAssemblyCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyCompoundSystemDeflection',)


class RootAssemblyCompoundSystemDeflection(_2566.AssemblyCompoundSystemDeflection):
    '''RootAssemblyCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle_efficiency_results(self) -> '_2611.DutyCycleEfficiencyResults':
        '''DutyCycleEfficiencyResults: 'DutyCycleEfficiencyResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2611.DutyCycleEfficiencyResults)(self.wrapped.DutyCycleEfficiencyResults) if self.wrapped.DutyCycleEfficiencyResults is not None else None

    @property
    def root_assembly_compound_power_flow(self) -> '_3965.RootAssemblyCompoundPowerFlow':
        '''RootAssemblyCompoundPowerFlow: 'RootAssemblyCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3965.RootAssemblyCompoundPowerFlow)(self.wrapped.RootAssemblyCompoundPowerFlow) if self.wrapped.RootAssemblyCompoundPowerFlow is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2508.RootAssemblySystemDeflection]':
        '''List[RootAssemblySystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_2508.RootAssemblySystemDeflection))
        return value

    @property
    def bearing_race_f_es(self) -> 'List[_2121.RaceBearingFESystemDeflection]':
        '''List[RaceBearingFESystemDeflection]: 'BearingRaceFEs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BearingRaceFEs, constructor.new(_2121.RaceBearingFESystemDeflection))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2508.RootAssemblySystemDeflection]':
        '''List[RootAssemblySystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_2508.RootAssemblySystemDeflection))
        return value
