..
   This manual is copyright 2018 Bruce Ravel and released under
   The Creative Commons Attribution-ShareAlike License
   http://creativecommons.org/licenses/by-sa/3.0/

.. role:: strike
    :class: strike

.. _todo_list:

To Do List
==========

This is an aggregate list of things missing from the BMM beamline
documentation manual.

#. :strike:`Document change_edge()`
#. :strike:`Document pseudo channel cut & fixed exit DCM modes`
#. Document use of ``XDI_record`` to control what motors get recorded
   in the XDI header


This is an aggregate list of things mentioned in this document that
the BMM data collection system needs to do.

#. Better sanity checking on linescan input
#. Better sanity checking on areascan input
#. Have database consume snapshots
#. :strike:`Mode C lookup table`
#. Lookup table for E < 8 keV at goniometer
#. Look up E0 from element & edge, use E0 to specify a non-edge energy
#. :strike:`Better sanitizing of INI file input`
#. Better heuristics for scan time remaining


Add a scan.ini parameter
------------------------

#. Add its entry into ``scan_metadata()`` in ``84-energyscan.py``
#. Add its default value to the ``BMM_configuration``  class in ``74-modes.py``
#. Add it to ``html_dict`` in ``84-energyscan.py`` around line 912
#. Correspondingly, add to the call arguments of
   ``scan_sequence_static_html()`` in ``84-energyscan.py``

and, of course, use the new parameter in whatever way it needs to be used.

