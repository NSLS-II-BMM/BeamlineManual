..
   This manual is copyright 2018 Bruce Ravel and released under
   The Creative Commons Attribution-ShareAlike License
   http://creativecommons.org/licenses/by-sa/3.0/

.. _pds:

Photon Delivery System
======================

Shutters
--------

**Open and close the photon shutter**
   In the nomenclature of BMM, the photon shutter is ``shb``.  Open
   and close this shutter with::

     shb.open()
     shb.close()

   If you wish to open or close the photon shutter in a :numref:`macro
   (Section %s) <macro>`, do::

     yield from shb.open_plan()
     yield from shb.close_plan()

**Open and close the safety shutter**
   This is the front-end shutter.  Closing it takes light off the
   monochromator, which is not something you typically want to do
   during an experiment.  That said, the safety shutter is ``sha`` in
   the BMM nomenclature::

     sha.open()
     sha.close()

Monochromator
-------------

The monochromator consists of 8 motors.  It should never be necessary
to interact directly with any of the motors.  Plans exist for
facilitating any actions a user should ever need.

**Query the current energy**

   ::

     dcm.wh()

   This returns a short report like this:

   .. code-block:: text

      Energy = 19300.1   reflection = Si(111)
      current: Bragg =  5.87946   2nd Xtal Perp = 15.0792   2nd Xtal Para = 146.4328


   This report shows the current energy, the crystal set currently in
   use, and the position of the parallel and perpendicular motors of
   the second crystal carriage.

**Move to a new energy**
   The ``dcm.energy`` virtual motor coordinates the Bragg, parallel,
   and perpendicular motors to maintain a fixed exit height and set
   the energy of the mono.  To move to the copper K edge energy::

      RE(mv(dcm.energy, 8979))

   To move 50 eV above the copper K edge energy::

      RE(mv(dcm.energy, 8979+50))

   Note that the BlueSky command line is able to do simple arithmetic
   (and a whole lot more!).  It is a good idea to leave the arithmetic
   to the computer.

**Move to a new energy in a macro**
   An energy change can be a part of a :numref:`macro (Section %s)
   <macro>`.  Simply do::

     yield from mv(dcm.energy, 8979+50))

**Tune the second crystal of the mono**
   After a long move, you might need to retune the second crystal.  To
   find the peak of the rocking curve and move to that peak::

     RE(rocking_curve())

   This will run a scan of the pitch of the second crystal.  At the
   end of the scan, it moves to the ceiling of the measured intensity
   profile.

   You can tune the second crystal by hand with these commands::

     tu()
     td()

   Those stand for :quoted:`tune up` and :quoted:`tune down`.  Do not
   think that :quoted:`up` and :quoted:`down` refer to measured
   intensity.  Rather, they refer to the direction of motion of the
   motor which adjusts the second crystal pitch.  When you move to
   higher energy, you usually need to tune in ``td()`` direction.
   When you move to a lower energy, you usually need to tune in the
   ``tu()`` direction.  Obviously.....

Mirrors
-------

Mirrors are set as part of the mode changing plan.  Unless you know
exactly what you are doing, you should never move the mirrors.
Adjusting mirrors by hand is a poor idea.  Changing the mirror
positions in any way changes the height and inclination of the beam as
it enters the end station.  This requires changes in positions of the
slits, the XAFS table, and other parts of the photon delivery system.

`In short, don't move the mirror motors.`

That said, if you want to know the current positions of the motors on
the focusing mirror, use ``m2.wh()``


.. code-block:: text

   In [1903]: m2.wh()
   M2:
        vertical =   6.000 mm           YU  =   6.000
        lateral  =   0.000 mm           YDO =   6.000
        pitch    =   0.000 mrad         YDI =   6.000
        roll     =  -0.001 mrad         XU  =  -0.129
        yaw      =   0.200 mrad         XD  =   0.129
        bender   =  163789.0 steps

For the harmonic rejection mirror, use ``m3.wh()``

.. code-block:: text

   In [1904]: m3.wh()
   M3: (Rh/Pt stripe)
        vertical =   0.000 mm           YU  =  -1.167
        lateral  =  15.001 mm           YDO =   1.167
        pitch    =   3.500 mrad         YDI =   1.167
        roll     =   0.000 mrad         XU  =  15.001
        yaw      =   0.001 mrad         XD  =  15.001


End station slits
-----------------

Near the end of the photon delivery system, in Diagnostic Module 3 in
the end station, there is a four-blade slits system.  These are used
to define the beam size on the sample.

The individual blades are moved like any other motor::

  RE(mv(slits3.outboard, -0.5))
  RE(mvr(slits3.top, -0.1))

The slits are called ``slits3.top``, ``slits3.bottom``,
``slits3.inboard``, and ``slits3.outboard``.

Coordinated motions of the slits are also possible::

  RE(mv(slits3.hsize, 6))
  RE(mv(slits3.hcenter, 0.25))
  RE(mv(slits3.vsize, 0.5))
  RE(mv(slits3.vcenter, -0.1))

Those commands move pairs of motors to adjust the size and center in
the horizontal and vertical directions.

To know the current positions of the slit blades and their coordinated
motions, use ``slits3.wh()``

.. code-block:: text

   In [1904]: slits3.wh()
