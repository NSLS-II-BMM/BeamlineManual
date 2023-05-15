..  
   This document was developed primarily by a NIST employee. Pursuant
   to title 17 United States Code Section 105, works of NIST employees
   are not subject to copyright protection in the United States. Thus
   this repository may not be licensed under the same terms as Bluesky
   itself.

   See the LICENSE file for details.

.. _intro:

Introduction to BMM
===================

BMM is NIST's Beamline for Materials Measurement.

At the unix command line, type ``bsui`` to start the BlueSky user
interface.  bsui is simply an `Ipython shell <https://ipython.org/>`_
with some customizations specific to BlueSky.  On top of that, there
are a number of customizations specific to BMM.


In this user manual, there are chapters covering most of the chores
one will need to do at the beamline, including:

#. moving motors
#. changing the state of the photon delivery system
#. making motor scans
#. making energy scans
#. interacting with the beamline's electronic log book
#. troubleshooting common problems

TL;DR
-----

**Open/close the shutter**
   ``shb.open()`` and ``shb.close()``, see :numref:`{name}, Section {number} <shutters>`

**Change energy**
   Use the ``RE(change_edge())`` command, see :numref:`{name}, Section {number} <pds>`

**Sample alignment scans**
   Use the ``RE(linescan())`` command, see :numref:`{name}, Section {number} <linescan>`

**XAFS scan**
   Use the ``RE(xafs())`` command, see :numref:`{name}, Section {number} <xafsscan>`

**Import an automation spreadsheet**
   Prepare a spreadsheet, then ``xlsx()``, see :numref:`{name}, Section {number} <automation>`



The user experience
-------------------

The Ipython/bsui prompt at BMM is modified to provide at-a-glance
information about the state of the beamline.

.. _fig-prompt:
.. figure::  _images/prompt.png
   :target: _images/prompt.png
   :width: 40%
   :align: center

   The BlueSky user prompt at BMM

* The green ``BMM`` indicates that the beamline is :numref:`set up and
  ready for the user (see Section %s) <start_end>`.  When the beamline
  is not ready for users, the ``BMM`` string is red.

* The string ``D.111`` indicates that the photon delivery system is in
  :numref:`mode D (see Table %s) <pds-modes>` and that :numref:`the
  Si(111) monochromator (Section %s) <change-crystals>` is in use.

* The green number in square brackets is an incremented count of how
  many commands have been issued since ``bsui`` was started.

* If the prompt starts with three red exclamation points |nd| something like 

      :red:`!!!` :green:`BMM` D.111 :green:`[1]`

  that means that some motors were not connected when Bluesky started.
  Contact beamline staff immediately!

.. _cadashboard:

CA Dashboard
~~~~~~~~~~~~

At the top of the big screen, you see a crude-but-handy beamline
monitor.  It looks like this:

.. _fig-cadashboard:
.. figure::  _images/cadashboard.png
   :target: _images/cadashboard.png
   :width: 100%
   :align: center

   The CA dashboard beamline monitor

This provides a (very) concise overview of the state of the beamline.

**Line 1**
   In short, if the top line has no red text, the beamline is all ready to go.

   + BMM is enabled (green) or disabled (red)
   + The BM, FE, & user photon shutters are open (green) or closed (red)
   + The ring current
   + The state of vacuum sections 1 through 7 |nd| green means vacuum
     level is OK, red means vacuum level is high
   + The state of the in-vacuum motors, 4 on the DCM, 2 on the
     focusing mirror, 2 on the harmonic rejection mirror |nd| green
     means temperature is OK, red means temperature is high
   + The open (green) or closed (red) state of the 3 front end gate
     valves and the 6 beamline gate valves

**Line 2**
   + The energy position of the monochromator
   + The signals on the I0 and It ion chambers, measured in nanoamps
   + The current operation at the beamline, options are: idle (white),
     XAFS scan (pink), line scan (cyan), area scan (yellow), or time
     scan (blue)

**Line 3**
   + Positions of common sample motors and size of sample slits

For more information about this tool, `follow this link
<https://wiki-nsls2.bnl.gov/beamline6BM/index.php/Cadashboard>`_,
which explains how to run the tool and position it on the screen.  It
also explains how to launch the tool when the beamline is set up for
XRD measurements.


.. _slack:

Slack and Google Drive
~~~~~~~~~~~~~~~~~~~~~~

At the beginning of your experiment, you will be invited to the BMM
Slack workspace.  There you can follow along with the progress of the
experiment in the #beamtime channel.

Throughout the course of the experiment, messages and figures will be
automatically posted to that channel.  This allows someone to keep
track of progress and to keep an eye on data quality without being
physically at the beamline.

.. _fig-slack:
.. figure::  _images/slack.png
   :target: _images/slack.png
   :width: 50%
   :align: center

   An example of messages and a picture of measured data posted to the
   beamline Slack channel.

The measured data along with the entire contents of the 
:numref:`measurement dossier (Section %s) <dossier>` will be synched
to Google Drive.  At the beginning of the experiment (in fact, when
the ``start_experiment()`` command described in the next session is
run), a folder for the experiment will be created on Google Drive.
The contents of the user's data folder will be synched frequently to
that folder throughout the course of the experiment, including
every time an individual XAFS scan finishes.

This allows a remote user to examine the data being measured in
almost-real time.  The data will be available on Google Drive within a
few seconds of the end of each scan.

