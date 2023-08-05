import numpy as np
import math


class RadarTarget(object):
    def __init__(self, distance=0, rcs=0, velocity=0, azimuth=0, elevation=0):
        """
        Creates a static radar target

        :param distance: Simulated object distance, in meters
        :type distance: float
        :param rcs: Simulated object RCS, in dBsm
        :type rcs: float
        :param velocity: Simulated object velocity, in m/sec
        :type velocity: float
        :param azimuth: Simulated object azimuth, in deg
        :type azimuth: float
        :param elevation: Simulated object elevation, in deg
        :type elevation: float
        """
        self.distance = distance
        self.rcs = rcs
        self.velocity = velocity
        self.azimuth = azimuth
        self.elevation = elevation

    def __str__(self):
        return "Distance: {} m\n" \
               "RCS: {} dBsm\n" \
               "Velocity: {} m/sec\n" \
               "Azimuth: {} deg\n" \
               "Elevation: {} deg".format(self.distance, self.rcs, self.velocity, self.azimuth, self.elevation)


class DynamicRadarTarget(object):
    def __init__(self, start_x=0, start_y=0, start_z=0, end_x=0, end_y=0, end_z=0, rcs=0, velocity=0):
        """
        Creates a dynamic radar target

        :param start_x: Simulated x-axis (cross range) object starting position, in m
        :type start_x: float
        :param start_y: Simulated y-axis (down range) object starting position, in m
        :type start_y: float
        :param start_z: Simulated z-axis (elevation) object starting position, in m
        :type start_z: float
        :param end_x: Simulated x-axis (cross range) object ending position, in m
        :type end_x: float
        :param end_y: Simulated y-axis (down range) object ending position, in m
        :type end_y: float
        :param end_z: Simulated z-axis (elevation) object ending position, in m
        :type end_z: float
        :param rcs: Simulated object RCS, in dBsm
        :type rcs: float
        :param velocity: Simulated object velocity, in m/sec
        :type velocity: float
        """
        self.start_x = start_x
        self.start_y = start_y
        self.start_z = start_z
        self.end_x = end_x
        self.end_y = end_y
        self.end_z = end_z
        self.rcs = rcs
        self.velocity = velocity

    def get_target_points(self, time_interval=0.1):
        """
        Calculates the individual Radar Target points, given a specified time interval.

        :param time_interval: The interval of time to determine individual Radar Target points, in sec.
        :type time_interval: float
        """
        target_points = list()

        # Calculate the distance between the two points
        distance_x = self.end_x-self.start_x
        distance_y = self.end_y-self.start_y
        distance_z = self.end_z-self.start_z
        distance_between_points = np.sqrt(np.square(distance_x)+np.square(distance_y)+np.square(distance_z))

        # Calculate the time between the points
        time_between_points = distance_between_points / self.velocity

        # Calculate the velocity vector
        factor = self.velocity / distance_between_points
        velocity_x = distance_x * factor
        velocity_y = distance_y * factor
        velocity_z = distance_z * factor
        velocity_vector = np.array([velocity_x, velocity_y, velocity_z])

        for time_msec in range(0, int(time_between_points * 1000), int(time_interval * 1000)):
            time_sec = time_msec / 1000

            # Calculate the point in space at each time
            point_x = self.start_x + (velocity_x * time_sec)
            point_y = self.start_y + (velocity_y * time_sec)
            point_z = self.start_z + (velocity_z * time_sec)
            radial_vector = np.array([-point_x, -point_y, -point_z])

            # Convert to euclidean geometry
            point_distance = np.sqrt(np.square(point_x)+np.square(point_y)+np.square(point_z))
            point_azimuth = np.arctan(point_x/point_y) * 180 / np.pi
            point_elevation = np.arctan(point_z/point_y) * 180 / np.pi

            # Calculate the angle between the velocity vector and the radial vector (to determine radial velocity)
            vector_dot_product = velocity_vector.dot(radial_vector)
            vector_norms = np.linalg.norm(velocity_vector) * np.linalg.norm(radial_vector)
            radial_vector_angle_radians = np.arccos(vector_dot_product / vector_norms)

            radial_velocity = np.linalg.norm(velocity_vector) * np.cos(radial_vector_angle_radians)

            # Create the radar target for the point (make velocity sign indicate + is coming towards sensor)
            point_radar_target = RadarTarget(distance=point_distance,
                                             rcs=self.rcs,
                                             velocity=radial_velocity,
                                             azimuth=point_azimuth,
                                             elevation=point_elevation)

            # Append to the list of points
            target_points.append(point_radar_target)

        return target_points
