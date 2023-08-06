'''_7016.py

DatumAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2163
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6556
from mastapy.system_model.analyses_and_results.system_deflections import _2459
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6988
from mastapy._internal.python_net import python_net_import

_DATUM_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'DatumAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumAdvancedSystemDeflection',)


class DatumAdvancedSystemDeflection(_6988.ComponentAdvancedSystemDeflection):
    '''DatumAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _DATUM_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2163.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2163.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6556.DatumLoadCase':
        '''DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6556.DatumLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def component_system_deflection_results(self) -> 'List[_2459.DatumSystemDeflection]':
        '''List[DatumSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2459.DatumSystemDeflection))
        return value
