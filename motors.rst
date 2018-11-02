..
   This manual is copyright 2018 Bruce Ravel and released under
   The Creative Commons Attribution-ShareAlike License
   http://creativecommons.org/licenses/by-sa/3.0/


.. _motors:

Moving and querying motors
==========================

To get an overview of the state of the beamline motors, do ``ms()`` at
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
           linx     liny    roll    pitch    linxs    roth     rotb     rots
           9.224  115.000   0.840   0.000  -45.000    0.000  -59.000    0.000
   ==============================================================================



Sample stages
-------------

These stages sit on top of the XAFS optical table.  The nickname is a
short string that can be used in the ``linescan()`` plan and certain
other places instead of writing out the BlueSky's name for the motor.

.. table:: XAFS sample stages
   :name:  xafs-stages

   ========== ========= ===========  =========  ===================  ===============================
   motor      nickname  type         units      notes                directions
   ========== ========= ===========  =========  ===================  ===============================
   xafs_linx  x         linear       mm         main sample stage    |plus| outboard, - inboard
   xafs_liny  y         linear       mm         main sample stage    |plus| up, - down
   xafs_linxs xs        linear       mm         reference stage      |plus| up, - down
   xafs_pitch pitch     tilt         degrees    Huber tilt stage     |plus| more positive
   xafs_roll  roll      tilt         degrees    Huber tilt stage     |plus| more positive
   xafs_roth  rh        rotary       degrees    Huber circle         |plus| more positive
   xafs_rotb  rb        rotary       degrees    large rotary stage   |plus| more positive
   xafs_rots  rs        rotary       degrees    small rotary stage   |plus| more positive
   ========== ========= ===========  =========  ===================  ===============================

Configuration and position of the motors can be queried easily.  In
the following examples, the ``xafs_liny`` motor is used.  The commands
are the same for all sample stage motors.

**Querying position**
   The position of any motor can be queried with a command line like
   ``%w xafs_liny``. 

**Moving to a new position**
   Always move motors through the run engine, for example: ::

      RE(mvr(xafs_liny, 10))

   ``mvr`` is the relative move command |nd| the numerical argument is
   the amount to move from the current position. ``mv``, as in::

      RE(mv(xafs_liny, 37.63))

   is the absolute move command.  The numerical argument is the
   position to which the motor will move.

   All movements are logged in the :numref:`experimental log (Section %s) <log>`

**Moving to a new position in a plan**
   To move a sample stage as part of a :numref:`macro (Section %s)
   <macro>` , do::

     yield from mv(xafs_liny, 37.36)

   You can combine motions of two or more motors in a single
   synchronous movement::

     yield from mv(xafs_liny, 37.36, xafs_linx, 15.79)


**Querying soft limits**
   To know the soft limits on a sample stage, do
   ``xafs_liny.llm.value`` or ``xafs_liny.hlm.value`` for the low or
   high limit. 

**Setting soft limits**
   To set the soft limits on a sample stage, do something like
   ``xafs_liny.llm = 5`` or ``xafs_liny.hlm = 85``

   .. caution:: Is this right?

**Reference stage**
   The reference stage is calibrated such that the beam passes through
   the center of a slot every 45 mm.  Thus the five positions, from
   top to bottom, are -90, -45, 0, 45, and 90.  Move to a new
   positions by::

     RE(mv(xafs_linxs, -45))

   As part of a macro that changes energies, you might do something
   like::

     yield from mv(dcm.energy, 11564) # the Pt K edge energy
     yield from mv(xafs_linxs, 45)    # the position of the Pt foil in the foil holder

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

Table motors
------------

Typically, table motors are not moved individually.  When changing
:numref:`photon delivery system modes (Section %s) <change-mode>`, the
table should be put into the correct orientation such that the beam
passes through the center of the ion chambers.

The lateral table motors are normally disabled.


.. table:: XAFS table motors
   :name:  xafs-table

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
