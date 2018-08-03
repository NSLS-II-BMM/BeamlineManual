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
an equals sign and a line contains a single keyword/value pair.

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
   bothways   = False
   channelcut = True
   focus      = False
   hr         = True

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

   .. todo:: Look up E0 given the element and edge symbols

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

``bothways`` (line 17)
   *Experimental feature* |nd| ``True`` to measure in both monochromator
   directions, ``False`` to only measure in the increasing-energy
   (decreasing angle) direction.

``channelcut`` (line 18)
   *Work in progress* |nd| ``True`` to measure XAFS in
   pseudo-channel-cut mode, ``False`` to measure in fixed-exit mode.

``focus`` (line 19)
   ``True`` when the focusing mirror is in use.

``hr`` (line 20)
   ``True`` when the harmonic rejection mirror is in use.

``mode`` (line 23)
   Indicate how data should be displayed on screen during a scan.  The
   options are ``transmission``, ``fluorescence``, ``both``, or
   ``reference``.  ``both`` means to display *both* the transmission
   and fluorescence during the scan.


Scan regions
------------

In a typical step scan, we measure data on a coarse grid in the
pre-edge, a fine grid through the edge region, and on a constant grid
in photoelectron wavenumber in the extended region.  The ``bounds``,
``steps``, and ``times`` keywords (lines 27-29) are used to set this
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

#. Moves to the beginning of the scan range and begin taking scans
   using the ``scan_n()`` plan and cyclers for energy values and dwell
   times constructed form the ``bounds``, ``steps``, and ``times`` in
   the INI file

#. After each scan, extracts the data table from the database and wrote
   an ASCII file in the `XDI format
   <https://github.com/XraySpectroscopy/XAS-Data-Interchange>`_

The plan also provides some tools to cleanup correctly after a scan
sequence (i.e. kill certain motors, reset certain parameters) ends or
is terminated.

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

Any keyword form the INI file can be used as command argument in the
call to ``xafs()``.  Arguments to ``xafs()`` tak priority over values
in the INI file.


Once you have prepared the macro file, you must reload the macro into
the running BlueSky session::

  %run -i '/path/to/macro.py'

then run the macro by invoking the scan sequence function through the
run engine::

  RE(scan_sequence())

