..
   This manual is copyright 2018 Bruce Ravel and released under
   The Creative Commons Attribution-ShareAlike License
   http://creativecommons.org/licenses/by-sa/3.0/

.. _pds:

Photon Delivery System
======================

Configure the Photon Delivery System
------------------------------------

Configuring the photon delivery system for a specific measurement is
usually quite simple.  When moving to a new absorption edge, do the
following:

.. code-block:: python

   RE(change_edge('Fe'))

substituting the two-letter symbol for the element you want to
measure.  This will:

* move the monochromator :numref:`(Section %s) <dcm>`
* put the photon delivery system in the correct mode :numref:`(Section
  %s) <change-mode>`
* measure the rocking curve of the monochromator :numref:`(Section %s)
  <special-linescans>`
* optimize the height of the hutch slits :numref:`(Section %s)
  <special-linescans>`
* move the reference foil holder to the correct position
  :numref:`(Section %s) <sample_stages>`
* set the active Xspress3 ROI to the correct emission line

This whole process takes less than 5 minutes. After that, the beamline
is ready to collect data.

If using the focusing mirror, do this:

.. code-block:: python

   RE(change_edge('Fe', focus=True))

Excluding the ``focus`` argument |nd| or setting it to False |nd|
indicates setup for unfocused beam.

This edge change can be put into a :numref:`macro (see Section %s)
<macro>` like so:

.. code-block:: python
   
   yield from change_edge('Fe')

or

.. code-block:: python
   
   yield from change_edge('Fe', focus=True)

In this way, a macro can manage energy changes while you sleep!

.. _foilholder:

Automating reference foil changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A wheel is used to hold and switch between reference foils.  The
standard reference wheel has the 20 most commonly measured elements,
plus four empty slots where additional references can be mounted.

To select, for example, the iron reference foil:

.. code-block:: python

   RE(reference('Fe'))

In a plan:

.. code-block:: python

   yield from reference('Fe')

The argument is simply the one- or two-element symbol for the target
element.

The ``change_edge()`` command does this automatically, so long as the
target edge is available on the reference holder.

The foil holder is configured as a python list:

.. code-block:: python

   #                    1     2     3     4     5     6     7     8     9     10    11    12
   xafs_ref.content = [None, 'Ti', 'V',  'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge',
                       'As', 'Se', 'Br', 'Zr', 'Nb', 'Mo', 'Pt', 'Au', 'Pb', None, None, None]
   #                    13    14    15    16    17    18    19    20    21    22    23    24


Adding a new element to this list is simple.  Suppose we affix a
sample of Dy\ :sub:`2`\ O\ :sub:`3` to slot 22 (right after the Pb
foil) as a reference for Dy.  This placement can be configured by

.. code-block:: python

   xafs_ref.content[21] = 'Dy'

Note that python lists count from 0, hence the 22\ :sup:`nd` slot is
index 21 in the list.

To see the available foils, do ``%se``

BMM has stable oxide references for all lanthanides except Pm as well
as metal or oxide references for most other elements within the
measurement range of the beamline that are not normally mounted on the
reference wheel.

`Here is a complete list of standards
<https://nsls-ii-bmm.github.io/bmm-standards/BMM-standards.html>`__ in
BMM's collection.


.. _roichannels:

..
  Automating fluorescence ROI changes
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  To make sure that the correct ROI channel is selected, you need to
  configure the ROI readout.  Suppose that you have configured the
  analog detector readout system to measure three of those transition
  metals.  Then you would execute a command like this to configure the
  detector readout:

  .. code-block:: python

     rois.set('Fe Co Ni')

  Unfortunately, the ROI channels and reference holder have the hot
  dog/hot dog bun problem.  There are only three output channels for the
  analog detector readout system, thus only three elements can be
  configured at a time.

  When you change edge to an element that is configured as an ROI
  channel, the data acquisition system will take its fluorescence data
  from the corresponding channels of the Struck multichannel scalar.  It
  will also perform the dead-time correction using the correct signal
  chains for the selected element. 

