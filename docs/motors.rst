..
   This manual is copyright 2018 Bruce Ravel and released under
   The Creative Commons Attribution-ShareAlike License
   http://creativecommons.org/licenses/by-sa/3.0/

.. |nbsp| unicode:: 0xA0 
   :trim:

.. _motors:

Moving and querying motors
==========================

To get an overview of the state of the beamline motors, do ``%m`` at
the bsui command line.  Here is an example:

.. code-block:: text

   In [1897]: %m
   ==============================================================================
   Energy = 19300.1   reflection = Si(111)   mode = fixed
        Bragg =  5.87946   2nd Xtal Perp = 15.0792   2nd Xtal Para = 146.4328

   M2
        vertical =   6.000 mm           YU  =   6.000
        lateral  =   0.000 mm           YDO =   6.000
        pitch    =   0.000 mrad         YDI =   6.000
        roll     =  -0.001 mrad         XU  =  -0.129
        yaw      =   0.200 mrad         XD  =   0.129

   M3
        vertical =   0.000 mm           YU  =  -1.167
        lateral  =  15.001 mm           YDO =   1.167
        pitch    =   3.500 mrad         YDI =   1.167
        roll     =   0.000 mrad         XU  =  15.001
        yaw      =   0.001 mrad         XD  =  15.001

   Slits3:   vsize  vcenter  hsize   hcenter     top    bottom    outboard  inboard
             1.350   0.000   8.000  -0.000      0.675   -0.675    4.000   -4.000

   DM3_BCT:  45.004 mm

   XAFS table:
        vertical  pitch    roll   YU     YDO     YDI
        132.000   0.000   0.000 132.000 132.000 132.000

   XAFS stages:
             x        y     roll    pitch    linxs    roth    wheel     rots
           9.224  115.000   0.840   0.000  -45.000    0.000  -59.000    0.000
   ==============================================================================


.. _sample_stages:

Sample stages
-------------

These stages sit on top of the XAFS optical table.  The nickname is a
short string that can be used in the ``linescan()`` plan and certain
other places instead of writing out the BlueSky name for the motor.

.. table:: XAFS sample stages
   :name:  xafs-stages
   :align: left

   ========== ===========  =========  =======================  ===================================
   motor      type         units      notes                    directions
   ========== ===========  =========  =======================  ===================================
   xafs_x     linear       mm         main sample stage        |plus| outboard, - inboard
   xafs_y     linear       mm         main sample stage        |plus| up, - down
   xafs_det   linear       mm         detector mount           |plus| closer to sample, - farther
   xafs_wheel rotary       degrees    *ex situ* sample wheel   |plus| clockwise, - widdershins
   xafs_linxs linear       mm         ref wheel vertical       |plus| up, - down
   xafs_ref   rotary       degrees    reference stage          |plus| clockwise, - widdershins
   xafs_pitch tilt         degrees    Huber tilt stage         |plus| more positive
   xafs_roll  tilt         degrees    Huber tilt stage         |plus| more positive
   xafs_rots  rotary       degrees    small rotary stage   
   xafs_roth  rotary       degrees    Huber circle         
   ========== ===========  =========  =======================  ===================================

Configuration and position of the motors can be queried easily.  In
the following examples, the ``xafs_y`` motor is used.  The commands
are the same for all sample stage motors.

**Querying position**
   The position of any motor can be queried with a command line like ::

      %w xafs_y 

**Moving to a new position**
   Always move motors through the run engine, for example: ::

      RE(mvr(xafs_y, 10))

   ``mvr`` is the relative move command |nd| the numerical argument is
   the amount by which the motor will move from the current position.

   ``mv``, as in::

      RE(mv(xafs_y, 37.63))

   is the absolute move command.  The numerical argument is the
   position to which the motor will move.

   All movements are logged in the :numref:`experimental log (Section %s) <logfile>`

**Moving to a new position in a plan**
   To move a sample stage as part of a :numref:`macro (Section %s)
   <macro>` , do::

     yield from mv(xafs_y, 37.36)

   You can combine motions of two or more motors in a single
   synchronous movement::

     yield from mv(xafs_y, 37.36, xafs_x, 15.79)

   Similarly::

     yield from mvr(xafs_y, 5)

