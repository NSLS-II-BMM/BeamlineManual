..
   This manual is copyright 2018 Bruce Ravel and released under
   The Creative Commons Attribution-ShareAlike License
   http://creativecommons.org/licenses/by-sa/3.0/

.. _xafs:

XAFS scans
==========

The BMM step scan plan starts by editing an `INI file
<https://en.wikipedia.org/wiki/INI_file>`_.  This is a simple
keyword/value system where the keyword is separated from the value by
an equals sign and each line contains a single keyword/value pair.

This file captures the set of metadata that the user supplies to
specify the details of the step scan, the basic configuration of the
beamline, and some details about the sample preparation.  Most of this
metadata is captured in the beamline database and written to the
header of the output data files.

This file is typically stored in the same folder where the data files
are written and is called by name when running an XAFS scan.


.. _ini:

The INI file
------------

.. sourcecode:: ini
   :linenos:

   [scan]
   folder        = /home/bravel/BMM_Data/303200
   filename      = cufoil
   experimenters = Betty Cooper, Veronica Lodge, Archibald Andrews

   e0         = 8979
   element    = Cu
   edge       = K
   sample     = Cu metal
   prep       = standard foil
   comment    = Welcome to BMM

   nscans     = 3
   start      = 1

   usbstick   = True

   # mode is transmission, fluorescence, both, or reference
   mode = transmission

   ##  regions relative
   ##  to e0:         1      2      3      4
   bounds     = -200    -30     -10   15.5    15k
   steps      =      10     2.0    0.3    0.05k
   times      =      0.5    0.5    0.5    0.25k


Here is a complete explanation of the contents of the INI file.

``folder`` (line 1)
   The fully resolved path to the data folder

``filename`` (line 2)
   The stub for the names of the output data files and the snapshots

``experimenters`` (line 3)
   The name of the participants in the measurement

``e0`` (line 6)
   The edge energy for the element and edge of this measurement.  This
   is the energy reference for the ``bounds``.  If absent, the
   tabulated value determined from ``element`` and ``edge`` will be
   used. 

``element`` (line 7)
   The one- or two-letter symbol for the element.

``edge`` (line 8)
   The symbol (``K``, ``L3``, ``L2``, ``L1``) of the edge being
   measured.

``sample`` (line 9)
   This is intended to capture the stoichiometry or composition of the
   sample being measured.

``prep`` (line 10)
   This is intended to capture the details of how the sample was
   prepared for measurement.

``comment`` (line 11)
   This is for anything else you might want to say about your sample.

``nscans`` and ``start`` (lines 13 - 14)
   These are used to form the file extension of the output data file.
   They indicate the starting value of the number used as the file
   extension and how many repetitions of the scan to make.  The file
   extension is always a zero-padded, three-digit number,
   e.g. :file:`cufoil.001`, :file:`cufoil.002`, and so on.

   ``start`` is normally a positive integer but can also be the word
   ``next``, in which case the ``folder`` will be searched for
   files starting with ``filename`` and ending in a number.  The
   subsequent number will be used.  E.g. if ``cuedge.007`` is the
   highest numbered file in the ``cuedge`` sequence, running XAFS
   again using the same INI file will start with ``cuedge.008``.

``usbstick`` (line 16)
   ``True`` will examine the user-supplied filename for characters
   that cannot be part of a `filename
   <https://en.wikipedia.org/wiki/Filename#Reserved_characters_and_words>`_
   on a standard USB memory stick.  If any are found, the filename
   will be modified in a way that retains the meaning of the replaced
   characters, but which can be successfully written to a memory
   stick.  Since this is mostly an issue with Windows file systems,
   users who want to do  their data analysis on a Windows computer
   should use this option.  :numref:`See Section %s <usbsafe>`.

``mode`` (line 19)
   Indicate how data should be displayed on screen during a scan.  The
   options are ``transmission``, ``fluorescence``, ``both``, or
   ``reference``.  ``both`` means to display *both* the transmission
   and fluorescence during the scan.

   This parameter also controls what gets written to the output data
   files. In all cases, the signals from I0, It, and Ir are written to
   the data file.  If ``mode`` is ``fluorescence`` or ``both``, then
   16 columns related to the fluorescence detector are also
   written. The columns labeled ``dtc1``, ``dtc2``, ``dtc3``, and
   ``dtc4`` are the dead-time corrected signals for each of the four
   elements of the detector.  The ``roiN``, ``icrN``, and ``ocrN``
   columns give the signal in the discriminator window, the input
   count rate, and the output count rate for each element.  That is
   sufficient information to recompute the dead-time correction, if
   need be.

