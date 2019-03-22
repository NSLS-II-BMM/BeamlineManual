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

Changing energy is usually simple enough that the user can do so
without help.  Here's the recipe:

#. First move the DCM to the new energy position.  It is usually a
   good idea to move a bit above the target edge energy.  Here's an
   example for moving 50 eV above the iron K edge energy:

   .. code-block:: python

      RE(mv(dcm.energy, 7112+50))

#. Put the beamline in the correct photon delivery system mode.  (See
   the table just above.)  Continuing with the example of the iron K
   edge, for unfocused beam:

   .. code-block:: python

      RE(change_mode('E'))

   If the new edge energy is in the same energy range according to the
   table above, you can skip this step.  For example, Mn and Fe are
   both in mode E (or mode C).  The ``change_mode()`` command does not
   need to be run to move between those edges.

#. Measure a :numref:`rocking curve scan (Sec %s) <special-linescans>`
   to verify that the second crystal of the rocking curve is parallel
   to the first crystal.  This is more important for large energy
   changes.  You may find that you can skip this step if you are
   changing between nearby edges.

   .. code-block:: python

      RE(rocking_curve())

   At the end of the scan, the mono pitch will be moved to the top of
   the rocking curve.

#. Next, verify that the :numref:`height of the hutch slits (Sec %s)
   <special-linescans>` is optimized for the beam height.  In
   principle, this should be correct after changing photon delivery
   system mode.  But it doesn't hurt to verify.

   .. code-block:: python

      RE(slit_height())

   At the end of the scan, you will need to pluck the correct position
   from the plot.

#. Finally, if you are using a reference foil, you should move the
   reference foil holder to the slot containing the correct foil.  The
   command is something like:

   .. code-block:: python

      RE(mv(xafs_ref, 45))

   The positions on the reference foil holder are 45 mm apart.  The
   top-most slot is at an ``xafs_ref`` position of -90, the
   bottom-most at +90.


.. todo::
   Better automation.  Something like ``RE(change_edge('Fe'))``, which
   changes energy, moves to the correct photon delivery mode, runs a
   rocking curve, and sets the reference foil.


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