Along with an invitation to the Slack workspace, the user will receive
an invitation to share the Google Drive.


.. _start_end:

Starting and ending an experiment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a new experiment begins, run the command::

  BMMuser.start_experiment(name='Betty Cooper', date='2019-02-29', gup=123456, saf=654321)

This will create that data folder and populate it with an
:numref:`experimental log (Section %s) <log>`, write a template for a
:numref:`macro file (Section %s) <macro>`, configure the logger to
write a :numref:`user log file (Section %s) <logfile>` for this
experiment, set the GUP and SAF numbers as metadata for output files,
set up :numref:`snapshot (Section %s) <snap>` and :numref:`dossier
(Section %s) <dossier>` folders, and perfrom other experiment start-up
chores.

The ``name`` should be the PI's full name, preferably transliterated
into normal ASCII.  The ``date`` should be the starting day of the
experiment in the ``YYYY-MM-DD`` format.  The ```GUP`` and ``SAF``
numbers can be found on the posted safety approval form.

Once the experiment is finished, run this command::

  BMMuser.end_experiment()

This will reset the logger and the ``DATA`` variable and unset the GUP
and SAF numbers.


..
  Electrochemistry experiments
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  .. note:: January 2022

     Electrochemistry is not yet properly supported in the experimental
     work flow.  This section is remains aspirational.

  The data acquisition system at BMM has rudimentary support for
  electrochemistry experiments using the BioLogic potentiostat.  When
  starting a new experiment, do this::

    BMMuser.start_experiment(name='Betty Cooper', date='2019-02-29', gup=123456, saf=654321, echem=True)

  The ``echem`` argument, when set to ``True`` tells the system to look
  for data from the potentiostat in the appropriate place on the Windows
  computer running the EC-Lab software.  It will make a folder called
  ``electrochemistry`` in the data folder and make a folder on the
  Windows machine at ``C:Users\xf06nm\My Documents\EC-Lab\Data``.
  There will be a folder with the PI's name and a subfolder with the
  start date of the experiment.

  At the end of the experiment, the electrochemistry files are copied
  from the Windows machine to the data folder.  This puts all of the
  data in one place and makes sure that the electrochemistry data are
  backed up correctly.


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

and to see a summary of some useful command line hotkeys, use ``%k``:

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


BMM and Building 743
--------------------


BMM is on the south side of the NSLS-II building.  You should park at
building 743 and enter through the main entrance of 743.

.. _fig-sitemap:
.. figure::  _images/map.png
   :target: _images/map.png
   :width: 60%
   :align: center

   Route from the Main Gate to Building 743


Walk though the lobby to the doors that lead out onto the experimental
floor.  BMM is just across the walk way from the doors to the 743 lobby.



.. subfigstart::

.. _fig-743lobby:
.. figure::  _images/743lobby.jpg
   :target: _images/743lobby.jpg
   :width: 100%
   :align: center

   Approaching the floor through the lobby of Building 743

.. _fig-corridor:
.. figure::  _images/corridor.jpg
   :target: _images/corridor.jpg
   :width: 100%
   :align: center

   BMM is just across the corridor from the door to the 743 lobby

.. _fig-controlstation:
.. figure::  _images/BMMcontrolstation.jpg
   :target: _images/BMMcontrolstation.jpg
   :width: 100%
   :align: center

   Walk past the diagonal support beam and head into the BMM control
   station

.. subfigend::
   :width: 0.31
   :label: _fig-XRFINST



BMM's staff have offices on the outer hallway of Building 743.


.. _fig-lob3:
.. figure::  _images/LOB-3.png
   :target: _images/LOB-3.png
   :width: 90%
   :align: center

   Bruce's, Jean's and Vesna's offices in Building 743




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
by 1 mm is delivered to the end station.  For many XAS experiments,
this rather large beam is desirable.  Indeed, many of the visitors to
BMM specifically request the large beam for their experiments.  With
the focusing mirror in place, that large swath is reduced to a spot of
about 300 |mu| m by 200 |mu| m.

Acknowledgements
----------------

This documentation project uses the lovely `{book}theme
<https://sphinx-book-theme.readthedocs.io/en/latest/index.html>`__
from the `The Executable Book Project
<https://ebp.jupyterbook.org/>`__.

This project uses a GitHub action to build and deploy this document
whenever a ``git push`` happens.

BMM's profile was mostly written by Bruce.  But I could not have done
so without the help of several members of NSLS-II's DSSI program.  In
particular, I want to thank Dan Allan, Tom Caswell, Josh Lynch, Max
Ratikin, Dmitri Gavrilov, and Stuart Campbell

BMM also makes use of lots of great python tools.  Along with all the
obvious candidates in the scientific python ecosystem, Matt Newville's
Larch is used for processing every XAS scan that gets measured.


A note about copyright
----------------------

This document and `the BlueSky data collection profile
<https://github.com/NSLS-II-BMM/profile_collection>`__ it covers was
developed primarily by a NIST employee. Pursuant to title 17 United
States Code Section 105, works of NIST employees are not subject to
copyright protection in the United States. Thus this repository may
not be licensed under the same terms as Bluesky itself or its
documentation.

See the `LICENSE file
<https://raw.githubusercontent.com/NSLS-II-BMM/BeamlineManual/master/LICENSE>`__
for details.
