'''_7115.py

BoltCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2157
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6982
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7121
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'BoltCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundAdvancedSystemDeflection',)


class BoltCompoundAdvancedSystemDeflection(_7121.ComponentCompoundAdvancedSystemDeflection):
    '''BoltCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BOLT_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2157.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2157.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6982.BoltAdvancedSystemDeflection]':
        '''List[BoltAdvancedSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6982.BoltAdvancedSystemDeflection))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6982.BoltAdvancedSystemDeflection]':
        '''List[BoltAdvancedSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6982.BoltAdvancedSystemDeflection))
        return value
