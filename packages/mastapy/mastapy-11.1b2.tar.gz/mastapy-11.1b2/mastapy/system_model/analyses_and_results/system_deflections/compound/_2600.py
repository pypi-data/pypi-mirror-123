'''_2600.py

CVTCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.analyses_and_results.system_deflections import _2442
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2569
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CVTCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundSystemDeflection',)


class CVTCompoundSystemDeflection(_2569.BeltDriveCompoundSystemDeflection):
    '''CVTCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CVT_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2442.CVTSystemDeflection]':
        '''List[CVTSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_2442.CVTSystemDeflection))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2442.CVTSystemDeflection]':
        '''List[CVTSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_2442.CVTSystemDeflection))
        return value
