..
   This manual is copyright 2018 Bruce Ravel and released under
   The Creative Commons Attribution-ShareAlike License
   http://creativecommons.org/licenses/by-sa/3.0/

XAFS scans
==========

The BMM step scan plan starts by editing an `INI file
<https://en.wikipedia.org/wiki/INI_file>`_.  This is a simple
keyword/value system where the keyword is separated from the value by
an equals sign and a line contains a single keyword/value pair.

This file captures the set of metadata that the user supplies to
specify the details of the step scan, the basic configuration of the
beamline, and some details about the sample preparation.

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

At line 1, the location of the output data files in specified.
Although this INI file need not be in the same location as the output
data, users are encouraged to use the same folder for both.  The INI
file, then, serves to document how the data were collected.

At line 2, the file name stub for the output data is specified.  The
user is encouraged (but, again, not required) to use the same stub for
the INI file.

Line 3 contains the names of the people running the experiment.

Lines 6 to 11 specify some fundamental details about the sample being
measured.  :quoted:`sample` is intended to capture the stoichiometry
or other composition information about the sample.  :quoted:`prep`
captures the details of the sample preparation.  :quoted:`comment` is
to say anything else about the sample.

Lines 13 and 14 are used number successive scans in a measurement
sequence.  In this case, the first scan will be measured to
``/home/bravel/BMM_Data/303200/cufoil.001`` with subsequent scans
being ``cufoil.002`` and ``cufoil.003``.

Lines 16 through 20 are flags indicating various aspects of the
measurement.  ``snapshots`` sets whether photos will be taken of the
experimental setup.  If True, the jpg files will have names which use
the file name stub.  ``bothways`` and ``channelcut`` indicate aspects
of the monochromator motion.  ``focus`` and ``hr`` indicate the state
of the focusing and harmonic rejection mirrors.  True indicates that
the mirrors are in the beam path.

Line 23 shows sets how plots will be made on screen during the scan.

Finally, lines 27 to 29 set the energy and dwell time grids of the
step scan.


Running an XAFS scan
--------------------

Do this::

  RE(xafs('/path/to/scan.ini'))

#. Verify the content of the INI file with a user prompt

#. Make an entry in the experimental log indicating the INI contents
   and the current motor positions of all the important motors

#. Take snapshots of the XAS webcam and the analog camera near the sample

#. Move to the center of the angular range of motion of the scan and
   enter pseudo-channel-cut mode

#. Move to the beginning of the scan range and begin taking scans

#. After each scan, extract the data table from the database and wrote
   an ASCII file in the `XDI format
   <https://github.com/XraySpectroscopy/XAS-Data-Interchange>`_



Revisiting an XAFS scan
-----------------------

Grab from database, write to an XDI file::

  db2xdi('/path/to/data/file', '<id>')

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
experiment log indicating the times that the scan sequence begins and
ends.

Setting the ``BMM_xsp.prompt`` parameter to ``False`` at lines 2 skips
the step in the ``xafs()`` macro where the user is prompted to verify
that the scan is set iup correctly.


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

  %run -i /path/to/macro.py'

then run the macro by invoking the scan sequence function through the
run engine::

  RE(scan_sequence())

