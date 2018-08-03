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

      output example for
      the dcm.wh() command


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

   Note that the BlueSky command line is able to do simple
   arithmetic (and a whole lot more!).  It is a good idea to leave the
   arithmetic to the computer.

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
the focusing mirror ``m2.wh()``


.. code-block:: text

   output example for
   the m2.wh() command

and on the harmonic rejection mirror ``m3.wh()``

.. code-block:: text

   output example for
   the m3.wh() command




