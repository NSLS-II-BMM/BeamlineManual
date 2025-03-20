
..
   This document was developed primarily by a NIST employee. Pursuant
   to title 17 United States Code Section 105, works of NIST employees
   are not subject to copyright protection in the United States. Thus
   this repository may not be licensed under the same terms as Bluesky
   itself.

   See the LICENSE file for details.


.. _other_measurements:

Other measurement needs
=======================

.. attention:: Unfinished section

SEAD
----

Single energy absorption detection

Term coined in `a paper by Filipponi et al. <https://doi.org/10.1088/0953-8984/10/1/026>`__


explain INI file, plotting, dossier


Raster
------

Single ROI area scans.  A map of sorts.

explain INI file, plotting, dossier


Wafers
------

There is some functionality specifically for measuring films grown on
large, round wafers.  The basic experiment involves measuring XAS of 1
or more edges from selected positions on a film.  BMM has sample
holders specifically designed for holding standard size silica or
crystalline wafers.

Most such experiments involve reliable motion to specific locations on
the film.  This usually starts with finding the center of the wafer
and indexing locations relative to the center.

The method for finding the center involves finding the X,Y coordinates
of three points around the periphery of the wafer, then using
`geometry <https://docs.sympy.org/latest/modules/geometry/index.html>`__
to find the `center of the circle
<https://docs.sympy.org/latest/modules/geometry/polygons.html#sympy.geometry.polygon.Triangle.circumcenter>`__
intersecting those three points.

``RE(wafer.edge())`` 
    With the focused beam in the vicinity of a point on the edge of
    the wafer, make a scan in ``xafs_x``, plotting the signal on I\
    :sub:`t`, to find the X,Y coordinates of a point in the edge.
    This method will execute the :numref:`linescan (Section %s)
    <linescan>`, fit a lineshape to the measurement, then move to the
    position of the wafer's edge.
    This must be repeated three times on three widely spaced
    points.

``wafer.push()``
    After finding a point using ``RE(wafer.edge())``, push the current
    X,Y coordinates to a list.  After three measurements of the wafer
    edge, this list will contain the three X,Y
    coordinates of edge points.

``wafer.points``
    The list containing the three edge points.

``wafer.find_center()``
    Compute the wafer center from the contents of ``wafer.points``.

``RE(wafer.goto.center())``
    Move the ``xafs_x`` and ``xafs_y`` stages to the center position.

``wafer.center``
    The center position of the wafer.

``wafer.clear()``
    Clear the contents of ``wafer.points`` in order to start over.

