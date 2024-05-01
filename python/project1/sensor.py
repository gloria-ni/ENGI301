"""
--------------------------------------------------------------------------
Sensor Driver
--------------------------------------------------------------------------
License:   
Copyright 2021-2024 - Gloria Ni

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Sensor Driver

  This driver can support sensors that have either a pull up resistor between the
sensor and the processor pin (i.e. the input is "High" / "1" when the sensor is
not tapped) and will be connected to ground when the sensor is tapped (i.e. 
the input is "Low" / "0" when the sensor is tapped), or a pull down resistor 
between the sensor and the processor pin (i.e. the input is "Low" / "0" when the 
sensor is not tapped) and will be connected to power when the sensor is tapped
(i.e. the input is "High" / "1" when the sensor is tapped).

  To select the pull up configuration, tap_low=True.  To select the pull down
configuration, tap_low=False.


Software API:

  Sensor(pin, tap_low)
    - Provide pin that the sensor monitors
    
    wait_for_tap()
      - Wait for the sensor to be tapped 
      - Function consumes time
        
    is_tapped()
      - Return a boolean value (i.e. True/False) on if sensor is tapped
      - Function consumes no time
    
    get_tap_time
      - Return the time the sensor was last tapped

    cleanup()
      - Clean up HW
      
    Callback Functions:
      These functions will be called at the various times during a sensor 
      tap cycle.  There is also a corresponding function to get the value
      from each of these callback functions in case they return something.
    
      - set_tapped_callback(function)
        - Excuted every "sleep_time" while the sensor is tapped
      - set_untapped_callback(function)
        - Excuted every "sleep_time" while the sensor is untapped
      - set_on_tap_callback(function)
        - Executed once when the sensor is tapped
      - set_on_release_callback(function)
        - Executed once when the sensor is released
      
      - get_tapped_callback_value()
      - get_untapped_callback_value()
      - get_on_tap_callback_value()
      - get_on_release_callback_value()      


"""
import time

import Adafruit_BBIO.GPIO as GPIO

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

