
Welcome to PyViewX's documentation!
***********************************

A Python package for communicating with the SMI iViewX server via UDP.


iViewXClient
============

class class PyViewX.client.iViewXClient

   Handles all communication with the iViewX server.

   acceptCalibrationPoint(callback=None)

      Accept calibration point.

      Parameters:
         **callback** (*function.*) -- A function to call with
         response.

   cancelCalibration(callback=None)

      Cancel calibration procedure.

      Parameters:
         **callback** (*function.*) -- A function to call with
         response.

   getCalibrationParam(param, callback=None)

      Get calibration parameter.

      Parameters:
         * **param** (*int.*) -- Numeric ID of calibration parameter;
           valid options are 0, 1, 2 and 3.

         * **callback** (*function.*) -- A function to call with
           response.

   getSampleRate(callback=None)

      Get sample rate.

      Parameters:
         **callback** (*function.*) -- A function to call with
         response.

   requestCalibrationResults(callback=None)

      Request calibration resuts.

      Parameters:
         **callback** (*function.*) -- A function to call with
         response.

   resetCalibrationPoints(callback=None)

      Reset calibration points to default values.

      Parameters:
         **callback** (*function.*) -- A function to call with
         response.

   setCalibrationCheckLevel(value, callback=None)

      Set calibration check level.

      Parameters:
         * **value** (*int.*) -- Calibration check level; valid values
           are 0, 1, 2 or 3.

         * **callback** (*function.*) -- A function to call with
           response.

   setCalibrationParam(param, value, callback=None)

      Set calibration parameter.

      Parameters:
         * **param** (*int.*) -- Numeric ID of calibration parameter;
           valid options are 0, 1, 2 and 3.

         * **value** (*bool.*) -- New state of calibration parameter;
           valid options are True=On, False=Off.

         * **callback** (*function.*) -- A function to call with
           response.

   setCalibrationPoint(point, x, y, callback=None)

      Set location of calibration point.

      Parameters:
         * **point** (*int.*) -- Calibration point.

         * **x** (*int.*) -- Horizontal position of calibration point
           in pixels.

         * **y** (*int.*) -- Vertical position of calibration point in
           pixels.

         * **callback** (*function.*) -- A function to call with
           response.

      Note: Not available on RED systems.

   setDataFormat(frm, callback=None)

      Set the format of streaming data.

      Parameters:
         * **frm** (*str.*) -- The format of the streamed data.

         * **callback** (*function.*) -- A function to call with
           response.

   setSizeCalibrationArea(width, height, callback=None)

      Set the size of the calibration area.

      Parameters:
         * **width** (*int.*) -- Width of calibration area in pixels.

         * **height** (*int.*) -- Height of calibration area in
           pixels.

         * **callback** (*function.*) -- A function to call with
           response.

   startCalibration(points, eye=0, callback=None)

      Start calibration procedure.

      Parameters:
         * **points** (*int.*) -- The number of calibration points;
           valid options are 2, 5, 9 or 13.

         * **callback** (*function.*) -- A function to call with
           response.

   startDataStreaming(framerate=0, callback=None)

      Start data streaming.

      Parameters:
         * **framerate** (*int.*) -- Set framerate -- 1..SampleRate.
           [*optional*]

         * **callback** (*function.*) -- A function to call with
           response.

   startDriftCorrection(callback=None)

      Start drift correction.

      Parameters:
         **callback** (*function.*) -- A function to call with
         response.

      Note: Only for hi-speed systems.

   stopDataStreaming(callback=None)

      Stop data streaming.

      Parameters:
         **callback** (*function.*) -- A function to call with
         response.

   validateCalibrationAccuracy(callback=None)

      Validate calibration accuracy.

      Parameters:
         **callback** (*function.*) -- A function to call with
         response.

   validateCalibrationAccuracyExtended(x, y, callback=None)

      Validate calibration accuracy (extended).

      Parameters:
         * **x** (*int.*) -- Horizontal position of calibration test
           point in pixels.

         * **y** (*int.*) -- Vertical position of calibration test
           point in pixels.

         * **callback** (*function.*) -- A function to call with
           response.