Comments begin with the hash (``#``) character and are ignored.


Scan regions
~~~~~~~~~~~~

In a typical step scan, we measure data on a coarse grid in the
pre-edge, a fine grid through the edge region, and on a constant grid
in photoelectron wavenumber in the extended region.  The ``bounds``,
``steps``, and ``times`` keywords (lines 23-25) are used to set this
grid.


``bounds`` indicates the energies |nd| relative to the ``e0`` value
|nd| where the step sizes and dwell times will change.  There **must**
always be one more value in the ``bounds`` list than in the ``steps``
and ``times`` lists.

For the ``bounds`` and ``steps`` lists, values **must** be either a
number or a string consisting of a number followed by the letter
``k``.  Numbers followed by ``k`` are interpreted as being values in
photoelectron wavenumber and are only sensible above the edge.

You may switch back and forth between energy and wavenumber values.
The ``bounds`` and ``steps`` lists are converted to energy values
before being used.

In the ``bounds`` lists, an energy value indicates an energy below or
above the ``e0`` value.  A wavenumber value inidcates a wavenumber
value above the edge.

In the ``steps`` list, an energy value indicates a step size in eV.  A
wavenumber value indicates a step size in |AA|:sup:`-1`.

In the ``times`` list, a number indicates a dwell time in seconds.  A
number followed by ``k`` indicates that the dwell time will grow as a
function of wavenumber above the edge.  I.e., a value of ``0.25k``
means that the dwell time will be 1 second at 4 |AA|:sup:`-1`, 2
seconds at 8 |AA|:sup:`-1`, and so on.


More Boolean options
~~~~~~~~~~~~~~~~~~~~

There are several aspects of the XAFS scan plan that can be enabled or
disabled from the INI file.  The sample INI file written by the
:numref:`BMMuser.start_experiment() command (Section %s) <start_end>`
does not include these options, but they can be added to the INI file
if needed.

``snapshots``
   ``True`` to take :numref:`snapshots (Section %s) <snap>` from the
   XAS webcam and analog camera before beginning the scan sequence.
   ``False`` to skip the snapshots.  Default: ``True``

``channelcut``
  ``True`` to measure XAFS with the monochromator in pseudo-channelcut
  mode.  ``False`` to measure in fixed exit mode.  Default: ``True``

``rockingcurve``
  ``True`` to measure a :numref:`rocking curve scan (Section %s)
  <special-linescans>` after moving to the pseudo-channelcut mode
  energy.  Default: ``False``

``bothways``
  ``True`` to measure XAFS in both directions of the monochromator.
  ``False`` to always measure in the positive energy (negative angle)
  direction.  Default: ``False``

``htmlpage`` 
  ``False`` to disable writing of the :numref:`static HTML dossier
  (Section %s) <dossier>`.  Default: ``True``

``ththth`` 
  ``True`` to measure with :numref:`Si(333) reflection (Section %s)
  <use333>` of the Si(111) monochromator .  Default: ``False``




Scan run time
-------------

To get an approximation of the time a scan will take, do::

  howlong('/path/to/scan.ini')

The argument is the path to the INI file described above.

This will make a guess of scan time for an individual scan using a
rather crude heuristic for scan overhead.  It will also multiply by
the number of scans to give a total time in hours for the scan
sequence.

.. code-block:: text

   reading ini file: /home/bravel/BMM_Data/303169/scan.ini

   Each scan will take about 17.9 minutes
   The sequence of 6 scans will take about 1.8 hours

.. todo:: Improve heuristic by doing statistics on scans.  Wait
   patiently for Andrew Welter's scan telemetry package.

.. _usbsafe:

Safe filenames for USB sticks
-----------------------------

`These characters are problematic for filenames
<https://en.wikipedia.org/wiki/Filename#Reserved_characters_and_words>`_:

.. code-block:: text

      ? * / \ % : | " < >

While there is no issue using these characters in filenames on the
beamline computer, you will find that files containing these names
cannot be written to a normal USB memory stick.  The file system used
on most memory sticks |nd| `FAT32
<https://en.wikipedia.org/wiki/USB_flash_drive#File_system>`_ |nd|
does not allow those characters in filenames.  This is true even if
the system the memory stick is connected to will allow those
characters.


.. table:: Character translations in filenames
   :name:  usb-characters

   ================   ==================   =======================
    character name     character            substitution string
   ================   ==================   =======================
    question mark      |mquad| ?            ``_QM_``		      
    asterisk           |mquad| |ast|        ``_STAR_``
    forward slash      |mquad| /            ``_SLASH_``		      
    backslash          |mquad| \\           ``_BACKSLASH_``		      
    percent            |mquad| %            ``_PERCENT_``		      
    colon              |mquad| :            ``_COLON_``		      
    vertical bar       |mquad| |verbar|     ``_VERBAR_``		      
    greater than       |mquad| >            ``_GT_``		      
    less than          |mquad| <            ``_LT_``		      
   ================   ==================   =======================


As an example, a filename like 

.. code-block:: text

   Fe precipitate <60 mM

will be converted to 

.. code-block:: text

   Fe precipitate _LT_60 mM

such that the output files will be called

.. code-block:: text

   Fe precipitate _LT_60 mM.001
   Fe precipitate _LT_60 mM.002
   ...

Note that spaces are fine in filenames.


.. _xafsscan:

Run an XAFS scan
----------------

To run a scan, do this::

  RE(xafs('scan.ini'))

The argument is the path to the INI file described above.  The
``DATA`` variable simplifies the use of this plan.  ``DATA`` gets set
to the location of your data folder when :numref:`beginning an
experiment (Section %s) <start_end>`.

This plan is a wrapper around `BlueSky's scan_nd() plan
<https://nsls-ii.github.io/bluesky/plans.html#multi-dimensional-scans>`_.
It does the following chores:

#. Verifies the content of the INI file with a user prompt

#. Makes an entry in the :numref:`experimental log (Section %s)
   <logfile>` indicating the INI contents and the current motor
   positions of all the important motors

#. Takes :numref:`snapshots (Section %s) <snap>` of the XAS webcam and
   the analog camera near the sample

#. Moves to the center of the angular range of motion of the scan and
   enters pseudo-channel-cut mode

#. Generates a plotting subscription appropriate to the value of
   ``mode`` in the INI file

#. Enables a :numref:`set of suspenders (Section %s) <interrupt>`
   which will suspend the current XAFS scan in the event of a beam
   dump or a shutter closing (the suspenders are disabled at the end
   of the scan sequence)

#. Moves to the beginning of the scan range and begins taking scans
   using the ``scan_nd()`` plan and `cyclers
   <https://matplotlib.org/cycler/>`_ for energy values and dwell
   times constructed from the values of ``bounds``, ``steps``, and
   ``times`` read from the INI file

#. For each scan, notes the start and end times of the scan in the
   :numref:`experimental log (Section %s) <logfile>` along with the
   unique and transient IDs of the scan in the beamline database

#. After each scan, extracts the data table from the database and writes
   an ASCII file in the `XDI format
   <https://github.com/XraySpectroscopy/XAS-Data-Interchange>`_

#. After the full sequence of scans, write :numref:`a dossier (Section
   %s) <dossier>` containing a fairly complete record of the
   measurement |nd| including a crude first pass at the data reduction
   and processing |nd| made by the XAFS plan.

The plan also provides some tools to cleanup correctly (i.e. kill
certain motors, reset certain parameters) after a scan sequence ends
or is terminated.


Location of scan.ini file
~~~~~~~~~~~~~~~~~~~~~~~~~

When you launch an XAFS scan doing::

  RE(xafs('scan.ini'))

the location of the ``scan.ini`` file is assumed to be in ``DATA``.
For instance, if ``DATA`` is ``/home/bravel/BMM_Data/303303/``, then
the scan plan will look for the file
``/home/bravel/BMM_Data/303303/scan.ini``.  This is equivalent to::

  RE(xafs(DATA + 'scan.ini'))

where ``+`` is the python :quoted:`string concatination` operator.

You can also explicitly state where your INI file is located, as in::

  RE(xafs('/home/bravel/BMM_Data/303303/scan.ini'))

In that case, the explicit location of the INI file will be used.

The ``DATA`` variable is set when the ``new_experiment()`` command is
run at the beginning of the experiment (:numref:`see Section %s
<start_end>`).  To know the value of the ``DATA`` variable, simply
type ``DATA`` at the command line and hit :button:`Enter`.


.. _interrupt:

Interrupt an XAFS scan
~~~~~~~~~~~~~~~~~~~~~~

There are several scenarios where you may need to interrupt or halt an
XAFS scan.

Pause a scan and *resume*
  You can pause a scan at any time by
  hitting :button:`Ctrl`-:button:`c` twice.  This will return you to
  the command line, leaving the scan in a paused state.  To *resume*
  the scan, do::

    RE.resume()

  The scan will then continue from where it left off.

*Stop* a scan
  You can pause a scan at any time by hitting
  :button:`Ctrl`-:button:`c` twice.  This will return you to the
  command line, leaving the scan in a paused state.  To *end* the
  scan, do::

    RE.stop()

  The scan will then terminate, returning all motors and detectors to
  their resting state.

  This will also terminate a paused scan::

    RE.abort()

  The difference is that ``RE.stop()`` will tag the database entry of
  the current scan as ``success`` while ``RE.abort()`` will tag it as
  ``failed``.  In every other way, the two are equivalent |nd| each
  one will shut the scan down gracefully.

Pause a scan due to external events
  When the XAFS scan starts, it initiates a set of `suspenders
  <https://nsls-ii.github.io/bluesky/state-machine.html#automated-suspension>`_
  which respond to various external events, such as a shutter closing
  or the ring current dumping.  When one of these suspenders triggers,
  the scan will enter a paused state.  It will resume once the
  condition causing the suspension is resolved.  For example, when the
  closed shutter is re-opened or current is restored to the ring.  In
  general, a short bit of time is required to pass once the suspension
  condition is resolved before the scan resumes.  For instance,
  5 seconds are allowed to pass after a shutter is re-opened.

