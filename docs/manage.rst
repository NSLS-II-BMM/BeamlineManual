..
   This document was developed primarily by a NIST employee. Pursuant
   to title 17 United States Code Section 105, works of NIST employees
   are not subject to copyright protection in the United States. Thus
   this repository may not be licensed under the same terms as Bluesky
   itself.

   See the LICENSE file for details.

.. _manage:

Managing the beamline
=====================


In this section, some recipes are provided for managing the beamline
and meeting the needs and expectations of different experiments.

As a reminder, here is the table of operating modes.

.. _pds_modes:
.. table:: Photon delivery modes
   :name:  pds-modes2
   :align: left

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

Changing energy is simple.  Usually, it is as simple as doing

.. code-block:: python
		
   RE(change_edge('Fe'))

replacing the two-letter element symbol with the element you actually
want to measure. This command will move the monochromator, put the
photon delivery system in the correct mode, move the M2 bender to
approximately the correct setting, run a rocking curve scan,
optimize the slit height, move the reference foil holder to the
correct position (if configured), and select the correct ROI channel
(if configured).


If you want to reproduce this by hand, here is the command sequence:


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

#. If using focused beam, make sure that the mirror bender is in the
   correct position.  For focusing at the XAS table, ``m2_bender``
   should be at about 212000 counts.  For focusing at the position of
   the goniometer, ``m2_bender`` should be about 112000 counts.

   .. code-block:: python

      RE(mv(m2_bender, 212000))