Parameters for the change_edge() command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The full set of parameters for the ``change_edge()`` plan are:

.. code-block:: python

   RE(change_edge(element, focus=False, edge='K', energy=None, slits=True, calibrating=False, target=300.))

where,

``element``
  The one- or two-letter element symbol or Z number.

``focus``
  ``True``: set up for using the focusing mirror, modes A, B, C;
  ``False``: unfocused beam, modes D, E, F.  Default is ``False``.

``edge``
  If not specified, use K or L3, as appropriate for the energy range
  of the beamline.  Use this argument to specify an L1, L2, or M edge.

``energy``
  Use an E0 value that is not obtained from the look-up table.
  Default is unspecified, i.e. use ``element`` and look-up table.

``slits``
  ``True``: optimize slit height; ``False``: skip ``slit_hight()``
  scan.  Default is ``True``.

``calibrating``
  ``True``: used when performing beamline maintenance.  Default is ``False``

``target``
  The energy above e0 at which to perform the rocking curve scan.
  Default is 300.


Most of those parameters are rrarely used, except for ``edge``.  If
you need to set up for measuring an L\ :sub:`2` or L\ :sub:`1` edge, you
must specify it.


For all the details about the individual parts of the photon delivery
system, read on!


Shutters
--------

**Open and close the photon shutter**
   In the nomenclature of BMM, the photon shutter is ``shb``.  Open
   and close this shutter with::

     shb.open()
     shb.close()

   These plans are somewhat more elaborate than simply toggling the
   state of the shutters.  It happens from time to time that the
   shutter does not trigger when told to open or close.  So, these
   plans try up to three times to open or close the photon shutter,
   with a 1.5 second pause between attempts.

   If you wish to open or close the photon shutter (using the same
   multiple attempt algorithm) in a :numref:`macro (Section %s)
   <macro>`, do::

     yield from shb.open_plan()
     yield from shb.close_plan()

**Open and close the safety shutter**
   This is the front-end shutter.  Closing it takes light off the
   monochromator, which is not something you typically want to do
   during an experiment.  That said, the safety shutter is ``sha`` in
   the BMM nomenclature::

     sha.open()
     sha.close()

.. _dcm:

Monochromator
-------------

The monochromator consists of 8 motors.  It should never be necessary
to interact directly with any of the physical motors.  Plans exist for
facilitating any actions a user should ever need.

**Query the current energy**
   To know the position and energy of the monochromator: ``%w dcm``

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
   end of the scan, it moves to the center of mass of the measured
   intensity profile.

   You can do the rocking curve scan by looking at the signal on the
   Bicron which is used as the incident beam monitor for the XRD end
   station.  Do::

     RE(rocking_curve(detector='Bicron'))

   You can tune the second crystal by hand with these commands::

     tu()
     td()

   Those stand for "tune up" and "tune down".  Do not
   think that "up" and "down" refer to measured
   intensity.  Rather, they refer to the direction of motion of the
   motor which adjusts the second crystal pitch.  When you move to
   higher energy, you usually need to tune in ``td()`` direction.
   When you move to a lower energy, you usually need to tune in the
   ``tu()`` direction.  Obviously.....

