'''_5211.py

TorqueConverterTurbineMultibodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2323
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6667
from mastapy.system_model.analyses_and_results.mbd_analyses import _5116
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'TorqueConverterTurbineMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineMultibodyDynamicsAnalysis',)


class TorqueConverterTurbineMultibodyDynamicsAnalysis(_5116.CouplingHalfMultibodyDynamicsAnalysis):
    '''TorqueConverterTurbineMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2323.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2323.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6667.TorqueConverterTurbineLoadCase':
        '''TorqueConverterTurbineLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6667.TorqueConverterTurbineLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None
