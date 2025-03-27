
..
   This document was developed primarily by a NIST employee. Pursuant
   to title 17 United States Code Section 105, works of NIST employees
   are not subject to copyright protection in the United States. Thus
   this repository may not be licensed under the same terms as Bluesky
   itself.

   See the LICENSE file for details.


.. _other_measurements:

Other measurement needs
=======================

.. attention:: Unfinished section

SEAD
----

Single energy absorption detection

Term coined in `a paper by Filipponi et al. <https://doi.org/10.1088/0953-8984/10/1/026>`__


explain INI file, plotting, dossier


Raster
------

Single ROI area scans.  A map of sorts.

explain INI file, plotting, dossier


Wafers
------

There is some functionality specifically for measuring films grown on
large, round wafers.  The basic experiment involves measuring XAS of 1
or more edges from selected positions on a film.  BMM has sample
holders specifically designed for holding standard size silica or
crystalline wafers.

Most such experiments involve reliable motion to specific locations on
the film.  This usually starts with finding the center of the wafer
and indexing locations relative to the center.

The method for finding the center involves finding the X,Y coordinates
of three points around the periphery of the wafer, then using
`geometry <https://docs.sympy.org/latest/modules/geometry/index.html>`__
to find the `center of the circle
<https://docs.sympy.org/latest/modules/geometry/polygons.html#sympy.geometry.polygon.Triangle.circumcenter>`__
intersecting those three points.

``RE(wafer.edge())`` 
    With the focused beam in the vicinity of a point on the edge of
    the wafer, make a scan in ``xafs_x``, plotting the signal on I\
    :sub:`t`, to find the X,Y coordinates of a point in the edge.
    This method will execute the :numref:`linescan (Section %s)
    <linescan>`, fit a lineshape to the measurement, then move to the
    position of the wafer's edge.
    This must be repeated three times on three widely spaced
    points.

``wafer.push()``
    After finding a point using ``RE(wafer.edge())``, push the current
    X,Y coordinates to a list.  After three measurements of the wafer
    edge, this list will contain the three X,Y
    coordinates of edge points.

``wafer.points``
    The list containing the three edge points.

``wafer.find_center()``
    Compute the wafer center from the contents of ``wafer.points``.

``RE(wafer.goto.center())``
    Move the ``xafs_x`` and ``xafs_y`` stages to the center position.

``wafer.center``
    The center position of the wafer.

``wafer.clear()``
    Clear the contents of ``wafer.points`` in order to start over.


Glancing angle stage
--------------------

The glancing angle stage allows you to automate the alignment and
measurement of up to 8 sample, optionally spinning the samples to
suppress diffraction peaks from crystalline substrates.

This is not intended as a standing wave experiment.  The angle chosen
for the incident beam relative to the sample is usually large compared
to the critical angle.

Rather, the purpose of this instrument is to spread the beam out over
the surface of the sample by placing the sample at a shallow angle to
the incident beam.  This significantly increases the number of atoms
contributing to the measurement, thus increasing the signal going to
the fluorescence detector.

Here are all the commands related to the operation of the glancing
angle stage.

``RE(ga.to(N))``
   Rotate to sample N (N is an integer between 1 and 8).  All spinners
   are halted and spinner N is started, unless ``ga.spin`` is False.

``RE(ga.auto_align(angle))``
   Run the :numref:`automated alignment procedure (Section %s)
   <auto_ga>` to align the sample at the specified angle (in degrees)
   relative the flat position.

   The automated alignment procedure should always start when the
   stage is flat or approximately flat relative to the incoming beam.
   If you just aligned another sample, you should do either

   .. code-block:: python

      RE(ga.flatten())

   or

   .. code-block:: python

      RE(mvr(xafs_pitch, -angle))

   where ``angle`` is the argument to the previous
   ``ga.auto_align())`` command or the angle to moved to if doing the
   alignment by hand.

``RE(ga.flatten())``
   For a sample that has been aligned by the automated alignment
   procedure, return the sample to the position of flat and parallel
   to the beam.

``ga.spin``
   This is True if the sample should be spinning during measurement.
   So

   .. code-block:: python

      ga.spin = True

   or

   .. code-block:: python

      ga.spin = False

``ga.orientation`` 
   This is a string, either ``parallel`` or ``perpendicular``
   depending on the orientation of the sample stage.  This orientation
   is referring to the relative orientation of the surface of the
   spinning sample and the electric vector of the incident beam.  So

   .. code-block:: python

      ga.orientation = 'parallel'

   or

   .. code-block:: python

      ga.orientation = 'perpendicular'

``ga.on(N)``
   Turn on spinner N, where N is an integer between 1 and 8

``ga.off(N)``
   Turn off spinner N, where N is an integer between 1 and 8

``ga.alloff()``
   Turn off all spinners.

Once a sample is aligned and placed at the correct angle, you need to
set the detector position to optimize the fluorescence signal.  Here
are the relevant commands:

``%xrf``
   Measure an display a fluorescence spectrum.  You want the total
   count rate (the OCR column in the table printed to the screen) to
   be around 200,000 counts on each of the 7 channels.  Not the sum of
   channel!  Each channel can be as high as 200,000 counts.

``RE(mv(xafs_detx, YYY))`` 
   Move the detector to a new position, ``YYY``, where that indicates
   a floating point number, typically something between 10 and 205.
   When you move the detector to a new position, always remeasure the
   XRF spectrum with ``%xrf``.

   The fully retracted position is 205.  The closest position is
   usually set as a software limit when the experiment is being set
   up.