**Fixed-exit and pseudo-channelcut modes**
   The mono can be run in either fixed-exit or pseudo-channelcut
   modes. 

   Fixed exit means that the second monochromator crystal will be
   moved in directions parallel and perpendicular to its diffracting
   surface in order to maintain a fixed exit height of the beam coming
   from the second crystal.  Without fixed-exit mode, it would not be
   possible to change the energy over the entire energy range of the
   beamline.  The aperture after the monochromator is only a few
   millimeters tall.  The vertical displacement of the beam over a
   lerge energy change would be sufficient to move the beam out of the
   aperture. 

   However, the stability of the monochromator suffers with respect to
   EXAFS data quality when measuring an energy scan in fixed-exit
   mode.  We find it is better to disable the parallel and
   perpendicular motions when measuring XAFS, suffering a small
   vertical displacement of the beam.

   The mono mode is controlled by a parameter:

   .. code-block:: python

      dcm.mode = 'fixed'

   or 

   .. code-block:: python

      dcm.mode = 'channelcut'

   In practice, the monochromator is normally left in fixed-exit
   mode.  That way, the monochromator can be moved without worry about
   the beam height and the monochromator exit aperture.  In the 
   :numref:`XAFS scan plan (Section %s) <xafsscan>`, the monochromator
   first moves |nd| in fixed-exit mode |nd| to the center of the
   angular range of the scan, then sets ``dcm.mode`` to
   ``channelcut``. Once the sequence of scan repititions is finished,
   the monochromator is moved back to the center of the angular range
   and the monochromator is returned to fixed-exit mode.


Post-mono slits
---------------

After the mono, before the focusing mirror, in Diagnostic Module 2,
there is a four-blade slit system.  These are used to define the beam
size on the mirrors and to refine energy resolution for the focused
beam..


.. table:: Post mono slit motors
   :name:  slits2-motors
   :align: left

   ===============   ========  =======================  ===================
   motor             units     notes                    motion type
   ===============   ========  =======================  ===================
   slits2_top        mm        top blade position       single axis
   slits2_bottom     mm        bottom blade position    single axis
   slits2_inboard    mm        inboard blade position   single axis
   slits2_outboard   mm        outboard blade position  single axis
   slits2_hsize      mm        horizontal size          coordinated motion
   slits2_hcenter    mm        horizontal center        coordinated motion
   slits2_vsize      mm        vertical size            coordinated motion
   slits2_vcenter    mm        vertical center          coordinated motion
   ===============   ========  =======================  ===================


The individual blades are moved like any other motor::

  RE(mv(slits2.outboard, -0.5))
  RE(mvr(slits2.top, -0.1))


Coordinated motions are moved the same way::

  RE(mv(slits2.hsize, 6))
  RE(mvr(slits2.vcenter, -0.1))

To know the current positions of the slit blades and their coordinated
motions, use ``%w slits2``

.. code-block:: text

   In [1966]: %w slits2
   SLITS2:
        vertical   size   =   1.350 mm          Top      =   0.675
        vertical   center =   0.000 mm          Bottom   =  -0.675
        horizontal size   =   8.000 mm          Outboard =   4.000
        horizontal center =   0.000 mm          Inboard  =  -4.000

Mirrors
-------

Mirrors are set as part of the mode changing plan.  Unless you know
exactly what you are doing, you probably don't want to move the
mirrors outside of the ``change_mode()`` command.  (Adjusting M1 by
hand is a horrible idea -- unless you know exactly what you are doing
and why.)  Changing the mirror positions in any way changes the height
and inclination of the beam as it enters the end station.  This
requires changes in positions of the slits, the XAFS table, and other
parts of the photon delivery system.

Outside of the use of the ``change_mode()`` command, it should not be
necessary for users to move the mirror motors.  It is **very easy** to
lose the beam entirely when moving mirror motors.  Without a clear
understanding of how the optics work, re-finding the beam can be quite
challenging.  If you loose the beam by moving motors, the best
solution is probably to rerun the ``change_mode()`` command.

That said, if you want to know the current positions of the motors on
the focusing mirror, use ``%w m2``


.. code-block:: text

   In [1903]: %w m2
   M2:
        vertical =   6.000 mm           YU  =   6.000
        lateral  =   0.000 mm           YDO =   6.000
        pitch    =   0.000 mrad         YDI =   6.000
        roll     =  -0.001 mrad         XU  =  -0.129
        yaw      =   0.200 mrad         XD  =   0.129
        bender   =  163789.0 steps

