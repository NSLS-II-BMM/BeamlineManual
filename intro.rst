..
   This manual is copyright 2018 Bruce Ravel and released under
   The Creative Commons Attribution-ShareAlike License
   http://creativecommons.org/licenses/by-sa/3.0/

.. role:: strike
    :class: strike

.. _intro:

Introduction to BMM
===================

At the unix command line, type ``bsui`` to start the BlueSky user
interface.  bsui is simply an `Ipython shell <https://ipython.org/>`_
with some customizations specific to BlueSky.  On top of that, there
are a number of customizations specific to BMM.


In this user manual, there are chapters covering most of the chores
that a user will need to do at the beamline, including:

#. moving motors
#. understanding the state of the photon delivery system
#. making motor scans
#. making energy scans
#. interacting with the beamline's :quoted:`electronic log book`
#. troubleshooting common problems


The user experience
-------------------

The Ipython/bsui prompt at BMM is heavily modified to 
at-a-glance information about the state of the beamline.

.. _fig-prompt:
.. figure::  _images/prompt.png
   :target: _images/prompt.png
   :width: 40%
   :align: center

   The BlueSky user prompt at BMM

.. todo:: That prompt image is out of date.  Need to update image and
          discuss cadashboard. Also provide a picture of cadashboard.

The white characters at the beginning of the prompt show the
:numref:`photon delivery system mode (Section %s) <change-mode>` |nd|
currently :quoted:`XRD` |nd| and the :numref:`monochromator crystals
(Section %s) <change-crystals>` currently in use |nd| currently
Si(311).

:strike:`The red A and B indicate that the A and B (front end and
photon) shutters are currently closed.  When open these letters are
blue.` The italicized blue text gives the beam current.  (This picture
was made during a maintenance period.)  Finally, the bright green
number indicates the command count, just like the default Ipython
prompt.

.. _start_end:

Starting and ending an experiment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a new experiment begins, run the command::

  start_experiment(name='Betty Cooper', date='2019-02-28', gup=123456, saf=654321)

This will create that data folder and populate it with an
:numref:`experimental log (Section %s) <log>`, define the ``DATA``
variable for use in simplifying certain commands, write a template for
a :numref:`scan.ini file (Section %s) <xafs>`, write a template for a
:numref:`macro file (Section %s) <macro>`, configure the logger to
write a :numref:`user log file (Section %s) <logfile>` for this
experiment, set the GUP and SAF numbers as metadata for output files,
and set up :numref:`snapshot (Section %s) <snap>` and :numref:`dossier
(Section %s) <dossier>` folders.


The ``name`` should be the PI's full name, preferably transliterated
into normal ASCII.  The ``date`` should be the starting day of the
experiment in the ``YYYY-MM-DD`` format.

Once the experiment is finished, run this command::

  end_experiment()

This will reset the logger and the ``DATA`` variable and unset the GUP
and SAF numbers.


Getting help at the command line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see a summary of common commands, use ``%h``:

.. code-block:: text

   Open the shutter:                 shb.open()
   Close the shutter:                shb.close()

   Change energy:                    RE(mv(dcm.energy, <energy>))
   Move a motor, absolute:           RE(mv(<motor>, <position>))
   Move a motor, relative:           RE(mvr(<motor>, <delta>))
   Where is a motor?                 %w <motor>

   Where is the DCM?                 %w dcm
   Where is M2?                      %w m2
   Where is M3?                      %w m3
   Where are the slits?              %w slits3
   Where is the XAFS table?          %w xafs_table

   Summarize all motor positions:    %m
   Summarize utilities:              %ut

   How long will a scan seq. be?     howlong('scan.ini')
   Run a scan sequence:              RE(xafs('scan.ini'))
   Scan a motor, plot a detector:    RE(linescan(<det>, <motor>, <start>, <stop>, <nsteps>))
   Scan 2 motors, plot a detector:   RE(areascan(<det>, <slow motor>, <start>, <stop>, <nsteps>, <fast motor>, <start>, <stop>, <nsteps>))
   Make a log entry:                 BMM_log_info("blah blah blah")

   DATA = /home/bravel/BMM_Data/bucket

   All the details: https://nsls-ii-bmm.github.io/BeamlineManual/index.html

and to see a summary of some useful command line hotkeys, ``%k``:

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