#. Next, verify that the :numref:`height of the hutch slits (Sec %s)
   <special-linescans>` is optimized for the beam height.  In
   principle, this should be correct after changing photon delivery
   system mode.  But it doesn't hurt to verify.

   .. code-block:: python

      RE(slit_height())

   At the end of the scan, you will need to pluck the correct position
   from the plot.

#. Next, if you are using a reference foil, you should move the
   reference foil holder to the slot containing the correct foil.  The
   command is something like:

   .. code-block:: python

      RE(reference('Fe'))

   choosing the correct element for your measurement.

#. Finally,  select the correct ROI channel:

   .. code-block:: python

      BMMuser.verify_roi(xs, 'Fe', 'K')


..
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
pitch of the second crystal.  It will then move the DCM to the energy
that you started at with the other crystal set and run a rocking curve
scan.

Note that some of these motions can be a bit surprising in the sense
that the monochromator will end up outside the normal operating range
of the beamline.  They will, however, eventually return to sensible
places.


Change XAS |harr| XRD
---------------------

Begin this transition by leaving the I0 chamber in place to monitor
the incidence flux.  In most cases, this should do the trick:

.. code-block:: python

   RE(change_edge('Ni', xrd=True, energy=8600))

The element symbol in the first argument is not actually used in any
way when ``xrd=True`` is used, however the funtion requires
`something` as its first argument.  Setting ``xrd=True`` forces the
``focus=True`` and ``target=0`` arguments to the ``change_edge()``
command to be set.  This will move to the specified energy, place the
photon delivery mode in `XRD` mode, optimize the second
crystal and the slit height, and move to an approximately M2 bender
position. 

To do all of that by hand, you would do the follow commands:

.. code-block:: python

   RE(change_mode('XRD'))
   RE(mv(dcm.energy, 8600))
   RE(rocking_curve())
   RE(slit_height())

This change of mode should have the beam in good focus at the position
of the goniometer.  8000 eV is the nominal operating energy for the
goniometer.  If a higher energy is required, substitute the correct
energy for ``8600`` in the second line.

.. todo:: Determine look-up table for lower energy operations using
	  both M2 and M3.  This will require a new XAFS table and
	  adjustments to the limit switches on ``m3_ydo`` and
	  ``m3_ydi``.

Once the photon delivery system is set, remove the ion chambers and
insert the XRD flight path into its place.


.. _use333:

XAFS with Si(333)
-----------------

Using the Si(111) monochromator, it is possible to use the third
harmonic |nd| the Si(333) reflection |nd| to measure XAS with slightly
higher energy resolution.  In this section, we explain how to set up
the beamline to measure the Ge K edge at 11103 eV using the Si(333).

You cannot use the ``change_edge()`` command to do this.  Use of the
Si(111) (or Si(311)) is hard-wired into that plan.  You have to set up
the beamline by hand.

First, put the photon delivery system in mode D (or mode A if using
the focusing mirror):

.. code-block:: python

   RE(change_mode('D'))

Next, move the monochromator to a few 10s of eV above the absorption
edge, as measured with the third harmonic.  The Ge K edge is at 11103
eV, so we need to move the monochromator to 11103/3 = 3701 eV.

.. code-block:: python

   RE(mv(dcm.energy, (11103+27)/3))

or simply

.. code-block:: python

   RE(mv(dcm.energy, 3701+9))

This will put the third harmonic energy 27 eV above the Ge K edge.

Now, run a rocking curve scan:

.. code-block:: python

   RE(rocking_curve())

This will produce a plot that looks something like this:

.. _fig-rocking333:
.. figure::  _images/rocking_curve_333_E=3716.png
   :target: _images/rocking_curve_333_E=3716.png
   :width: 70%
   :align: center

   A rocking curve scan with the photon delivery system in mode D and
   the mono at 3716 eV.

The broad base of this curve is the Si(111) rocking curve with photons
at 3710 eV. The sharp spike in the middle is the Si(333) rocking curve
with photons at 11130 eV.

Optimize the slit_height:

.. code-block:: python

   RE(slit_height())

You are ready to measure XAS with the Si(333) reflection!

Here's an example ``scan.ini`` file for XANES of elemental Ge:  

.. code-block:: ini

   [scan]
   experimenters = Bruce Ravel

   filename      = Ge
   sample        = elemental Ge, crystalline
   prep          = standard sample
   comment       = measured with Si(333) reflection, 25um Al foil in beam path before I0

   ththth        = True
   e0            = 11103
   element       = Ge
   edge          = K

   nscans        = 1
   start         = next

   ## mode is one of transmission, fluorescence, both, or reference
   mode       = transmission

   ## Ge Si(333)
   bounds     = -45    -18     -9      36    150
   steps      =      9     0.9     0.3    0.9
   times      =      0.5    0.5    0.5    0.5
 

Several things to note:

#. Note that the actual value for E0 is specified, not the divided-by-3 value.  
#. Actual energy bounds and steps are specified, the xafs scan plan
   will convert them to appropriately sized steps for the Si(111).
#. By setting the 333 flag to True, the correct thing will happen,
   including writing the correct energy axis to the output data file.
#. The on-screen plot will show the fundamental |nd| Si(111) |nd| energy, however.  
#. Also, you still need to set up the photon delivery system up by hand.


Examine Motor Axes
------------------

Some BlueSky functionality related to the axes controlled by the FMBO
MCS8 motor controllers.  These include:

+ Collimating mirror (``m1_*``)
+ Filter assemblies (``dm1_*``)
+ Monochromator (``dcm_*``)
+ Second diagnostic module (``dm2_*``)
+ Focusing mirror (``m2_*``)
+ Harmonic rejection mirror (``m3_*``)
+ Third diagnostic module (``dm3_*``)

(38 axes motors in total) but not any of the end station motors
(``xafs_*``), which are run using NSLS-II standard GeoBricks.

**Homing**
  Any of these axes can be homed with, for example, ``dm3_bct.home()``

**Summarize the status of a motor**
  To show the values of all the status flags, for example, ``dm3_bct.status()``

**Which motors have been homed?**
  Do this command: ``homed()``

**Which motors have their amplifiers enabled?**
  Do this command: ``ampen()``


Calibrate the mono
------------------

The typical calibration procedure involves measuring the angular
position of the Bragg axis for the edge energies of 10 metals: Fe, Co,
Ni, Cu, Zn, Pt, Au, Pb, Nb, and Mo.  

#. Be sure that all 10 of these elements are actually mounted on the
   reference wheel and configured in the ``xafs_ref.mapping`` dict.
   (They should be.  It would be very unusual for any of these foils
   to have been removed from the reference wheel.)

#. Run the command 

   .. code-block:: python

      RE(calibrate(mono='111'))

   Use the ``mono='311'`` argument for the Si(311) monochromator.
   This will, in sequence, move to each edge and measure a XANES scan
   over a wide enough range that it should cover the edge (unless the
   mono is currently calibrated VERY wrongly).  This will write a file
   called :file:`edges111.ini` (or :file:`edges3111.ini`).  Each XANES
   scan uses the file
   :file:`/home/xf06bm/Data/Staff/mono_calibration/cal.ini` as the INI
   file.  Edge appropriate command line parameters will be added by
   the ``calibrate()`` plan.

#. Examine the data in Athena. Make sure E\ :sub:`0` is selected
   correctly for all 10 edges. Copy those values into the first column
   of :file:`edges111.ini` (or :file:`edges311.ini`). 

   .. attention::

      It is no longer necessary to compute the angular positions of
      the monochromator.  Those will be computed from the edge energy
      values you edited into the INI file by hand.

   .. 
     Compute the
     angular positions using
     .. code-block:: python
	dcm.e2a(<energy values>)
     and copy those numbers into the :file:`edgeH11.ini` file.

#. Run the command

   .. code-block:: python

      calibrate_mono(mono='111')

   (or use the ``'311'`` argument).  This will show the fitting
   results and plot the best fit.  It will also print in a text box
   instructions for modifying the :file:`BMM/dcm-parameters.py` file
   to use the new calibration values.

#. Edit :file:`BMM/dcm-parameters.py` as indicated.

#. Do

   .. code-block:: python

      %run -i 'home/xf06bm/.ipython/profile_collection/startup/BMM/dcm-parameters.py'

   then do

   .. code-block:: python

      dcm.set_crystal()

   Or simply restart bsui, which is usually the easiest thing.

#. Finally, do 


   .. code-block:: python

      calibrate_pitch(mono='111')

   and use the fitted slope and offset to modify ``approximate_pitch``
   in :file:`BMM/functions.py`.

The mono should now be correctly calibrated using the new calibration
parameters.