**Querying soft limits**
   To know the soft limits on a sample stage, do
   ``xafs_y.llm.value`` or ``xafs_y.hlm.value`` for the low or
   high limit. 

**Setting soft limits**
   To set the soft limits on a sample stage, do something like
   ``xafs_y.llm.value = 5`` or ``xafs_y.hlm.value = 85``

**Reference wheel** 
   The reference stage _`Reference` is a rotation stage with a `Delrin
   <https://en.wikipedia.org/wiki/Polyoxymethylene>`_ sample disk
   holding up to 24 reference foils.  It is calibrated such that the
   beam passes through the center of a slot every 15 degrees.  The
   slots are indexed such that they can be accessed by the symbol of
   the element being measured.  To move to a new reference foil::

     RE(reference('Fe'))

   To see the available foils, do ``%se``

   BMM has stable oxide references for all lanthanides except Pm as
   well as metal or oxide references for most other elements within
   the measurement range of the beamline that are not normally mounted
   on the reference wheel.

   `Here is a complete list of standards
   <https://nsls-ii-bmm.github.io/bmm-standards/BMM-standards.html>`__
   in BMM's collection.


Sample wheel
------------

The ``xafs_wheel`` motor is a rotary stage that is typically mounted
on the XY stage.  It can be mounted face-on to the beam or at 45
degrees for use with the fluorescence detector.

Sample plates laser cut from plastic sheet (initially we used `Delrin
<https://en.wikipedia.org/wiki/Polyoxymethylene>`_, since COVID made
supply difficult, we use whatever we can get) are attached to the
rotation stage.  The single-ring version of these plates have 24 slots
arranged around the periphery, evenly spaced 15 degree apart.  The
double-ring version has concentric rings of 24 slots each.  These are
still 15 degrees apart.  The radius of the outer ring is 26 mm larger
than the radius of the inner ring.

While you can move from slot to slot in increments of 15 degrees, i.e.

.. code-block:: python

   RE(mvr(xafs_wheel, 15*3))

it is somewhat easier to move by slot number.  The sample plates are
cut with sample numbers for slots 1, 7, 13, and 19, making it clear
which slot is which.  The wheel is mounted such that the numbers can
be read normally on the side facing the beam.

To move, for instance, to slot 5, do:

.. code-block:: python

   RE(slot(5))

In a macro, do

.. code-block:: python

   yield from slot(5)

To move to the inner or outer ring, do

.. code-block:: python

   RE(xafs_wheel.inner())
   RE(xafs_wheel.outer())

This translates ``xafs_x`` by |nbsp|  |pm| 26 mm.

In a macro, do

.. code-block:: python

   yield from xafs_wheel.inner()
   yield from xafs_wheel.outer()


..
   Sample spinner
   --------------

   The sample spinner is a 12 volt CPU cooling fan mounted on a plate
   which is mounted on the tilt stage.  It is used to spin crystalline
   samples in an effort to suppress Bragg peaks which might enter the
   fluorescence detector.

   To turn the spinner on and off::

     fan.on()
     fan.off()

   To turn the spinner on or off in a :numref:`macro (Section %s) <macro>`::

     yield from fan.on_plan()
     yield from fan.off_plan()

   The spinner should **always** be turned off before entering the end
   station.  It is a good idea to always have a camera pointed at the
   spinner while it is use.


Glancing angle stage
--------------------

The glancing angle stage, shown in :numref:`Figure %s <fig-gastage>`,
can hold up to eight samples and allows each sample to spin
independently.  The spinning allows spurious diffraction from a
crystalline substrate into the fluorescence detector to be suppressed.

.. _fig-gastage:
.. figure::  _images/glancing_angle_stage.jpg
   :target: _images/glancing_angle_stage.jpg
   :width: 50%
   :align: center

   The glancing angle stage with 8 sample positions.

To move to a sample position::

  RE(ga.to(<N>))

