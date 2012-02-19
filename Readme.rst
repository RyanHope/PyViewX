
Welcome to PyViewX's documentation!
***********************************

A Python package for communicating with the SMI iViewX server via UDP.


iViewXClient
============

class class PyViewX.client.iViewXClient

   Handles all communication with the iViewX server.

   acceptCalibrationPoint(callback=None)

      Accepts the current calibration point during the calibration
      process, and switches to the next calibration point. Returns the
      number of the next calibration point if successful. Available
      only during calibration.

      Parameters:
         **callback** (*function.*) -- A function to call with
         response.

      *The command is sent by iViewX every time a calibration point is
      accepted during calibration, either manually by the user or
      automatically.*

   cancelCalibration(callback=None)

      Cancels the calibration procedure.

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

      Returns current sample rate.

      Parameters:
         **callback** (*function.*) -- A function to call with
         response.

   requestCalibrationResults(callback=None)

      Requests iViewX for calibration results and returns the gaze
      data aquired for a specific calibration point.

      Parameters:
         **callback** (*function.*) -- A function to call with
         response.

   resetCalibrationPoints(callback=None)

      Sets all calibration points to default positions.

      Parameters:
         **callback** (*function.*) -- A function to call with
         response.

   setCalibrationCheckLevel(value, callback=None)

      Sets check level for calibration. Returns the new check level is
      successful.

      Parameters:
         * **value** (*int.*) -- Calibration check level; valid values
           are 0=none, 1=weak, 2=medium or 3=strong.

         * **callback** (*function.*) -- A function to call with
           response.

   setCalibrationParam(param, value, callback=None)

      Sets calibration parameters.

      +-------+------------------------+---------+---------+
      | param | description            | value=0 | value=1 |
      +=======+========================+=========+=========+
      | 0     | wait for valid data    | off     | on      |
      +-------+------------------------+---------+---------+
      | 1     | randomize point order  | off     | on      |
      +-------+------------------------+---------+---------+
      | 2     | auto accept            | off     | on      |
      +-------+------------------------+---------+---------+
      | 3     | calibration speed      | slow    | fast    |
      +-------+------------------------+---------+---------+

      Parameters:
         * **param** (*int.*) -- Numeric ID of calibration parameter.

         * **value** (*int.*) -- New state of calibration parameter.

         * **callback** (*function.*) -- A function to call with
           response.

   setCalibrationPoint(point, x, y, callback=None)

      Sets the position of a given calibration point.

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

      Sets data format for data output. The syntax is similar to the
      'C' string formatting syntax. Each format specifier is marked by
      a preceding percentage (%) symbol.

      +------------------+-----------------------------------------------------+
      | Format specifier | Description                                         |
      +==================+=====================================================+
      | TS               | timestamp in milliseconds (0 ...2^64/1000 ms)       |
      +------------------+-----------------------------------------------------+
      | TU               | timestamp in microseconds (0 ...2^64 μs)            |
      +------------------+-----------------------------------------------------+
      | DX,DY            | pupil diameter (0 ...2^32 pixels) x 32              |
      +------------------+-----------------------------------------------------+
      | PX,PY            | pupil position (± 2^31 pixels) x 32                 |
      +------------------+-----------------------------------------------------+
      | CX,CY            | corneal reflex position (± 2^31 pixels) x 32        |
      +------------------+-----------------------------------------------------+
      | SX,SY            | gaze position (± 2^31 pixels)                       |
      +------------------+-----------------------------------------------------+
      | SC               | scene counter                                       |
      +------------------+-----------------------------------------------------+
      | ET               | eye type information (l-left, r-right, b-binocular) |
      +------------------+-----------------------------------------------------+

      Example for monocular data:
         **%TS: %SX, %SY**

      Result:
         **28437864110: 400, 202**

      Example for binocular data:
         **%ET %SX %SY**

      Result:
         **b 399 398 200 199**

      Parameters:
         **frm** (*str.*) -- The format of the streamed data.

   setSizeCalibrationArea(width, height, callback=None)

      Sets the size of the calibration area.

      Parameters:
         * **width** (*int.*) -- Width of calibration area in pixels.

         * **height** (*int.*) -- Height of calibration area in
           pixels.

         * **callback** (*function.*) -- A function to call with
           response.

      *The command is sent by iViewX when the size of the calibration
      area is changed.*

   startCalibration(points, eye=0, callback=None)

      Starts a calibration. Returns calibration information is
      successful.

      Parameters:
         * **points** (*int.*) -- The number of calibration points;
           valid options are 2, 5, 9 or 13.

         * **eye** (*int.*) -- The eye to use for binocular systems;
           valid options are 1-right or 2-left.

         * **callback** (*function.*) -- A function to call with
           response.

   startDataStreaming(framerate=0)

      Starts continuous data output (streaming) using the output
      format specified with the "setDataFormat()" command. Optionally,
      the frame rate can be set at which the data will be streamed.

      Parameters:
         **framerate** (*int.*) -- Set framerate -- 1..SampleRate.
         [*optional*]

   startDriftCorrection(callback=None)

      Starts drift correction. Drift correction is available after a
      calibration of the system. Drift correction uses the first
      calibration point, which is usually the center point, as
      calibration point.

      Parameters:
         **callback** (*function.*) -- A function to call with
         response.

      Note: Only for hi-speed systems.

   stopDataStreaming()

      Stops continuous data output (streaming).

   validateCalibrationAccuracy(callback=None)

      Performs a validation of the calibration accuracy. This command
      is available only if a successful calibration has been performed
      previously. The result shows the accuracy of the calibration and
      therefore indicates its quality. With the return values you can
      estimage before starting the experiment, how good the
      measurement will be.

      Parameters:
         **callback** (*function.*) -- A function to call with
         response.

   validateCalibrationAccuracyExtended(x, y, callback=None)

      Performs an extended calibration validation of a single point.
      This command is available only if a successful calibration has
      been performed previously. THe result shows the accuracy of the
      calibration and therefore indicates its quality. With the return
      values you can estimate before starting the experiment, how good
      the measurement will be.

      Parameters:
         * **x** (*int.*) -- Horizontal position of calibration test
           point in pixels.

         * **y** (*int.*) -- Vertical position of calibration test
           point in pixels.

         * **callback** (*function.*) -- A function to call with
           response.