For the harmonic rejection mirror, use ``%w m3``

.. code-block:: text

   In [1904]: %w m3
   M3: (Rh/Pt stripe)
        vertical =   0.000 mm           YU  =  -1.167
        lateral  =  15.001 mm           YDO =   1.167
        pitch    =   3.500 mrad         YDI =   1.167
        roll     =   0.000 mrad         XU  =  15.001
        yaw      =   0.001 mrad         XD  =  15.001

.. _slits3:

End station slits
-----------------

Near the end of the photon delivery system, in Diagnostic Module 3 in
the end station, there is a four-blade slit system.  These are used
to define the beam size on the sample.


.. table:: End station slit motors
   :name:  slits3-motors
   :align: left

   ===============   ========  =======================  ===================
   motor             units     notes                    motion type
   ===============   ========  =======================  ===================
   slits3_top        mm        top blade position       single axis
   slits3_bottom     mm        bottom blade position    single axis
   slits3_inboard    mm        inboard blade position   single axis
   slits3_outboard   mm        outboard blade position  single axis
   slits3_hsize      mm        horizontal size          coordinated motion
   slits3_hcenter    mm        horizontal center        coordinated motion
   slits3_vsize      mm        vertical size            coordinated motion
   slits3_vcenter    mm        vertical center          coordinated motion
   ===============   ========  =======================  ===================


The individual blades are moved like any other motor::

  RE(mv(slits3.outboard, -0.5))
  RE(mvr(slits3.top, -0.1))


Coordinated motions are moved the same way::

  RE(mv(slits3.hsize, 6))
  RE(mvr(slits3.vcenter, -0.1))

To know the current positions of the slit blades and their coordinated
motions, use ``%w slits3``

.. code-block:: text

   In [1966]: %w slits3
   SLITS3:
        vertical   size   =   1.350 mm          Top      =   0.675
        vertical   center =   0.000 mm          Bottom   =  -0.675
        horizontal size   =   8.000 mm          Outboard =   4.000
        horizontal center =   0.000 mm          Inboard  =  -4.000

Configurations
--------------

.. _change-mode:

Photon delivery modes
~~~~~~~~~~~~~~~~~~~~~

A look-up table is used to move the elements of the photon delivery
system to their correct locations for the different energy ranges and
focusing conditions.  Here is a table of different photon delivery
modes.  Modes A-F are for delivery of light to the XAS end station.
Mode XRD delivers high energy, focused beam to the goniometer.


.. table:: Photon delivery modes
   :name:  pds-modes
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

.. todo:: Lookup table not complete for mode B. In fact, the ydo and
   ydi jacks of M3 cannot move low enough to enter mode B.  In
   practice, mode B is not available.


To move between modes, do::

  RE(change_mode('<mode>'))

where ``<mode>`` is one of the strings in the first column of
:numref:`Table %s <pds-modes>`.  For example::

  RE(change_modes('D'))

This will move 17 motors all at the same time and should take less
than 2 minutes.

Note that the bender on the focusing mirror is not adjusted by the
``change_mode()`` plan.  You will likely need to adjust the curvature
|nd| thus the focal length |nd| by hand.  Focusing at the XAS end
station requires that bender be near its upper limit.  Focusing at the
XRD station uses much less focus.

.. _change-crystals:

Monochromator crystals
~~~~~~~~~~~~~~~~~~~~~~

To change between the Si(111) and Si(311) crystals, do::

  RE(change_crystals('111'))

or::

  RE(change_crystals('311'))

This will move the lateral motor of the monochromator between the two
crystal sets and adjust the pitch of the second crystal to be nearly
in tune and the roll to deliver the beam to nearly the same location
for both crystals.  This also is quick and should take less than 3
minutes.

The ``change_xtals()`` plan also runs the :numref:`rocking curve
(Section %s) <special-linescans>` macro to fix the tuning of the
second crystal.

