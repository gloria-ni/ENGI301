"""
--------------------------------------------------------------------------
Project 1
--------------------------------------------------------------------------
License:   
Copyright 2023 Gloria Ni

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

Conduct test to analyze the tapping frequency of a patient.

Requirements:
  - Determine the average, standard deviation, minimum, and maximum frequencies 
    of a patient tapping over 30 seconds

Uses:
  - HT16K33 display library developed in class
  - Button
  - Buzzer
  - LED

"""
import time
import math

import Adafruit_BBIO.GPIO as GPIO

import LCD 
import button as BUTTON
import led as LED
import buzzer as BUZZER
import sensor as SENSOR


# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Proj():
    """ Proj """
    reset_time = None
    button     = None
    buzzer     = None
    led        = None
    LCD        = None
    sensor     = None
    
    def __init__(self, reset_time=2.0, button="P2_2", rs="P1_2", enable="P1_4", d4="P2_6",
    d5 = "P2_8", d6 = "P2_10", d7 = "P2_18", cols = 16, rows = 2, led="P2_3", buzzer="P2_1",
    sensor = "P2_4"):
        """ Initialize variables and set up display """
        self.reset_time = reset_time
        self.button     = BUTTON.Button(button)
        self.LCD        = LCD.LCD(rs, enable, d4, d5, d6, d7, cols, rows)
        self.led        = LED.LED(led)
        self.buzzer     = BUZZER.Buzzer(buzzer)
        self.sensor     = SENSOR.Sensor(sensor)
        
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """Setup the hardware components."""
        # Initialize Display
        self.LCD.clear()

    # End def


    def run(self):
        """Execute the main program."""
        
        # Instantiate variables
        freq = 0
        freq_list = []
        
        while(1):
            # Wait for button to start test
            self.LCD.message("PUSH TO START")
            self.button.wait_for_press()
                # start countdown
            self.LCD.clear()
            self.LCD.message("5")
            time.sleep(1)
            self.LCD.clear()
            self.LCD.message("4")
            time.sleep(1)
            self.LCD.clear()
            self.LCD.message("3")
            time.sleep(1)
            self.LCD.clear()
            self.LCD.message("2")
            time.sleep(1)
            self.LCD.clear()
            self.LCD.message("1")
            time.sleep(1)
            # LED, text, buzzer cue to start test
            self.LCD.clear()
            self.LCD.message("TAP NOW")
            self.led.on()
            self.buzzer.play(440, 1.0, True) 
            time.sleep(1)
            self.led.off()
            
            # Collect tapping data
            session_start_time= time.time()
            self.sensor.wait_for_tap()
            while((time.time()-session_start_time)<10):
                # Wait for tap
                old_tap_time = self.sensor.get_tap_time()
                self.sensor.wait_for_tap()
                freq = 1/(self.sensor.get_tap_time() - old_tap_time)
                freq_list.append(freq)
            # End Tapping
            # LED, text, buzzer cue to start test
            self.LCD.clear()
            self.LCD.message("TEST DONE")
            self.led.on()
            self.buzzer.play(440, 1.0, True) 
            time.sleep(1)
            self.led.off()
            
            # Analyze frequencies
            max_freq = max(freq_list)
            min_freq = min(freq_list)
            mean_freq = sum(freq_list) / len(freq_list) 
            stdev_freq = (sum([((i - mean_freq) ** 2) for i in freq_list]) / len(freq_list)) ** 0.5
            
            # End tapping
            self.LCD.clear()
            self.LCD.message("TEST DONE")
            self.LCD.clear()
            self.LCD.message("PUSH FOR AVG,SD")
            
            # Display mean & stdev
            self.button.wait_for_press()
            disp_text = "AVG-" + str(mean_freq)[0:4] + " STD-" + str(stdev_freq)[0:3]
            self.LCD.clear()
            self.LCD.message(disp_text)
            
            # Display min & max
            self.button.wait_for_press()
            self.LCD.clear()
            self.LCD.message("PUSH FOR MAX,MIN")
            self.button.wait_for_press()
            disp_text = "MIN-" + str(min_freq)[0:4] + " MAX-" + str(max_freq)[0:3]
            self.LCD.clear()
            self.LCD.message(disp_text)
            
            # END
            self.button.wait_for_press()
            self.LCD.clear()
            self.LCD.message("COMPLETE")
            time.sleep(1)
            self.LCD.clear()
            break
    # End def


    def cleanup(self):
        """Cleanup the hardware components."""
        
        self.LCD.clear()
        self.LCD.message("DEAD")
        
    # End def

# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Program Start")

    # Create instantiation of the program
    proj = Proj()
    
    try:
        # Run
        proj.run()

    except KeyboardInterrupt:
        # Clean up hardware when exiting
        proj.cleanup()

    print("Program Complete")