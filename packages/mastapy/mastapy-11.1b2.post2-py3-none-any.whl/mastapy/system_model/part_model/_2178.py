'''_2178.py

MountableComponent
'''


from typing import Optional

from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import (
    _1991, _1981, _1982, _1989,
    _1994, _1995, _1997, _1998,
    _1999, _2000, _2001, _2003,
    _2004, _2005, _2008, _2009,
    _1987, _1980, _1983, _1984,
    _1988, _1996, _2002, _2007,
    _2010
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _2025, _2014, _2016, _2018,
    _2020, _2022, _2024, _2026,
    _2028, _2030, _2033, _2034,
    _2035, _2038, _2040, _2042,
    _2044, _2046
)
from mastapy.system_model.connections_and_sockets.cycloidal import (
    _2048, _2049, _2051, _2052,
    _2054, _2055, _2050, _2053,
    _2056
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _2058, _2060, _2062, _2064,
    _2066, _2068, _2069, _2057,
    _2059, _2061, _2063, _2065,
    _2067
)
from mastapy.system_model.part_model import _2151, _2160, _2159
from mastapy.system_model.part_model.shaft_model import _2196
from mastapy.system_model.part_model.cycloidal import _2282
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MountableComponent')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponent',)


class MountableComponent(_2159.Component):
    '''MountableComponent

    This is a mastapy class.
    '''

    TYPE = _MOUNTABLE_COMPONENT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountableComponent.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rotation_about_axis(self) -> 'float':
        '''float: 'RotationAboutAxis' is the original name of this property.'''

        return self.wrapped.RotationAboutAxis

    @rotation_about_axis.setter
    def rotation_about_axis(self, value: 'float'):
        self.wrapped.RotationAboutAxis = float(value) if value else 0.0

    @property
    def inner_socket(self) -> '_1991.CylindricalSocket':
        '''CylindricalSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1991.CylindricalSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CylindricalSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_bearing_inner_socket(self) -> '_1981.BearingInnerSocket':
        '''BearingInnerSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1981.BearingInnerSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to BearingInnerSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_bearing_outer_socket(self) -> '_1982.BearingOuterSocket':
        '''BearingOuterSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.BearingOuterSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to BearingOuterSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_cvt_pulley_socket(self) -> '_1989.CVTPulleySocket':
        '''CVTPulleySocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.CVTPulleySocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CVTPulleySocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_inner_shaft_socket(self) -> '_1994.InnerShaftSocket':
        '''InnerShaftSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.InnerShaftSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to InnerShaftSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_inner_shaft_socket_base(self) -> '_1995.InnerShaftSocketBase':
        '''InnerShaftSocketBase: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1995.InnerShaftSocketBase.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to InnerShaftSocketBase. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_mountable_component_inner_socket(self) -> '_1997.MountableComponentInnerSocket':
        '''MountableComponentInnerSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1997.MountableComponentInnerSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to MountableComponentInnerSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_mountable_component_outer_socket(self) -> '_1998.MountableComponentOuterSocket':
        '''MountableComponentOuterSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1998.MountableComponentOuterSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to MountableComponentOuterSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_mountable_component_socket(self) -> '_1999.MountableComponentSocket':
        '''MountableComponentSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1999.MountableComponentSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to MountableComponentSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_outer_shaft_socket(self) -> '_2000.OuterShaftSocket':
        '''OuterShaftSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2000.OuterShaftSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to OuterShaftSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_outer_shaft_socket_base(self) -> '_2001.OuterShaftSocketBase':
        '''OuterShaftSocketBase: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.OuterShaftSocketBase.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to OuterShaftSocketBase. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_planetary_socket(self) -> '_2003.PlanetarySocket':
        '''PlanetarySocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2003.PlanetarySocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to PlanetarySocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_planetary_socket_base(self) -> '_2004.PlanetarySocketBase':
        '''PlanetarySocketBase: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2004.PlanetarySocketBase.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to PlanetarySocketBase. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_pulley_socket(self) -> '_2005.PulleySocket':
        '''PulleySocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.PulleySocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to PulleySocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_rolling_ring_socket(self) -> '_2008.RollingRingSocket':
        '''RollingRingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2008.RollingRingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to RollingRingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_shaft_socket(self) -> '_2009.ShaftSocket':
        '''ShaftSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2009.ShaftSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to ShaftSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_cylindrical_gear_teeth_socket(self) -> '_2025.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.CylindricalGearTeethSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_cycloidal_disc_axial_left_socket(self) -> '_2048.CycloidalDiscAxialLeftSocket':
        '''CycloidalDiscAxialLeftSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2048.CycloidalDiscAxialLeftSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_cycloidal_disc_axial_right_socket(self) -> '_2049.CycloidalDiscAxialRightSocket':
        '''CycloidalDiscAxialRightSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2049.CycloidalDiscAxialRightSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CycloidalDiscAxialRightSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_cycloidal_disc_inner_socket(self) -> '_2051.CycloidalDiscInnerSocket':
        '''CycloidalDiscInnerSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2051.CycloidalDiscInnerSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CycloidalDiscInnerSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_cycloidal_disc_outer_socket(self) -> '_2052.CycloidalDiscOuterSocket':
        '''CycloidalDiscOuterSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2052.CycloidalDiscOuterSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CycloidalDiscOuterSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2054.CycloidalDiscPlanetaryBearingSocket':
        '''CycloidalDiscPlanetaryBearingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2054.CycloidalDiscPlanetaryBearingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_ring_pins_socket(self) -> '_2055.RingPinsSocket':
        '''RingPinsSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2055.RingPinsSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to RingPinsSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_clutch_socket(self) -> '_2058.ClutchSocket':
        '''ClutchSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2058.ClutchSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to ClutchSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_concept_coupling_socket(self) -> '_2060.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2060.ConceptCouplingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_coupling_socket(self) -> '_2062.CouplingSocket':
        '''CouplingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2062.CouplingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to CouplingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_part_to_part_shear_coupling_socket(self) -> '_2064.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2064.PartToPartShearCouplingSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_spring_damper_socket(self) -> '_2066.SpringDamperSocket':
        '''SpringDamperSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2066.SpringDamperSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to SpringDamperSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_torque_converter_pump_socket(self) -> '_2068.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2068.TorqueConverterPumpSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_socket_of_type_torque_converter_turbine_socket(self) -> '_2069.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'InnerSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2069.TorqueConverterTurbineSocket.TYPE not in self.wrapped.InnerSocket.__class__.__mro__:
            raise CastException('Failed to cast inner_socket to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.InnerSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerSocket.__class__)(self.wrapped.InnerSocket) if self.wrapped.InnerSocket is not None else None

    @property
    def inner_connection(self) -> '_1987.Connection':
        '''Connection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1987.Connection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to Connection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_1980.AbstractShaftToMountableComponentConnection':
        '''AbstractShaftToMountableComponentConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1980.AbstractShaftToMountableComponentConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_belt_connection(self) -> '_1983.BeltConnection':
        '''BeltConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1983.BeltConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to BeltConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_coaxial_connection(self) -> '_1984.CoaxialConnection':
        '''CoaxialConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1984.CoaxialConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CoaxialConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_cvt_belt_connection(self) -> '_1988.CVTBeltConnection':
        '''CVTBeltConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1988.CVTBeltConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CVTBeltConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_inter_mountable_component_connection(self) -> '_1996.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.InterMountableComponentConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to InterMountableComponentConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_planetary_connection(self) -> '_2002.PlanetaryConnection':
        '''PlanetaryConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.PlanetaryConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to PlanetaryConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_rolling_ring_connection(self) -> '_2007.RollingRingConnection':
        '''RollingRingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2007.RollingRingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to RollingRingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_shaft_to_mountable_component_connection(self) -> '_2010.ShaftToMountableComponentConnection':
        '''ShaftToMountableComponentConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2010.ShaftToMountableComponentConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_agma_gleason_conical_gear_mesh(self) -> '_2014.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2014.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_bevel_differential_gear_mesh(self) -> '_2016.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.BevelDifferentialGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_bevel_gear_mesh(self) -> '_2018.BevelGearMesh':
        '''BevelGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2018.BevelGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to BevelGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_concept_gear_mesh(self) -> '_2020.ConceptGearMesh':
        '''ConceptGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2020.ConceptGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ConceptGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_conical_gear_mesh(self) -> '_2022.ConicalGearMesh':
        '''ConicalGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.ConicalGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ConicalGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_cylindrical_gear_mesh(self) -> '_2024.CylindricalGearMesh':
        '''CylindricalGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2024.CylindricalGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_face_gear_mesh(self) -> '_2026.FaceGearMesh':
        '''FaceGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2026.FaceGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to FaceGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_gear_mesh(self) -> '_2028.GearMesh':
        '''GearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2028.GearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to GearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_hypoid_gear_mesh(self) -> '_2030.HypoidGearMesh':
        '''HypoidGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2030.HypoidGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to HypoidGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_2033.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_2034.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2034.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_2035.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2035.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_spiral_bevel_gear_mesh(self) -> '_2038.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2038.SpiralBevelGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_straight_bevel_diff_gear_mesh(self) -> '_2040.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2040.StraightBevelDiffGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_straight_bevel_gear_mesh(self) -> '_2042.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2042.StraightBevelGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_worm_gear_mesh(self) -> '_2044.WormGearMesh':
        '''WormGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2044.WormGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to WormGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_zerol_bevel_gear_mesh(self) -> '_2046.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2046.ZerolBevelGearMesh.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2050.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2050.CycloidalDiscCentralBearingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2053.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2053.CycloidalDiscPlanetaryBearingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_ring_pins_to_disc_connection(self) -> '_2056.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2056.RingPinsToDiscConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to RingPinsToDiscConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_clutch_connection(self) -> '_2057.ClutchConnection':
        '''ClutchConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2057.ClutchConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ClutchConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_concept_coupling_connection(self) -> '_2059.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2059.ConceptCouplingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_coupling_connection(self) -> '_2061.CouplingConnection':
        '''CouplingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2061.CouplingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to CouplingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_part_to_part_shear_coupling_connection(self) -> '_2063.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2063.PartToPartShearCouplingConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_spring_damper_connection(self) -> '_2065.SpringDamperConnection':
        '''SpringDamperConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2065.SpringDamperConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to SpringDamperConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def inner_connection_of_type_torque_converter_connection(self) -> '_2067.TorqueConverterConnection':
        '''TorqueConverterConnection: 'InnerConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2067.TorqueConverterConnection.TYPE not in self.wrapped.InnerConnection.__class__.__mro__:
            raise CastException('Failed to cast inner_connection to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.InnerConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerConnection.__class__)(self.wrapped.InnerConnection) if self.wrapped.InnerConnection is not None else None

    @property
    def is_mounted(self) -> 'bool':
        '''bool: 'IsMounted' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsMounted

    @property
    def inner_component(self) -> '_2151.AbstractShaft':
        '''AbstractShaft: 'InnerComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2151.AbstractShaft.TYPE not in self.wrapped.InnerComponent.__class__.__mro__:
            raise CastException('Failed to cast inner_component to AbstractShaft. Expected: {}.'.format(self.wrapped.InnerComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerComponent.__class__)(self.wrapped.InnerComponent) if self.wrapped.InnerComponent is not None else None

    @property
    def inner_component_of_type_shaft(self) -> '_2196.Shaft':
        '''Shaft: 'InnerComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2196.Shaft.TYPE not in self.wrapped.InnerComponent.__class__.__mro__:
            raise CastException('Failed to cast inner_component to Shaft. Expected: {}.'.format(self.wrapped.InnerComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerComponent.__class__)(self.wrapped.InnerComponent) if self.wrapped.InnerComponent is not None else None

    @property
    def inner_component_of_type_cycloidal_disc(self) -> '_2282.CycloidalDisc':
        '''CycloidalDisc: 'InnerComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2282.CycloidalDisc.TYPE not in self.wrapped.InnerComponent.__class__.__mro__:
            raise CastException('Failed to cast inner_component to CycloidalDisc. Expected: {}.'.format(self.wrapped.InnerComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InnerComponent.__class__)(self.wrapped.InnerComponent) if self.wrapped.InnerComponent is not None else None

    def try_mount_on(self, shaft: '_2151.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_2160.ComponentsConnectedResult':
        ''' 'TryMountOn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        '''

        offset = float(offset)
        method_result = self.wrapped.TryMountOn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def mount_on(self, shaft: '_2151.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_1984.CoaxialConnection':
        ''' 'MountOn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.connections_and_sockets.CoaxialConnection
        '''

        offset = float(offset)
        method_result = self.wrapped.MountOn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None