`Here is a summary of pausing, resuming, and stopping scans using
BlueSky
<https://nsls-ii.github.io/bluesky/state-machine.html#summary>`_.

Revisit an XAFS scan
--------------------

Grab a database entry and write it to an XDI file::

  db2xdi('/path/to/data/file', '<id>')

The first argument is the name of the output data file.  The second
argument is either the scan's unique ID |nd| something like
``f6619ed7-a8e5-41c2-a499-f793b0fcacec`` |nd| or the scan's transient
id number.  Both the unique and transient ids can be found in
:numref:`the dossier (Section %s) <dossier>`.

.. _macro:

Scan sequence macro
-------------------

A macro at BMM is a short bit of python code which sequentially moves
motors and initiates scans.  A common way of doing this is to make an
INI file for each sample that intend to measure.  The macro then steps
to each sample, then runs the ``xafs()`` plan by calling the INI file
each sample.

.. sourcecode:: python
   :linenos:

   def scan_sequence():
      BMMuser.prompt = False
      BMM_info('Starting scan sequence')

      yield from mv(xafs_x, 23.86, xafs_y, 71.27)
      yield from xafs('sample1.ini')

      yield from mv(xafs_x, 23.86, xafs_y, 81.27)
      yield from xafs('sample2.ini')

      BMMuser.prompt = True
      BMM_info('Scan sequence finished')

