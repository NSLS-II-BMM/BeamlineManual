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

   snapshots  = True

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
   is the energy reference for the ``bounds``.

   .. todo:: Look up E0 given the element and edge symbols, remove ``e0`` keyword

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

``snapshots`` (line 16)
   ``True`` to take snapshots from the XAS webcam and analog camera
   before beginning the scan sequence.  ``False`` to skip the
   snapshots

``mode`` (line 19)
   Indicate how data should be displayed on screen during a scan.  The
   options are ``transmission``, ``fluorescence``, ``both``, or
   ``reference``.  ``both`` means to display *both* the transmission
   and fluorescence during the scan.


Scan regions
------------

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
``k``.  Numbers followed by ``k`` are interpreted as being value sin
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

.. todo:: Much more sanity checking & sanitizing of input

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

.. todo:: Improve heuristic by doing statistics on scans


Running an XAFS scan
--------------------

To run a scan, do this::

  RE(xafs('/path/to/scan.ini'))

The argument is the path to the INI file described above.

This plan is a wrapper around `BlueSky's scan_nd() plan
<https://nsls-ii.github.io/bluesky/plans.html#multi-dimensional-scans>`_.
It does the following chores:

#. Verifies the content of the INI file with a user prompt

#. Makes an entry in the experimental log indicating the INI contents
   and the current motor positions of all the important motors

#. Takes snapshots of the XAS webcam and the analog camera near the sample

#. Moves to the center of the angular range of motion of the scan and
   enter pseudo-channel-cut mode

#. Generates a plotting subscription appropriate to the value of
   ``mode`` in the INI file

#. Enables a set of suspenders which will suspend the current XAFS
   scan in the event of a beam dump or a shutter closing (the
   suspenders are disabled at the end of the scan sequence)

#. Moves to the beginning of the scan range and begin taking scans
   using the ``scan_nd()`` plan and cyclers for energy values and dwell
   times constructed from ``bounds``, ``steps``, and ``times`` in
   the INI file

#. For each scan, notes the start and end times of the scan in the
   experimental log along with the unique and transient IDs of the
   scan in the beamline archive database

#. After each scan, extracts the data table from the database and wrote
   an ASCII file in the `XDI format
   <https://github.com/XraySpectroscopy/XAS-Data-Interchange>`_

The plan also provides some tools to cleanup correctly (i.e. kill
certain motors, reset certain parameters) after a scan sequence ends
or is terminated.

Revisiting an XAFS scan
-----------------------

Grab database entry and write it to an XDI file::

  db2xdi('/path/to/data/file', '<id>')

The first argument is the name of the output data file.  The second
argument is either the scan's unique ID |nd| something like
``f6619ed7-a8e5-41c2-a499-f793b0fcacec`` |nd| or the scan's transient
id number.  Both the unique and transient ids can be found in the
experimental log.

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
      BMM_xsp.prompt = False
      BMM_info('Starting scan sequence')

      yield from mv(xafs_linx, 23.86, xafs_liny, 71.27)
      yield from xafs('/path/to/sample1.ini')

      yield from mv(xafs_linx, 23.86, xafs_liny, 81.27)
      yield from xafs('/path/to/sample2.ini')

      BMM_xsp.prompt = True
      BMM_info('Scan sequence finished')

The calls to ``BMM_info()`` at lines 3 and 12 insert lines in the
:numref:`experiment log (Section %s) <log>` indicating the times that
the scan sequence begins and ends.

Setting the ``BMM_xsp.prompt`` parameter to ``False`` at lines 2 skips
the step in the ``xafs()`` macro where the user is prompted to verify
that the scan is set up correctly.

Alternately, you can use a single, master :file:`scan.ini` file that
covers all the metadata common to all the samples in a sequence.
Then, as part of the argument to the ``xafs()`` plan, specify those
metadata items specific to the sample.

.. sourcecode:: python
   :linenos:

   def scan_sequence():
      BMM_xsp.prompt = False
      BMM_info('Starting scan sequence')

      yield from mv(xafs_linx, 23.86, xafs_liny, 71.27)
      yield from xafs('/path/to/scan.ini', filename = 'sample1', prep = 'pressed pellet')

      yield from mv(xafs_linx, 23.86, xafs_liny, 81.27)
      yield from xafs('/path/to/scan.ini', filename = 'sample2', prep = 'powder on tape')

      BMM_xsp.prompt = True
      BMM_info('Scan sequence finished')

Any keyword from the INI file can be used as a command argument in the
call to ``xafs()``.  Arguments to ``xafs()`` will take priority over
values in the INI file.


Once you have prepared the macro file, you must reload the macro into
the running BlueSky session::

  %run -i '/path/to/macro.py'

then run the macro by invoking the scan sequence function through the
run engine::

  RE(scan_sequence())

XAFS data file
--------------

XAFS data files are written to the `XDI format
<https://github.com/XraySpectroscopy/XAS-Data-Interchange>`_.  Here is
an example.  You can see how the metadata from the INI file and
elsewhere is captured in the output XDI file.

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
   # Mono.name: Si(311)
   # Mono.d_spacing: 1.6376385 Å
   # Mono.encoder_resolution: 0.0000050 deg/ct
   # Mono.angle_offset: 15.9943932 deg
   # Mono.scan_mode: pseudo channel cut
   # Mono.scan_type: step
   # Mono.direction: forward in energy
   # Mono.first_crystal_temperature: 30.2 C
   # Mono.compton_shield_temperature: 30.5 C
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
