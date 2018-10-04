class Periodic:
    import re
    from PIDController import PIDController as PID
    from pymavlink import mavutil
    from MathUtils import MathUtils as Math

    xPID = PID()
    yPID = PID()
    zPID = PID()

    stepComplete = False

    currxLoc = 0.0
    curryLoc = 0.0
    currzLoc = 0.0

    prevxLoc = 0.0
    prevyLoc = 0.0
    prevzLoc = 0.0

    mavFrame = None

    @classmethod
    def fly(self, x, y, z):
        self.xPID.setSetpoint(x)
        self.yPID.setSetpoint(y)
        self.zPID.setSetpoint(z)

        self.currxLoc = self.getLocation()[0]
        self.curryLoc = self.getLocation()[1]
        self.currzLoc = self.getLocation()[2]

        self.xPID.setInput(self.currxLoc-self.prevxLoc)
        self.yPID.setInput(self.curryLoc-self.prevyLoc)
        self.zPID.setInput(self.currzLoc)

        xVal = self.xPID.performPID()
        yVal = self.yPID.performPID()
        zVal = self.zPID.performPID()

        minimum = 0.1

        if (abs(xVal) < minimum and not self.xPID.onTarget()):
            xVal = self.Math.signum(xVal) * minimum

        if (abs(yVal) < minimum and not self.yPID.onTarget()):
            yVal = self.Math.signum(yVal) * minimum

        if (abs(zVal) < minimum and not self.zPID.onTarget()):
            zVal = self.Math.signum(zVal) * minimum

        if (abs(self.currxLoc-x) < 0.2 and abs(self.curryLoc-y) < 0.2
                and abs(self.currzLoc-z) < 0.2):
            self.stepComplete = True
        else:
            self.stepComplete = False

        #print ""
        #print "xVal: ", xVal
        #print "yVal: ", yVal
        print "Location| X:", self.getLocation()[0], " Y:", self.getLocation()[1], " Z:", self.getLocation()[2]
        #print vehicle.parameters['FLOW_ENABLE']

        self.send_ned_velocity(xVal, yVal, zVal)

    @classmethod
    def moveComplete(self):
        return self.stepComplete

    @classmethod
    def getVelocity(self):
        global vehicle
        return vehicle.velocity

    @classmethod
    def getLocation(self):
        loc = vehicle.location.local_frame
        location = str(loc).split(',')
        currentxLoc = location[0].partition('=')[2]
        currentyLoc = location[1].partition('=')[2]
        currentzLoc = location[2].partition('=')[2]

        return float(currentxLoc), float(currentyLoc), -float(currentzLoc)

    @classmethod
    def resetLocation(self):
        self.prevxLoc = self.getLocation()[0]
        self.prevyLoc = self.getLocation()[1]

    #x = north; y = east; z = up
    @classmethod
    def send_ned_velocity(self, velocity_x, velocity_y, velocity_z):
        global vehicle
        """
        Move vehicle in direction based on specified velocity vectors.
        """
        msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0,       # time_boot_ms (not used)
            0, 0,    # target system, target component
            mavFrame, # frame
            0b0000111111000111, # type_mask (only speeds enabled)
            0, 0, 0, # x, y, z positions (not used)
            velocity_x, velocity_y, -velocity_z, # x, y, z velocity in m/s
            0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
            0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

        #print msg
        vehicle.send_mavlink(msg)

    @classmethod
    def init(self):
        self.xPID.setPID(0.56, 0.0, 0.0)
        self.xPID.setInputRange(-7.0, 7.0)
        self.xPID.setOutputRange(-1.0, 1.0)
        self.xPID.setTolerance(0.03)
        self.xPID.enable()

        self.yPID.setPID(0.56, 0.0, 0.0)
        self.yPID.setInputRange(-7.0, 7.0)
        self.yPID.setOutputRange(-1.0, 1.0)
        self.yPID.setTolerance(0.03)
        self.yPID.enable()

        self.zPID.setPID(0.33, 0.0, 0.0)
        self.zPID.setInputRange(0.0, 5.0)
        self.zPID.setOutputRange(-1.0, 1.0)
        self.zPID.setTolerance(0.03)
        self.zPID.enable()

    @classmethod
    def setVehicle(self, v, frame):
        global vehicle
        global mavFrame
        vehicle = v
        mavFrame = frame