The calls to ``BMM_info()`` at lines 3 and 12 insert lines in the
:numref:`experiment log (Section %s) <log>` indicating the times that
the scan sequence begins and ends.

Setting the ``BMMuser.prompt`` parameter to ``False`` at lines 2 skips
the step in the ``xafs()`` macro where the user is prompted to verify
that the scan is set up correctly.

Alternately, you can use a single, master :file:`scan.ini` file that
covers all the metadata common to all the samples in a sequence.
Then, as part of the argument to the ``xafs()`` plan, specify those
metadata items specific to the sample.

.. sourcecode:: python
   :linenos:

   def scan_sequence():
      BMMuser.prompt = False
      BMM_info('Starting scan sequence')

      yield from mv(xafs_x, 23.86, xafs_y, 71.27)
      yield from xafs('scan.ini', filename = 'sample1', prep = 'pressed pellet')

      yield from mv(xafs_x, 23.86, xafs_y, 81.27)
      yield from xafs('scan.ini', filename = 'sample2', prep = 'powder on tape')

      BMMuser.prompt = True
      BMM_info('Scan sequence finished')

:numref:`Any keyword (Section %s) <ini>` from the INI file can be used
as a command argument in the call to ``xafs()``.  Arguments to
``xafs()`` will take priority over values in the INI file.


Assuming your macro file is stored in your data folder under the name
``macro.py``, you can load or reload the macro into the running
BlueSky session::

  %run -i DATA+'macro.py'

then run the macro by invoking the scan sequence function through the
run engine::

  RE(scan_sequence())

Every time you edit the macro file, you **must** reload it into the
running BlueSky session.

The name of the macro file is not proscribed.  If it would be
convenient to have, say, ``macroFe.py`` and ``macroPt.py``, that's
fine.  Just be sure to explicitly ``%run -i`` the file using the
correct name.


XAFS data file
--------------

