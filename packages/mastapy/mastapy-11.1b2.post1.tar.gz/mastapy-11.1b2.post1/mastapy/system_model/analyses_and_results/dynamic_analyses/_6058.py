'''_6058.py

RollingRingAssemblyDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2310
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6636
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6065
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'RollingRingAssemblyDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblyDynamicAnalysis',)


class RollingRingAssemblyDynamicAnalysis(_6065.SpecialisedAssemblyDynamicAnalysis):
    '''RollingRingAssemblyDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ASSEMBLY_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAssemblyDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2310.RollingRingAssembly':
        '''RollingRingAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2310.RollingRingAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6636.RollingRingAssemblyLoadCase':
        '''RollingRingAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6636.RollingRingAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None
