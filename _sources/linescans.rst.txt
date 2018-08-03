..
   This manual is copyright 2018 Bruce Ravel and released under
   The Creative Commons Attribution-ShareAlike License
   http://creativecommons.org/licenses/by-sa/3.0/

.. _linescan:

Sample position scans
=====================

General line scans
------------------

A line scan is a simple scan of a single motor axis with an on-screen
plot.  At BMM this sort of scan is typically done using the
``linescan()`` plan.  This is a wrapper around BlueSky's `rel_scan()
<https://nsls-ii.github.io/bluesky/generated/bluesky.plans.rel_scan.html#bluesky.plans.rel_scan>`_.

In BMM's ``linescan()`` plan, the scan is always a relative scan
around the current position of the motor being scanned.  It works like
this::

    RE(linescan('x', 'it', -4, 4, 81))

The arguments are:

#. The motor axis to be scanned.  This can be either the motor's
   BlueSky name or the nickname in the :ref:`xafs-stages` table.  So,
   these are equivalent::

     RE(linescan('x', 'it', -4, 4, 81))
     RE(linescan(xafs_linx, 'it', -4, 4, 81))

   For a motor that does not have a nickname, you must use the BlueSky
   names, as in::

     RE(linescan(slits3_outboard, 'it', -1, 1, 21))

#. The detector for the plotted signal.  The choices are ``it``,
   ``if``, and ``i0``.  For the ``it`` choice, the plot will display
   the ratio of It/I0.  Similarly for the ``if`` choice, the plot will
   display the sum of four silicon drift channels normalized by I0.
   For the ``i0`` choice, the signal on the I0 chamber will be plotted.

#. The starting position of the motor scan, relative to the current
   position.

#. The ending position of the motor scan, relative to the current
   position.

#. The number of steps in the scan.


At the end of the scan, you are prompted with the following question::

    Pluck motor position from the plot? [Yn]

If you answer ``Y``, or simply hit return, you will be prompted to
single click the left mouse button on the plot.  The motor that was
scanned will then move to the motor position you clicked on.

You can skip the :quoted:`click for motor position` step by typing
``n`` and hitting return.


Plucking a point from a scan
----------------------------

If you want to repeat the action of clicking on a point and moving the
motor to the click-upon point, do::

  RE(pluck())

This will enable the mouse click and subsequent motion on the most
recent plot.  The ``pluck()`` command *only* works on the most recent
plot.  You may not pluck from an older plot that is still displayed on
the screen.

Of course, an older plot remains active in the sense that you can pass
the cursor over the plot and read the mouse coordinates in the bottom,
left corner of the plot window.  You can find a point in this way,
then do a movement command line::

  RE(mv(xafs_liny, 28.31))


Revisit a line scan
-------------------

Retrieve data from the database using the database key or scan ID::

   ls2dat('/path/to/output.file', '<id>')

This writes from the database to an output file.  The output file is a
simple column data file without header or metadata.

The first argument is the name of the output data file.  The second
argument is either the scan's unique ID |nd| something like 
``f6619ed7-a8e5-41c2-a499-f793b0fcacec`` |nd| or the scan's transient
id number.  Both the unique and transient ids can be found in the
experimental log.


Special purpose line scans
--------------------------

A number of line scan types are so common and so often performed with
the same arguments that they have special names.

**Rocking curve scan**
   This command::

     RE(rocking_curve())

   does a scan of the pitch of the second mono crystal and plots the
   signal on I0.  At the end of the scan, it moves to the position of
   the peak of the rocking curve.  This scan is useful after a large
   change of energy.

   You can put this scan in macro using::

     yield from rocking_curve()

**Slit height scan**
   This command::

     RE(slit_height())

   Runs a scan of the DM3 BCT motor around its current position.  At
   the end of the scan, you are prompted to click on the plot to
   choose a position to move the slit height to.  This scan is useful
   for verifying that the slits are in the correct orientation for
   the delivery of beam from the mirrors.


Area scans
----------

.. todo:: Bespoke area scan plan based on ``rel_grid_scan()`` with
	  logging, plucking, etc.

