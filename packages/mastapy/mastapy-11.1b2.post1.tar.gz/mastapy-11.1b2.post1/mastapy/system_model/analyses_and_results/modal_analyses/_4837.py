'''_4837.py

CycloidalAssemblyModalAnalysis
'''


from mastapy.system_model.part_model.cycloidal import _2281
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6544
from mastapy.system_model.analyses_and_results.system_deflections import _2443
from mastapy.system_model.analyses_and_results.modal_analyses import _4898
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'CycloidalAssemblyModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssemblyModalAnalysis',)


class CycloidalAssemblyModalAnalysis(_4898.SpecialisedAssemblyModalAnalysis):
    '''CycloidalAssemblyModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_ASSEMBLY_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalAssemblyModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2281.CycloidalAssembly':
        '''CycloidalAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2281.CycloidalAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6544.CycloidalAssemblyLoadCase':
        '''CycloidalAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6544.CycloidalAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def system_deflection_results(self) -> '_2443.CycloidalAssemblySystemDeflection':
        '''CycloidalAssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2443.CycloidalAssemblySystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None
