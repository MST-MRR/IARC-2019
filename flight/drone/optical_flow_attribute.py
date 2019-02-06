from dronekit import Vehicle


class OpticalFlow(object):
    """
    The Optical Flow readings.
    
    The message definition is here: https://pixhawk.ethz.ch/mavlink/#RAW_IMU  ???
    
    :param time_usec: Timestamp
    :param sensor_id: Sensor ID
    :param flow_x: Flow in X sensor direction
    :param flow_y: Flow in Y sensor direction
    :param flow_comp_m_x: Flow in x-sensor direction, angular-speed compensated
    :param flow_comp_m_y: Flow in y-sensor direction, angular-speed compensated
    :param quality: Optical flow quality / confidence. 0: bad, 255: maximum quality
    :param ground_distance: Ground distance. Positive value: distance known. Negative value: Unknown distance   
    """
    def __init__(self, time_usec=None, sensor_id=None, flow_x=None, flow_y=None, xygro=None, flow_comp_m_y=None, quality=None, ground_distance=None):
        """
        RawIMU object constructor.
        """
        self.time_usec = time_usec
        self.sensor_id = sensor_id
        self.flow_x = flow_x
        self.flow_y = flow_y
        self.flow_comp_m_x = quality
        self.flow_comp_m_y = flow_comp_m_y
        self.quality = quality
        self.ground_distance = ground_distance             
        
    def __str__(self):
        """
        String representation used to print the RawIMU object. 
        """
        return "RAW_IMU: time_usec={},sensor_id={},flow_x={},flow_y={},flow_comp_m_x={},flow_comp_m_y={},quality={},ground_distance={}".format(self.time_usec, self.sensor_id, self.flow_x,self.flow_y,self.flow_comp_m_x,self.flow_comp_m_y,self.quality,self.ground_distance)
     

    @property
    def optical_flow(self):
        return self._optical_flow