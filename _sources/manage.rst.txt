..
   This manual is copyright 2018 Bruce Ravel and released under
   The Creative Commons Attribution-ShareAlike License
   http://creativecommons.org/licenses/by-sa/3.0/

.. _manage:

Managing the beamline
=====================


In this section, some recipes are provided for managing the beamline
and meeting the needs and expectations of different experiments.

As a reminder, here is the table of operating modes.

.. table:: Photon delivery modes
   :name:  pds-modes2

   ====== ============ ========================= 
   Mode   focused      energy range
   ====== ============ ========================= 
   A      |checkmark|  above 8 keV
   B      |checkmark|  below 6 keV
   C      |checkmark|  6 keV |nd| 8 keV
   D      |xmark|      above 8 keV
   E      |xmark|      6 keV |nd| 8 keV
   F      |xmark|      below 6 keV
   XRD    |checkmark|  above 8 keV
   ====== ============ ========================= 


Change energy
-------------

Suppose that you want to move the monochromator from 8 keV to 15 keV.
This is a fairly low-overhead change to beamline configuration as both
energies are suitable for modes A or D.

This is a three-step process.  First move the DCM to the new energy
position, then run a rocking curve scan to tune up the second crystal,
finally verify the slit height.

.. code-block:: python

   RE(mv(dcm.energy, 15000))
   RE(rocking_curve())
   RE(slit_height())

A comment about this: Currently there are small errors both in the
mode look-up table and in the configuration of the mono.  In
principle, there should be no change in beam height when changing
energy.  In practice, the beam position changes a bit, so it is
prudent to verify the slit height.


Change mode
-----------

Suppose that you want to change from high-energy, unfocused operations
to low energy, focused.  That is, you are changing from mode D to mode
B, for example moving from a large sample at the yttrium K edge to a
small sample at the vanadium K edge.

.. code-block:: python

   RE(change_mode('B'))
   RE(mv(dcm.energy, 5465+50))
   RE(rocking_curve())
   RE(slit_height())

.. todo:: We are still working on optimizing the mode look-up table.
	  At this time, some additional adjustments of the mirrors
	  will be required to optimize focus at the XAS position.

#. If the beam has recently been focused at the XRD station, you will
   also need to adjust the bender on M2 to optimize vertical focus at
   the XAS station (or vice versa).  This is best done with the small
   CCD camera sitting in the XAS sample stage.

#. Again, iterating the optimization of the rocking curve and slit
   height might be necessary.

Change crystals
---------------

Suppose you wanted to change from the Pt L3 edge (11564 eV) on the
Si(111) crystal to the same energy on the Si(311) crystal.

.. code-block:: python

   RE(change_xtal('311'))

This will move the lateral motor of the DCM and optimize the roll and
pitch of the second crystal.  It will leave the DCM at 22143.4 eV, so
move back to the correct energy and rerun the rocking curve scan.

.. code-block:: python

   RE(mv(dcm.energy, 11564))
   RE(rocking_curve())

Note that some of these motions can be a bit surprising in the sense
that the monochromator will end up outside the normal operating range
of the beamline.

For example, starting much higher in energy on the Si(111)
monochromator will leave the beamline above the energy cut-off imposed
by the collimating mirror.  In that case, the signal will be quite
feeble and the rocking curve scan that is part of the
``change_xtal()`` command might be hard to interpret.

Another example: changing from a rather low energy on the Si(311)
crystal might leave the mono well below 5000 eV.  In that case the
fundemnatal will be significantly attenuated by the Be windows and by
the air, while the harmonics may not be well removed by the flat
mirror.  Again, the rocking curve scan will be hard to interpret in
that case.

In both examples, move the monochromator back to the desired energy
before exploring the rocking curve.




Change XAS |harr| XRD
---------------------

Begin this transition by leaving the I0 chamber in place to monitor
the incidence flux.  Do:

.. code-block:: python

   RE(change_mode('XRD'))
   RE(mv(dcm.energy, 8000))
   RE(rocking_curve())
   RE(slit_height())

This change of mode should have the beam in good focus at the position
of the goniometer.  8000 eV is the nominal operating energy for the
goniometer.  If a higher energy is required, substitute the correct
energy for ``8000`` in the second line.

.. todo:: Determine look-up table for lower energy operations using
	  both M2 and M3.

Once the photon delivery system is set, remove the ion chambers and
insert the XRD flight path into its place.
