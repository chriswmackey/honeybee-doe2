# coding=utf-8
"""Model DOE-2 Properties."""
from honeybee.units import parse_distance_string


class ModelDoe2Properties(object):
    """DOE-2 Properties for Honeybee Model.

    Args:
        host: A honeybee_core Model object that hosts these properties.

    Properties:
        * host
    """

    def __init__(self, host):
        """Initialize ModelDoe2Properties."""
        self._host = host

    @property
    def host(self):
        """Get the Model object hosting these properties."""
        return self._host

    def check_for_extension(self, raise_exception=True, detailed=False):
        """Check that the Model is valid for DOE-2 simulation.

        This process includes all relevant honeybee-core checks as well as checks
        that apply only for DOE-2.

        Args:
            raise_exception: Boolean to note whether a ValueError should be raised
                if any errors are found. If False, this method will simply
                return a text string with all errors that were found. (Default: True).
            detailed: Boolean for whether the returned object is a detailed list of
                dicts with error info or a string with a message. (Default: False).

        Returns:
            A text string with all errors that were found or a list if detailed is True.
            This string (or list) will be empty if no errors were found.
        """
        # set up defaults to ensure the method runs correctly
        detailed = False if raise_exception else detailed
        msgs = []
        tol = self.host.tolerance
        ang_tol = self.host.angle_tolerance
        e_tol = parse_distance_string('0.03ft', self.host.units)

        # perform checks for duplicate identifiers, which might mess with other checks
        msgs.append(self.host.check_all_duplicate_identifiers(False, detailed))

        # perform several checks for the Honeybee schema geometry rules
        msgs.append(self.host.check_planar(tol, False, detailed))
        msgs.append(self.host.check_self_intersecting(tol, False, detailed))
        msgs.append(self.host.check_degenerate_rooms(e_tol, False, detailed))

        # perform geometry checks related to parent-child relationships
        msgs.append(self.host.check_sub_faces_valid(tol, ang_tol, False, detailed))
        msgs.append(self.host.check_sub_faces_overlapping(tol, False, detailed))
        msgs.append(self.host.check_rooms_solid(tol, ang_tol, False, detailed))
        msgs.append(self.host.check_upside_down_faces(ang_tol, False, detailed))

        # perform checks related to adjacency relationships
        msgs.append(self.host.check_room_volume_collisions(tol, False, detailed))
        msgs.append(self.host.check_missing_adjacencies(False, detailed))
        msgs.append(self.host.check_matching_adjacent_areas(tol, False, detailed))
        msgs.append(self.host.check_all_air_boundaries_adjacent(False, detailed))

        # perform checks that are specific to DOE-2
        e_prop = self.host.properties.energy
        msgs.append(e_prop.check_interior_constructions_reversed(False, detailed))
        msgs.append(self.check_no_room_holes(False, detailed))
        # TODO: Add checks for the number of room face vertices and courtyards

        # output a final report of errors or raise an exception
        full_msgs = [msg for msg in msgs if msg]
        if detailed:
            return [m for msg in full_msgs for m in msg]
        full_msg = '\n'.join(full_msgs)
        if raise_exception and len(full_msgs) != 0:
            raise ValueError(full_msg)
        return full_msg

    def check_generic(self, raise_exception=True, detailed=False):
        """Check generic of the aspects of the Model DOE-2 properties.

        This includes checks for everything except holes in floor plates and
        courtyard stories.

        Args:
            raise_exception: Boolean to note whether a ValueError should be raised
                if any errors are found. If False, this method will simply
                return a text string with all errors that were found.
            detailed: Boolean for whether the returned object is a detailed list of
                dicts with error info or a string with a message. (Default: False).

        Returns:
            A text string with all errors that were found or a list if detailed is True.
            This string (or list) will be empty if no errors were found.
        """
        # set up defaults to ensure the method runs correctly
        detailed = False if raise_exception else detailed
        msgs = []
        # perform checks for specific doe-2 simulation rules
        # TODO: Add checks for the number of room face vertices
        # output a final report of errors or raise an exception
        full_msgs = [msg for msg in msgs if msg]
        if detailed:
            return [m for msg in full_msgs for m in msg]
        full_msg = '\n'.join(full_msgs)
        if raise_exception and len(full_msgs) != 0:
            raise ValueError(full_msg)
        return full_msg

    def check_all(self, raise_exception=True, detailed=False):
        """Check all of the aspects of the Model DOE-2 properties.

        Args:
            raise_exception: Boolean to note whether a ValueError should be raised
                if any errors are found. If False, this method will simply
                return a text string with all errors that were found.
            detailed: Boolean for whether the returned object is a detailed list of
                dicts with error info or a string with a message. (Default: False).

        Returns:
            A text string with all errors that were found or a list if detailed is True.
            This string (or list) will be empty if no errors were found.
        """
        # set up defaults to ensure the method runs correctly
        detailed = False if raise_exception else detailed
        msgs = []
        # perform checks for specific doe-2 simulation rules
        # TODO: Add checks for the number of room face vertices and courtyards
        # output a final report of errors or raise an exception
        full_msgs = [msg for msg in msgs if msg]
        if detailed:
            return [m for msg in full_msgs for m in msg]
        full_msg = '\n'.join(full_msgs)
        if raise_exception and len(full_msgs) != 0:
            raise ValueError(full_msg)
        return full_msg

    def check_no_room_holes(self, raise_exception=True, detailed=False):
        """Check whether any Room has geometry with holes.

        EQuest currently has no way to represent such geometry so, if the issue
        is not addressed, the hole will simply be removed as part of the
        process of exporting to an INP file.

        Args:
            raise_exception: If True, a ValueError will be raised if the Room2D
                floor plate has one or more holes. (Default: True).
            detailed: Boolean for whether the returned object is a detailed list of
                dicts with error info or a string with a message. (Default: False).

        Returns:
            A string with the message or a list with a dictionary if detailed is True.
        """
        detailed = False if raise_exception else detailed
        msgs = []
        for room in self.host.rooms:
            msg = room.properties.doe2.check_no_holes(False, detailed)
            if detailed:
                msgs.extend(msg)
            elif msg != '':
                msgs.append(msg)
        if detailed:
            return msgs
        full_msg = '\n'.join(msgs)
        if raise_exception and len(msgs) != 0:
            raise ValueError(full_msg)
        return full_msg

    def to_dict(self):
        """Return Model DOE-2 properties as a dictionary."""
        return {'doe2': {'type': 'ModelDoe2Properties'}}

    def apply_properties_from_dict(self, data):
        """Apply the energy properties of a dictionary to the host Model of this object.

        Args:
            data: A dictionary representation of an entire honeybee-core Model.
                Note that this dictionary must have ModelEnergyProperties in order
                for this method to successfully apply the energy properties.
        """
        assert 'doe2' in data['properties'], \
            'Dictionary possesses no ModelDoe2Properties.'
        room_doe2_dicts = []
        if 'rooms' in data and data['rooms'] is not None:
            for room_dict in data['rooms']:
                try:
                    room_doe2_dicts.append(room_dict['properties']['doe2'])
                except KeyError:
                    room_doe2_dicts.append(None)
            for room, r_dict in zip(self.host.rooms, room_doe2_dicts):
                if r_dict is not None:
                    room.properties.doe2.apply_properties_from_dict(r_dict)

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return 'Model DOE2 Properties: [host: {}]'.format(self.host.display_name)