HIGH          = GPIO.HIGH
LOW           = GPIO.LOW

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Sensor():
    """ Sensor Class """
    pin                           = None
    
    untapped_value               = None
    tapped_value                 = None
    
    sleep_time                    = None
    tap_time                      = None

    tapped_callback              = None
    tapped_callback_value        = None
    untapped_callback            = None
    untapped_callback_value      = None
    on_tap_callback             = None
    on_tap_callback_value       = None
    on_release_callback           = None
    on_release_callback_value     = None
    
    
    def __init__(self, pin=None, tap_low=True, sleep_time=0.1):
        """ Initialize variables and set up the sensor """
        if (pin == None):
            raise ValueError("Pin not provided for Sensor()")
        else:
            self.pin = pin
        
        # For pull up resistor configuration:    tap_low = True
        # For pull down resistor configuration:  tap_low = False
        if tap_low:
            self.untapped_value = HIGH
            self.tapped_value   = LOW
        else:
            self.untapped_value = LOW
            self.tapped_value   = HIGH
        
        # By default sleep time is "0.1" seconds
        self.sleep_time      = sleep_time
        self.tap_duration  = 0.0        

        # Initialize the hardware components        
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """ Setup the hardware components. """
        # Initialize sensor
        # Set up the sensor
        GPIO.setup(self.pin, GPIO.IN )
        pass

    # End def


    def is_tapped(self):
        """ Is the Sensor tapped?
        
           Returns:  True  - Sensor is tapped
                     False - Sensor is not tapped
        """
        #   Compare input value of the GPIO pin of the sensor (i.e. self.pin) to the "tapped value" of the class 
        
        return GPIO.input(self.pin)==self.tapped_value;

    # End def


    def wait_for_tap(self):
        """ Wait for the sensor to be tapped.  This function will 
           wait for the sensor to be tapped and released so there
           are no race conditions.
           
           Use the callback functions to peform actions while waiting
           for the sensor to be tapped or get values after the sensor
           is tapped.
        
           Arguments:  None
           Returns:    None
        """
        tap_time = None
        
        # Wait for sensor tap
        #   Execute the untapped callback function based on the sleep time
        #   Update while loop condition to compare the input value of the  
        #   GPIO pin of the sensor (i.e. self.pin) to the "untapped value" 
        #   of the class (i.e. we are executing the while loop while the 
        #   sensor is not being tapped)
        #
        while(GPIO.input(self.pin)==self.untapped_value):
        
            if self.untapped_callback is not None:
                self.untapped_callback_value = self.untapped_callback()
            
            time.sleep(self.sleep_time)
            

        
        # Executed the on tap callback function
        if self.on_tap_callback is not None:
            self.on_tap_callback_value = self.on_tap_callback()
        
        # Wait for sensor release
        #   Execute the tapped callback function based on the sleep time
        #
        # HW#4 TODO: (one line of code)
        #   When the input value of the GPIO pin of the sensor (self.pin) equals the "tapped value" 
        #   of the class (i.e. while the sensor is being tapped), update the tap time

        while(GPIO.input(self.pin)==self.tapped_value):
        
            if self.tapped_callback is not None:
                self.tapped_callback_value = self.tapped_callback()
                
            time.sleep(self.sleep_time)
        
        # Record the tap time
        self.tap_time = time.time()

        # Executed the on release callback function
        if self.on_release_callback is not None:
            self.on_release_callback_value = self.on_release_callback()        
        
    # End def

    
    def get_tap_time(self):
        """ Return the most recent tap time """
        return self.tap_time
    
    # End def
    
    
    def cleanup(self):
        """ Clean up the sensor hardware. """
        # Nothing to do for GPIO
        pass
    
    # End def
    
    
    # -----------------------------------------------------
    # Callback Functions
    # -----------------------------------------------------

    def set_tapped_callback(self, function):
        """ Function excuted every "sleep_time" while the sensor is tapped """
        self.tapped_callback = function
    
    # End def

    def get_tapped_callback_value(self):
        """ Return value from tapped_callback function """
        return self.tapped_callback_value
    
    # End def
    
    def set_untapped_callback(self, function):
        """ Function excuted every "sleep_time" while the sensor is untapped """
        self.untapped_callback = function
    
    # End def

    def get_untapped_callback_value(self):
        """ Return value from untapped_callback function """
        return self.untapped_callback_value
    
    # End def

    def set_on_tap_callback(self, function):
        """ Function excuted once when the sensor is tapped """
        self.on_tap_callback = function
    
    # End def

    def get_on_tap_callback_value(self):
        """ Return value from on_tap_callback function """
        return self.on_tap_callback_value
    
    # End def

    def set_on_release_callback(self, function):
        """ Function excuted once when the sensor is released """
        self.on_release_callback = function
    
    # End def

    def get_on_release_callback_value(self):
        """ Return value from on_release_callback function """
        return self.on_release_callback_value
    
    # End def    
    
# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Sensor Test")

    # Create instantiation of the sensor
    sensor = Sensor("P2_4")
    
    # Create functions to test the callback functions
    def tapped():
        print("  Sensor tapped")
    # End def
    
    def untapped():
        print("  Sensor not tapped")
    # End def

    def on_tap():
        print("  On Sensor tap")
        return 3
    # End def

    def on_release():
        print("  On Sensor release")
        return 4
    # End def    

    # Use a Keyboard Interrupt (i.e. "Ctrl-C") to exit the test
    try:
        # Check if the sensor is tapped
        print("Is the sensor tapped?")
        print("    {0}".format(sensor.is_tapped()))

        
        # Check if the sensor is tapped
        print("Is the sensor tapped?")
        print("    {0}".format(sensor.is_tapped()))
        
        print("Release the sensor.")
        time.sleep(4)
        
        print("Waiting for sensor tap ...")
        sensor.wait_for_tap()
        print("    Sensor tapped at {0} seconds. ".format(sensor.get_tap_time()))
        
        print("Setting callback functions ... ")
        sensor.set_tapped_callback(tapped)
        sensor.set_untapped_callback(untapped)
        sensor.set_on_tap_callback(on_tap)
        sensor.set_on_release_callback(on_release)
        
        print("Waiting for sensor with callback functions ...")
        value = sensor.wait_for_tap()
        print("    Sensor tapped at {0} seconds. ".format(sensor.get_tap_time()))
        print("    Sensor tapped callback return value    = {0} ".format(sensor.get_tapped_callback_value()))
        print("    Sensor untapped callback return value  = {0} ".format(sensor.get_untapped_callback_value()))
        print("    Sensor on tap callback return value   = {0} ".format(sensor.get_on_tap_callback_value()))
        print("    Sensor on release callback return value = {0} ".format(sensor.get_on_release_callback_value()))        
        
    except KeyboardInterrupt:
        pass

    print("Test Complete")