where ``<N>`` is a number from 1 to 8, as shown by the labels in
:numref:`Figure %s <fig-gastage>`.  This command will rotate that
sample into the beam path and start the sample spinning.

To turn a spinner on or off::

  ga.on(<N>)
  ga.off(<N>)

To turn off all spinners::

  ga.alloff()

In a plan::

  yield from ga.on_plan()
  yield from ga.off_plan()
  yield from ga.alloff_plan()



Sample alignment
~~~~~~~~~~~~~~~~

A sample is aligned into the beam by moving the tilt stage to an
approximately flat position::

  RE(mv(xafs_pitch(0))

Then performing the following sequence::

  RE(linescan(xafs_y, 'It', -1, 1, 41))
  RE(linescan(xafs_pitch, 'It', -2, 2, 41))

At the and of the ``xafs_y`` scan, pick the position halfway down the
edge in the It signal.  At the end of the ``xafs_pitch`` scan, select
the peak position.  This will place the sample such that it is flat
relative to the incident beam direction and halfway blocking the beam.

You may choose to iterate those two scans.

Next move the sample to the measurement angle.  Suppose the
measurement angle is 2.5 degrees::

  RE(mv(xafs_pitch, 2.5))

Finally, position the sample so that the beam is hitting the center of
the sample::

  RE(linescan(xafs_y, 'If', -1, 1, 41))

Since the sample is not at the eucentric of the tilt stage, this final
vertical scan is always necessary.  When first aligning the sample,
you may need to center the sample in ``xafs_x`` as well::

  RE(linescan(xafs_x, 'If', -6, 6, 41))

You will almost certainly need to scan over a longer range.  Make sure
the detector is retracted far enough to allow for this motion.


Automated alignment
~~~~~~~~~~~~~~~~~~~

The sequence described above can be automated in many cases::

  RE(ga.auto_align(2.5))

This will run the sequence of alignment scans described above,
pitching the sample to the user-specified angle before the vertical
scan measuring the fluorescence signal.  This works by fitting an
error function to the ``xafs_y`` scan versus It, selecting the peak of
the pitch scan, then selecting the peak of the ``xafs_y`` scan versus
fluorescence.

.. _fig-ga_alignment:
.. figure::  _images/spinner-alignment.png
   :target: _images/spinner-alignment.png
   :width: 50%
   :align: center

   If all goes well, the result of the sample alignment looks like
   this.  A picture like this is posted to :numref:`Slack (Section %s)
   <slack>`.


For very flat samples which are square or circular and about 5mm
across or larger, this alignment algorithm is very robust.  For oddly
shaped samples, verify that the automation works before relying upon
it.  Otherwise, simply do the alignment by hand.

Table motors
------------

Typically, table motors are not moved individually.  When changing
:numref:`photon delivery system modes (Section %s) <change-mode>`, the
table should be put into the correct orientation such that the beam
passes through the center of the ion chambers.  It is very easy to put
the beamline in a confusing state by changing the table motors outside
of the ``change_mode()`` command.

The lateral table motors |nd| and its yaw |nd| are normally disabled.


.. table:: XAFS table motors
   :name:  xafs-table
   :align: left

   ==============   ========  =================================
   motor            units     notes
   ==============   ========  =================================
   xafs_yu          mm        upstream table jack
   xafs_ydi         mm        downstream, inboard table jack
   xafs_ydo         mm        downstream, outboard table jack
   xafs_vertical    mm        coordinated linear motion
   xafs_pitch       degrees   coordinated table pitch
   xafs_roll        degrees   coordinated table roll
   ==============   ========  =================================


**Querying table position**
   The position of any motor can be queried with a command line like
   ``%w xafs_table``.

**Moving table motors**
   The normal movement commands work on the real and virtual motors,
   e.g.::

      RE(mvr(xafs_ydi, 3))
      RE(mv(xafs_vertical, 107))

   Again, this is rarely necessary.  The mode changing plan should
   leave the table in the correct location for your experiment.

   All table movements are recorded in the :numref:`experimental log
   (Section %s) <log>`.
