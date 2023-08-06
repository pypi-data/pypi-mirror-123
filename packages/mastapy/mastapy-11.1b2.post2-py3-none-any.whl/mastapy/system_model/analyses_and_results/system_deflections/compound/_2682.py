'''_2682.py

UnbalancedMassCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2191
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2542
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2683
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'UnbalancedMassCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassCompoundSystemDeflection',)


class UnbalancedMassCompoundSystemDeflection(_2683.VirtualComponentCompoundSystemDeflection):
    '''UnbalancedMassCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2191.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2191.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_2542.UnbalancedMassSystemDeflection]':
        '''List[UnbalancedMassSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_2542.UnbalancedMassSystemDeflection))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2542.UnbalancedMassSystemDeflection]':
        '''List[UnbalancedMassSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_2542.UnbalancedMassSystemDeflection))
        return value
