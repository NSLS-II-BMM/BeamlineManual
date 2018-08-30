..
   This manual is copyright 2018 Bruce Ravel and released under
   The Creative Commons Attribution-ShareAlike License
   http://creativecommons.org/licenses/by-sa/3.0/


.. _intro:

Introduction to BMM
===================

At the unix command line, type ``bsui`` to start the BlueSky user
interface.  bsui is simply an `Ipython shell <https://ipython.org/>`_
with some customizations specific to BlueSky.  On top of that, there
are a number of customizations specific to BMM.

There are some commands that give a broad overview of the state of the
beamline.  To see the locations of the motors that matter most to most
experiments, do::

  ms()

This will print the following report to the screen:

.. code-block:: text

   In [1897]: ms()
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


To get an overview of the status of the beamline utilities |nd|
i.e. things like temperatures and gate vale states |nd| do::

  su()

This will print this report to the screen:

.. code-block:: text

   In [1898]: su()
   Monday 06 August, 2018 10:24 AM

   BMPS: open            IDPS: closed            Photon Shutter: closed

   Thermocouple               Temperature         Valve   state          Vacuum section       pressure     current
   =======================================================================================================================
     Mirror 1, inboard fin            33.5 C        FEGV1   open          Diagnostic Module 1   8.60E-09     20.0 μA
     Mirror 1, disaster mask          32.4 C        FEGV3   open          Monochromator         5.00E-08    320.0 μA
     Mirror 1, outboard fin           33.2 C        FEGV2   open          Diagnostic Module 2   3.60E-09     86.0 μA
     First fluorescent screen         29.0 C        GV1     open          Focusing Mirror       3.10E-09     15.0 μA
     111 first crystal                28.7 C        GV2     open          Harmonic Rej. Mirror  2.20E-09      8.9 μA
     311 first crystal                29.4 C        GV3     open          Transport Pipe        2.10E-09      2.7 μA
     Compton shield                   29.2 C        GV4     open          Diagnostic Module 3   2.70E-09      7.4 μA
     Second crystal pitch             27.9 C        GV5     open          Flight Path           7.20E+02
     Second crystal roll              27.9 C        GV6     open
     Second crystal perpendicular     27.6 C
     Second crystal parallel          25.5 C
     Mirror 2 upstream                26.4 C
     Mirror 2 downstream              25.9 C
     Mirror 3 upstream                26.0 C
     Mirror 3 downstream              25.5 C
     Filter assembly 1, slot 1        28.8 C
     Filter assembly 1, slot 2        28.6 C
     Filter assembly 1, slot 3        28.5 C
     Filter assembly 1, slot 4        29.0 C
     Filter assembly 2, slot 1        28.7 C
     Filter assembly 2, slot 2        28.7 C
     Filter assembly 2, slot 3        28.6 C
     Filter assembly 2, slot 4        28.7 C



The user experience
-------------------

The Ipython/bsui prompt at BMM is heavily modified to give important
at-a-glance information about the state of the beamline.

.. _fig-prompt:
.. figure::  _images/prompt.png
   :target: _images/prompt.png
   :width: 40%
   :align: center

   The BlueSky user prompt at BMM

The white characters at the beginning of the prompt show the
:numref:`photon delivery system mode (Section %s) <change-mode>` |nd|
currently :quoted:`XRD` |nd| and the :numref:`monochromator crystals
(Section %s) <change-crystals>` currently in use |nd| currently
Si(311).

The red :quoted:`A` and :quoted:`B` indicate that the A and B (front
end and photon) shutters are currently closed.  When open these
letters are blue.  The italicized blue text gives the beam current.
(This picture was made during a maintenance period.)  Finally, the
bright green number indicates the command count, just like the
default Ipython prompt.

.. _start_end:

Starting and ending an experiment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a new experiment begins, run the command::

  new_experiment('folder')

This will create ``folder`` and populate it with an
:numref:`experimental log (Section %s) <log>`, define the ``DATA``
variable for use in simplifying certain commands, write a template for
a :numref:`scan.ini file (Section %s) <xafs>`, write a template
for a :numref:`macro file (Section %s) <macro>`, and configure the
logger to write a log file for this experiment.

Once the experiment is finished, run this command::

  end_experiment()

This will reset the logger and the ``DATA`` variable.


Getting help at the command line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see a summary of common commands, use ``BMM_help()``:

.. code-block:: text

   Open the shutter:               shb.open()
   Close the shutter:              shb.close()

   Change energy:                  RE(mv(dcm.energy, <energy>))
   Move a motor, absolute:         RE(mv(<motor>, <position>))
   Move a motor, relative:         RE(mvr(<motor>, <delta>))
   Where is a motor?               <motor>.wh()

   Where is the DCM?               dcm.wh()
   Where is M2?                    m2.wh()
   Where is M3?                    m3.wh()
   Where are the slits?            slits3.wh()
   Where is the XAFS table?        xafs_table.wh()

   Summarize all motor positions:  ms()
   Summarize utilities:            su()

   How long will a scan seq. be?   howlong(DATA + 'scan.ini')
   Run a scan sequence:            RE(xafs(DATA + 'scan.ini'))
   Scan a motor, plot a detector:  RE(linescan(<det>, <motor>, <start>, <stop>, <nsteps>))
   Scan 2 motors, plot a detector: RE(areascan(<det>, <slow motor>, <start>, <stop>, <nsteps>, <fast motor>, <start>, <stop>, <nsteps>))
   Make a log entry:               BMM_log_info("blah blah blah")

   DATA = /home/bravel/BMM_Data/bucket

   All the details: https://nsls-ii-bmm.github.io/BeamlineManual/index.html

and to see a summary of some useful command line hotkeys,
``BMM_keys()``:

.. code-block:: text

   Abort scan:             Ctrl-c twice!
   Search backwards:       Ctrl-r
   Quit search:            Ctrl-g
   Beginning of line:      Ctrl-a
   End of line:            Ctrl-e
   Delete character        Ctrl-d
   Cut text to eol         Ctrl-k
   Cut text from bol       Ctrl-u
   Paste text              Ctrl-y

   More details: http://readline.kablamo.org/emacs.html


The day will come that we have a GUI for running XAFS experiments at
BMM.  For now, we have the command line.  Read on |nd| it's not too
difficult!





A Bit about BMM
---------------

BMM is an XAS beamline.  As such it is on the simpler end of things at
NSLS-II.  We use an NSLS-II `three-pole wiggler (3PW)
<https://www.bnl.gov/nsls2/project/source_properties.asp>`_ as our
photon source.  This provides broadband radiation throughout the hard
X-ray range, up to about 30 keV.  It is a small device |nd| only about
40 cm long and with a magnetic path length of about 12 cm |nd| which
is inserted in a short section between the two bend magnets in the
dual-bend achromat lattice at NSLS-II.  The flux is certainly not the
equal of any of the many-pole insertion devices in the straight, but
it is highly performant for many XAS experiment.

About 13 meters from the source, we have a paraboloid collimating
mirror.  This position is well within the storage ring tunnel and
about 12 meters from the entrance to the BMM first optical enclosure.
We placed a mirror at that location to capture the largest possible
swath of the divergent light coming from the 3PW source.  A paraboloid
is the correct shape for focusing light in both the horizontal and
vertical directions.  However, a paraboloid must be a fixed figure,
fixed angle device in order to optimally collimate the light.  Because
the mirror is in the front end, thus inaccessible during operations,
we found the paraboloid to be an attractive solution.  Once aligned in
the beam, it should never need adjustment.

The collimated light is delivered to a double crystal monochromator
(DCM).  The DCM has pairs of Si(111) and Si(311) crystals which are
accessed by :numref:`translating the DCM vacuum vessel laterally
(Section %s) <change-crystals>` .  A transition between the two
crystal sets takes about 2 minutes.

After the DCM, we have a toroidal focusing mirror followed by a flat
harmonic rejection mirror.  One or both of these mirrors is in the
beam depending on :numref:`the configuration of the XAS experiment
(Section %s) <change-mode>` in the end station.  Because the beam is
deflected upward after the collimating mirror, at least one of the
mirrors after the DCM must be used in order to deflect the beam
through the lengthy transport pipe and into the end station.

Because the collimating mirror is at a fixed angle, it only serves as
a harmonic rejection mirror above an energy determined by its
operating angle.  That turns out to be about 23.5 keV.  For XAS
experiments conducted above 8 keV, then, the harmonic rejection
provided by the collimating mirror is adequate.  At lower energies,
the flat harmonic rejection mirror is used to provide clean beam.

With just the harmonic rejection mirror in place, a beam of size 8 mm
by 1.4 mm is delivered to the end station.  For many XAS experiments,
this rather large beam is desirable.  Indeed, many of the visitors to
BMM specifically request the large beam for their experiments.  With
the focusing mirror in place, that large swath is reduced to a spot of
about 300 |mu| m by 200 |mu| m.
