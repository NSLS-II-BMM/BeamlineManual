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

    RE(linescan('it', 'x', -4, 4, 81))

The arguments are:

#. A string indicating the detector for the plotted signal.  The
   choices are:

   * ``it``: display the ratio of ``It/I0``
   * ``if``: display the sum of four silicon drift channels normalized by ``I0`` 
   * ``i0``: display the signal on ``I0``
   * ``ir``: display the ratio of ``Ir/I0``
   * ``both``: display both ``It/I0`` *and* the sum of four silicon drift channels normalized by ``I0`` 

#. The motor axis to be scanned.  This can be either the motor's
   BlueSky name or the nickname string from :numref:`Table %s
   <xafs-stages>`.  So, these are equivalent::

     RE(linescan('it', 'x', -4, 4, 81))
     RE(linescan('it', xafs_x, -4, 4, 81))

   For a motor that does not have a nickname, you must use the ophyd
   object, as in::

     RE(linescan('i0', slits3_outboard, -1, 1, 21))

#. The starting position of the motor scan, relative to the current
   position.

#. The ending position of the motor scan, relative to the current
   position.

#. The number of steps in the scan.


At the end of the scan, you are prompted with the following question::

    Pluck motor position from the plot? [Yn]


If you answer :button:`y` then :button:`Enter`, or simply hit
:button:`Enter`, you will be prompted to single click the left mouse
button :mark:`leftclick,.` on the plot.  The motor that was scanned
will then move to the motor position you clicked on.

You can skip the "click for motor position" step by typing
:button:`n` and hitting :button:`Enter`.

.. todo:: Better sanity checking of input parameters


Plucking a point from a line scan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to repeat the action of clicking on a point and moving the
motor to the click-upon point, do::

  RE(pluck())

This will enable the left mouse :mark:`leftclick,.` click and
subsequent motion on the most recent plot.  The ``pluck()`` command
*only* works on the most recent plot.  You may not pluck from an older
plot that is still displayed on the screen.

Of course, an older plot remains active in the sense that you can pass
the cursor over the plot and read the mouse coordinates in the bottom,
left corner of the plot window.  You can find a point in this way,
then do a movement command line::

  RE(mv(xafs_y, 28.31))


Revisit a line scan
~~~~~~~~~~~~~~~~~~~

Retrieve data from the database using the database key or scan ID::

   ls2dat('/path/to/output.file', '<id>')

This writes from the database to an output file.  The output file is a
simple column data file without header or metadata.


The first argument is the name of the output data file.  The second
argument is either the scan's unique ID |nd| something like 
``42447313-46a5-42ef-bf8a-46fedc2c2bd1`` |nd| or the scan's transient
id number.  Both the unique and transient ids can be found in the
:numref:`dossier (Section %s) <dossier>`.



.. _special-linescans:

Specific line scans
-------------------

Some scan types are performed often enough and always with the same
arguments that they have special names.

**Rocking curve scan**
   This command::

     RE(rocking_curve())

   does a scan of the pitch of the second mono crystal and plots the
   signal on I0.  At the end of the scan, it moves to the position of
   the center of mass of the rocking curve.  This scan is useful after
   a large change of energy.  It also opens the slits to 3 mm in
   vertical size before starting the scan, then returns the slits to
   their original height after the scan.

   You can put this scan in a macro using::

     yield from rocking_curve()

**Slit height scan**
   This command::

     RE(slit_height())

   Runs a scan of the DM3 BCT motor around its current position.  At
   the end of the scan, you are prompted to left click
   :mark:`leftclick,.` on the plot to choose a position to move the
   slit height to.  This scan is useful for verifying that the slits
   are in the correct orientation for the delivery of beam from the
   mirrors.

   Optionally, the scan will move to the center of mass of the
   measurement, skipping the prompt and plot interaction::

     RE(slit_height(move=True))

   You can put this scan in a macro using::

     yield from slit_height()


Area scans
----------

