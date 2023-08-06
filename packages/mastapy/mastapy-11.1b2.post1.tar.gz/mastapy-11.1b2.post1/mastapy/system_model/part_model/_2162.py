'''_2162.py

Connector
'''


from typing import Optional

from mastapy.system_model.connections_and_sockets import (
    _1991, _1981, _1982, _1989,
    _1994, _1995, _1997, _1998,
    _1999, _2000, _2001, _2003,
    _2004, _2005, _2008, _2009,
    _1987, _1980, _1983, _1984,
    _1988, _1996, _2002, _2007,
    _2010
)
from mastapy._internal import constructor
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
from mastapy.system_model.part_model import (
    _2151, _2160, _2159, _2178
)
from mastapy.system_model.part_model.shaft_model import _2196
from mastapy.system_model.part_model.cycloidal import _2282
from mastapy._internal.python_net import python_net_import

_CONNECTOR = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Connector')


__docformat__ = 'restructuredtext en'
__all__ = ('Connector',)


class Connector(_2178.MountableComponent):
    '''Connector

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Connector.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def outer_socket(self) -> '_1991.CylindricalSocket':
        '''CylindricalSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1991.CylindricalSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CylindricalSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_bearing_inner_socket(self) -> '_1981.BearingInnerSocket':
        '''BearingInnerSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1981.BearingInnerSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to BearingInnerSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_bearing_outer_socket(self) -> '_1982.BearingOuterSocket':
        '''BearingOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.BearingOuterSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to BearingOuterSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_cvt_pulley_socket(self) -> '_1989.CVTPulleySocket':
        '''CVTPulleySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.CVTPulleySocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CVTPulleySocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_inner_shaft_socket(self) -> '_1994.InnerShaftSocket':
        '''InnerShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.InnerShaftSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to InnerShaftSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_inner_shaft_socket_base(self) -> '_1995.InnerShaftSocketBase':
        '''InnerShaftSocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1995.InnerShaftSocketBase.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to InnerShaftSocketBase. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_mountable_component_inner_socket(self) -> '_1997.MountableComponentInnerSocket':
        '''MountableComponentInnerSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1997.MountableComponentInnerSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to MountableComponentInnerSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_mountable_component_outer_socket(self) -> '_1998.MountableComponentOuterSocket':
        '''MountableComponentOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1998.MountableComponentOuterSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to MountableComponentOuterSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_mountable_component_socket(self) -> '_1999.MountableComponentSocket':
        '''MountableComponentSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1999.MountableComponentSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to MountableComponentSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_outer_shaft_socket(self) -> '_2000.OuterShaftSocket':
        '''OuterShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2000.OuterShaftSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to OuterShaftSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_outer_shaft_socket_base(self) -> '_2001.OuterShaftSocketBase':
        '''OuterShaftSocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.OuterShaftSocketBase.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to OuterShaftSocketBase. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_planetary_socket(self) -> '_2003.PlanetarySocket':
        '''PlanetarySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2003.PlanetarySocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PlanetarySocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_planetary_socket_base(self) -> '_2004.PlanetarySocketBase':
        '''PlanetarySocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2004.PlanetarySocketBase.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PlanetarySocketBase. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_pulley_socket(self) -> '_2005.PulleySocket':
        '''PulleySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.PulleySocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PulleySocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_rolling_ring_socket(self) -> '_2008.RollingRingSocket':
        '''RollingRingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2008.RollingRingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to RollingRingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_shaft_socket(self) -> '_2009.ShaftSocket':
        '''ShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2009.ShaftSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ShaftSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_cylindrical_gear_teeth_socket(self) -> '_2025.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.CylindricalGearTeethSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_axial_left_socket(self) -> '_2048.CycloidalDiscAxialLeftSocket':
        '''CycloidalDiscAxialLeftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2048.CycloidalDiscAxialLeftSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_axial_right_socket(self) -> '_2049.CycloidalDiscAxialRightSocket':
        '''CycloidalDiscAxialRightSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2049.CycloidalDiscAxialRightSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscAxialRightSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_inner_socket(self) -> '_2051.CycloidalDiscInnerSocket':
        '''CycloidalDiscInnerSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2051.CycloidalDiscInnerSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscInnerSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_outer_socket(self) -> '_2052.CycloidalDiscOuterSocket':
        '''CycloidalDiscOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2052.CycloidalDiscOuterSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscOuterSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2054.CycloidalDiscPlanetaryBearingSocket':
        '''CycloidalDiscPlanetaryBearingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2054.CycloidalDiscPlanetaryBearingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_ring_pins_socket(self) -> '_2055.RingPinsSocket':
        '''RingPinsSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2055.RingPinsSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to RingPinsSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_clutch_socket(self) -> '_2058.ClutchSocket':
        '''ClutchSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2058.ClutchSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ClutchSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_concept_coupling_socket(self) -> '_2060.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2060.ConceptCouplingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_coupling_socket(self) -> '_2062.CouplingSocket':
        '''CouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2062.CouplingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CouplingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_part_to_part_shear_coupling_socket(self) -> '_2064.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2064.PartToPartShearCouplingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_spring_damper_socket(self) -> '_2066.SpringDamperSocket':
        '''SpringDamperSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2066.SpringDamperSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to SpringDamperSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_torque_converter_pump_socket(self) -> '_2068.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2068.TorqueConverterPumpSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_socket_of_type_torque_converter_turbine_socket(self) -> '_2069.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2069.TorqueConverterTurbineSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket is not None else None

    @property
    def outer_connection(self) -> '_1987.Connection':
        '''Connection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1987.Connection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to Connection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_1980.AbstractShaftToMountableComponentConnection':
        '''AbstractShaftToMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1980.AbstractShaftToMountableComponentConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_belt_connection(self) -> '_1983.BeltConnection':
        '''BeltConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1983.BeltConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BeltConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_coaxial_connection(self) -> '_1984.CoaxialConnection':
        '''CoaxialConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1984.CoaxialConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CoaxialConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_cvt_belt_connection(self) -> '_1988.CVTBeltConnection':
        '''CVTBeltConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1988.CVTBeltConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CVTBeltConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_inter_mountable_component_connection(self) -> '_1996.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.InterMountableComponentConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to InterMountableComponentConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_planetary_connection(self) -> '_2002.PlanetaryConnection':
        '''PlanetaryConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.PlanetaryConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to PlanetaryConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_rolling_ring_connection(self) -> '_2007.RollingRingConnection':
        '''RollingRingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2007.RollingRingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to RollingRingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_shaft_to_mountable_component_connection(self) -> '_2010.ShaftToMountableComponentConnection':
        '''ShaftToMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2010.ShaftToMountableComponentConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_agma_gleason_conical_gear_mesh(self) -> '_2014.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2014.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_bevel_differential_gear_mesh(self) -> '_2016.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.BevelDifferentialGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_bevel_gear_mesh(self) -> '_2018.BevelGearMesh':
        '''BevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2018.BevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_concept_gear_mesh(self) -> '_2020.ConceptGearMesh':
        '''ConceptGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2020.ConceptGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConceptGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_conical_gear_mesh(self) -> '_2022.ConicalGearMesh':
        '''ConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.ConicalGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConicalGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_cylindrical_gear_mesh(self) -> '_2024.CylindricalGearMesh':
        '''CylindricalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2024.CylindricalGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_face_gear_mesh(self) -> '_2026.FaceGearMesh':
        '''FaceGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2026.FaceGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to FaceGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_gear_mesh(self) -> '_2028.GearMesh':
        '''GearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2028.GearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to GearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_hypoid_gear_mesh(self) -> '_2030.HypoidGearMesh':
        '''HypoidGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2030.HypoidGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to HypoidGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_2033.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_2034.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2034.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_2035.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2035.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_spiral_bevel_gear_mesh(self) -> '_2038.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2038.SpiralBevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_straight_bevel_diff_gear_mesh(self) -> '_2040.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2040.StraightBevelDiffGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_straight_bevel_gear_mesh(self) -> '_2042.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2042.StraightBevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_worm_gear_mesh(self) -> '_2044.WormGearMesh':
        '''WormGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2044.WormGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to WormGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_zerol_bevel_gear_mesh(self) -> '_2046.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2046.ZerolBevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2050.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2050.CycloidalDiscCentralBearingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2053.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2053.CycloidalDiscPlanetaryBearingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_ring_pins_to_disc_connection(self) -> '_2056.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2056.RingPinsToDiscConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to RingPinsToDiscConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_clutch_connection(self) -> '_2057.ClutchConnection':
        '''ClutchConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2057.ClutchConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ClutchConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_concept_coupling_connection(self) -> '_2059.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2059.ConceptCouplingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_coupling_connection(self) -> '_2061.CouplingConnection':
        '''CouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2061.CouplingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CouplingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_part_to_part_shear_coupling_connection(self) -> '_2063.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2063.PartToPartShearCouplingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_spring_damper_connection(self) -> '_2065.SpringDamperConnection':
        '''SpringDamperConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2065.SpringDamperConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to SpringDamperConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_connection_of_type_torque_converter_connection(self) -> '_2067.TorqueConverterConnection':
        '''TorqueConverterConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2067.TorqueConverterConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection is not None else None

    @property
    def outer_component(self) -> '_2151.AbstractShaft':
        '''AbstractShaft: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2151.AbstractShaft.TYPE not in self.wrapped.OuterComponent.__class__.__mro__:
            raise CastException('Failed to cast outer_component to AbstractShaft. Expected: {}.'.format(self.wrapped.OuterComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterComponent.__class__)(self.wrapped.OuterComponent) if self.wrapped.OuterComponent is not None else None

    @property
    def outer_component_of_type_shaft(self) -> '_2196.Shaft':
        '''Shaft: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2196.Shaft.TYPE not in self.wrapped.OuterComponent.__class__.__mro__:
            raise CastException('Failed to cast outer_component to Shaft. Expected: {}.'.format(self.wrapped.OuterComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterComponent.__class__)(self.wrapped.OuterComponent) if self.wrapped.OuterComponent is not None else None

    @property
    def outer_component_of_type_cycloidal_disc(self) -> '_2282.CycloidalDisc':
        '''CycloidalDisc: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2282.CycloidalDisc.TYPE not in self.wrapped.OuterComponent.__class__.__mro__:
            raise CastException('Failed to cast outer_component to CycloidalDisc. Expected: {}.'.format(self.wrapped.OuterComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterComponent.__class__)(self.wrapped.OuterComponent) if self.wrapped.OuterComponent is not None else None

    def house_in(self, shaft: '_2151.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_1987.Connection':
        ''' 'HouseIn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.connections_and_sockets.Connection
        '''

        offset = float(offset)
        method_result = self.wrapped.HouseIn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def try_house_in(self, shaft: '_2151.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_2160.ComponentsConnectedResult':
        ''' 'TryHouseIn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        '''

        offset = float(offset)
        method_result = self.wrapped.TryHouseIn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def other_component(self, component: '_2159.Component') -> '_2151.AbstractShaft':
        ''' 'OtherComponent' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.part_model.AbstractShaft
        '''

        method_result = self.wrapped.OtherComponent(component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None
