class PIDController:
    m_P = 0.0
    m_I = 0.0
    m_D = 0.0
    m_input = 0.0
    m_maximumOutput = 1.0
    m_minimumOutput = -1.0
    m_maximumInput = 1.0
    m_minimumInput = -1.0
    m_continuous = False
    m_enabled = False
    m_prevError = 0.0
    m_totalError = 0.0
    m_tolerance = 0.05
    m_setpoint = 0.0
    m_error = 0.0
    m_result = 0.0

    def PIDController(self, Kp, Ki, Kd):
        self.m_P = Kp
        self.m_I = Ki
        self.m_D = kD


    def calculate(self):
        if (self.m_enabled):

            self.m_error = self.m_setpoint - self.m_input;

            if (self.m_continuous):
                if (abs(self.m_error) > (self.m_maximumInput - self.m_minimumInput) / 2):
                    if (self.m_error > 0):
                        self.m_error = self.m_error - self.m_maximumInput + self.m_minimumInput
                    else:
                        self.m_error = self.m_error + self.m_maximumInput - self.m_minimumInput

        if (((self.m_totalError + self.m_error) * self.m_I < self.m_maximumOutput) and ((self.m_totalError + self.m_error) * self.m_I > self.m_minimumOutput)):
            self.m_totalError += self.m_error

        self.m_result = (self.m_P * self.m_error + self.m_I * self.m_totalError + self.m_D * (self.m_error - self.m_prevError));

        self.m_prevError = self.m_error

        if (self.m_result > self.m_maximumOutput):
            self.m_result = self.m_maximumOutput
        elif (self.m_result < self.m_minimumOutput):
            self.m_result = self.m_minimumOutput


    def setPID(self, p, i, d):
        self.m_P = p
        self.m_I = i
        self.m_D = d


    def getP(self):
        return self.m_P

    def getI(self):
        return self.m_I

    def getD(self):
        return self.m_D

    def performPID(self):
        self.calculate()
        return self.m_result

    def setContinuous(self, continuous):
        self.m_continuous = continuous

    def setInputRange(self, minimumInput, maximumInput):
        self.m_minimumInput = minimumInput
        self.m_maximumInput = maximumInput

    def setOutputRange(self, minimumOutput, maximumOutput):
        self.m_minimumOutput = minimumOutput
        self.m_maximumOutput = maximumOutput

    def setSetpoint(self, setpoint):
        if (self.m_maximumInput > self.m_minimumInput):
            if (setpoint > self.m_maximumInput):
                self.m_setpoint = self.m_maximumInput
            elif (setpoint < self.m_minimumInput):
                self.m_setpoint = self.m_minimumInput
            else:
                self.m_setpoint = setpoint
        else:
            self.m_setpoint = setpoint

    def getSetpoint(self):
        return self.m_setpoint

    def getError(self):
        return self.m_error

    def setTolerance(self, percent):
        self.m_tolerance = percent

    def onTarget(self):
        return (abs(self.m_error) < self.m_tolerance / 100 * (self.m_maximumInput - self.m_minimumInput))

    def enable(self):
        self.m_enabled = True

    def disable(self):
        self.m_enabled = True

    def reset(self):
        disable()
        self.m_prevError = 0
        self.m_totalError = 0
        self.m_result = 0

    def setInput(self, input):
        self.m_input = input