An area scan is a simple scan of a two motor axes with an on-screen
heat map.  At BMM this sort of scan is typically done using the
``areascan()`` plan.  This is a wrapper around BlueSky's
`rel_grid_scan()
<https://nsls-ii.github.io/bluesky/generated/bluesky.plans.rel_grid_scan.html#bluesky.plans.rel_grid_scan>`_.
Because the sample stages at BMM do not have encoders, the area scan
is made by `retreading the direction
<http://nsls-ii.github.io/bluesky/tutorial.html#scan-multiple-motors-in-a-grid>`_
of the fast motor rather than snaking back and forth.

In BMM's ``areascan()`` plan, the scan is always a relative scan
around the current positions of both motors being scanned.  It works
like this::

    RE(areascan('it', '<slow_motor>', -4, 4, 81, '<fast_motor>', -2, 2, 41))

The arguments are:

#. The slow motor axis.  This can be either the motor's
   BlueSky name or the nickname in :numref:`Table %s <xafs-stages>`.  So,
   these are equivalent::

     RE(areascan('it', 'x', -4, 4, 81, 'y', -2, 2, 41))
     RE(areascan('it', xafs_x, -4, 4, 81, xafs_y, -2, 2, 41))
     RE(areascan('it', xafs_x, -4, 4, 81, 'y', -2, 2, 41))

   For a motor that does not have a nickname, you must use the BlueSky
   name, as in this very silly example::

     RE(areascan('it', slits3_outboard, -1, 1, 21, dcm_pitch, -2, 2, 41))

#. The starting position of the slow motor, relative to the current
   position.

#. The ending position of the slow motor, relative to the current
   position.

#. The number of steps to take on the slow motor.

#. The fast motor axis.  This can be either the motor's
   BlueSky name or the nickname in :numref:`Table %s <xafs-stages>`.

#. The starting position of the fast motor, relative to the current
   position.

#. The ending position of the fast motor, relative to the current
   position.

#. The number of steps to take on the fast motor.

#. The detector for the plotted signal.  The choices are ``it``,
   ``if``, and ``i0``.  For the ``it`` choice, the plot will display
   the ratio of It/I0.  Similarly for the ``if`` choice, the plot will
   display the sum of four silicon drift channels normalized by I0.
   For the ``i0`` choice, the signal on the I0 chamber will be plotted.

At the end of the scan, you are prompted with the following question::

    Pluck motor position from the plot? [Yn]

If you answer ``Y``, or simply hit return, you will be prompted to
single click the left mouse button :mark:`leftclick,.` on the plot.
Both motors will then move to the position you clicked on.

You can skip the "click for motor position" step by typing
``n`` and hitting return.

.. todo:: Better sanity checking of input parameters


Plucking a point from an area scan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to repeat the action of clicking on a point and moving the
motor to the click-upon point, do::

  RE(pluck())

This will enable the left mouse click :mark:`leftclick,.` and
subsequent motion on the most recent plot.  The ``pluck()`` command
*only* works on the most recent plot.  You may not pluck from an older
plot that is still displayed on the screen.

Of course, an older plot remains active in the sense that you can pass
the cursor over the plot and read the mouse coordinates in the bottom,
left corner of the plot window.  You can find a point in this way,
then do a movement command::

  RE(mv(xafs_x, 28.31, xafs_y, 113.97))



Revisit an area scan
~~~~~~~~~~~~~~~~~~~~

Retrieve data from the database using the database key or scan ID::

   as2dat('/path/to/output.file', '<id>')

This writes from the database to an output file.  The output file is a
simple column data file.  The format of this data file is columns with
datablocks (i.e. rows of constant value of the slow motor) separated by
blank lines.  This is a format that `works with Gnuplot
<http://gnuplot.sourceforge.net/docs_4.2/node331.html>`_ and other
plotting programs.

The first argument is the name of the output data file.  The second
argument is either the scan's unique ID |nd| something like 
``42447313-46a5-42ef-bf8a-46fedc2c2bd1`` |nd| or the scan's transient
id number.  Both the unique and transient ids can be found in the
:numref:`dossier (Section %s) <dossier>`.