XAFS data files are written to the `XDI format
<https://github.com/XraySpectroscopy/XAS-Data-Interchange>`_.  Here is
an example.  You can see how the metadata from the INI file and
elsewhere is captured in the output XDI file.

.. todo:: Document use of ``XDI_record`` dictionary to control which
	  xafs motors and/or temperatures get recorded in the XDI header

.. code-block:: text

   # XDI/1.0 BlueSky/1.3.0
   # Beamline.name: BMM (06BM) -- Beamline for Materials Measurement
   # Beamline.xray_source: NSLS-II three-pole wiggler
   # Beamline.collimation: paraboloid mirror, 5 nm Rh on 30 nm Pt
   # Beamline.focusing: torroidal mirror with bender, 5 nm Rh on 30 nm Pt
   # Beamline.harmonic_rejection: none
   # Detector.I0: 10 cm N2
   # Detector.I1: 25 cm N2
   # Detector.I2: 25 cm N2
   # Detector.fluorescence: SII Vortex ME4 (4-element silicon drift)
   # Element.symbol: Mo
   # Element.edge: K
   # Facility.name: NSLS-II
   # Facility.current: 374.3 mA
   # Facility.energy: 3.0 GeV
   # Facility.mode: top-off
   # Facility.GUP: 333333
   # Facility.SAF: 344344
   # Mono.name: Si(311)
   # Mono.d_spacing: 1.6376385 Å
   # Mono.encoder_resolution: 0.0000050 deg/ct
   # Mono.angle_offset: 15.9943932 deg
   # Mono.scan_mode: pseudo channel cut
   # Mono.scan_type: step
   # Mono.direction: forward in energy
   # Sample.name: Sedovite
   # Sample.prep: speck of mineral in a holder in a gel cap
   # Sample.x_position: 2.750
   # Sample.y_position: 147.670
   # Scan.edge_energy: 20000.0
   # Scan.start_time: 2018-07-08T16:26:49
   # Scan.end_time: 2018-07-08T16:44:22
   # Scan.transient_id: 1447
   # Scan.uid: 442bb882-1e46-4607-a12d-1bca2efa74af
   # Scan.plot_hint: (DTC1 + DTC2 + DTC3 + DTC4) / I0  --  ($7+$8+$9+$10) / $4
   # Column.1: energy eV
   # Column.2: requested_energy eV
   # Column.3: measurement_time seconds
   # Column.4: I0 nA
   # Column.5: It nA
   # Column.6: Ir nA
   # Column.7: DTC1
   # Column.8: DTC2
   # Column.9: DTC3
   # Column.10: DTC4
   # Column.11: ROI1 counts
   # Column.12: ICR1 counts
   # Column.13: OCR1 counts
   # Column.14: ROI2 counts
   # Column.15: ICR2 counts
   # Column.16: OCR2 counts
   # Column.17: ROI3 counts
   # Column.18: ICR3 counts
   # Column.19: OCR3 counts
   # Column.20: ROI4 counts
   # Column.21: ICR4 counts
   # Column.22: OCR4 counts
   # ///////////
   # focused beam, Kyzylsai Dep., Chu-lli Mts., Zhambyl Dist., Kazakhstan 3852
   # -----------
   # energy  requested_energy  measurement_time  I0  It  Ir  DTC1  DTC2  DTC3  DTC4  ROI1  ICR1  OCR1  ROI2  ICR2  OCR2  ROI3  ICR3  OCR3  ROI4  ICR4  OCR4
   19809.967  19810.000  0.500  22.780277  28.026418  5.844915  3393.671531  3512.331211  2189.485830  2294.254018  2984.0  86162.0  79706.0  3085.0  86771.0  80213.0  2018.0  57884.0  55169.0  2085.0  64398.0  60757.0
   19820.016  19820.000  0.500  23.017712  28.316410  5.912596  3607.981130  3515.807498  2272.542220  2255.901234  3160.0  87991.0  81171.0  3088.0  87790.0  81205.0  2093.0  58242.0  55481.0  2036.0  66029.0  61927.0
   19830.022  19830.000  0.500  23.191409  28.546075  5.971688  3398.408050  3343.071835  2237.827496  2348.453171  2983.0  88018.0  81376.0  2930.0  88064.0  81298.0  2061.0  59218.0  56443.0  2120.0  66896.0  62787.0
   19840.073  19840.000  0.500  23.022700  28.346179  5.941913  3424.112880  3464.005608  2199.187023  2294.868496  3007.0  87171.0  80589.0  3042.0  87734.0  81137.0  2023.0  58516.0  55684.0  2075.0  66318.0  62324.0
   .
    .
     .
