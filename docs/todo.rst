..
   This document was developed primarily by a NIST employee. Pursuant
   to title 17 United States Code Section 105, works of NIST employees
   are not subject to copyright protection in the United States. Thus
   this repository may not be licensed under the same terms as Bluesky
   itself.

   See the LICENSE file for details.

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
#. Flesh out documentation on using automation + spreadsheets
#. Explain contents of dossier more fully
#. Current batch of cameras
#. Document using the Xspress3


This is an aggregate list of things mentioned in this document that
the BMM data collection system needs to do.

#. :strike:`Better sanity checking on linescan input`
#. Better sanity checking on areascan input, better interaction with area scan
#. :strike:`Have database consume snapshots`
#. :strike:`Mode C lookup table`
#. Lookup table for E < 8 keV at goniometer
#. :strike:`Look up E0 from element & edge`, use E0 to specify a non-edge energy
#. :strike:`Better sanitizing of INI file input`
#. :strike:`Better heuristics for scan time remaining`


How to add a scan.ini parameter
-------------------------------

#. Add its entry into ``scan_metadata()`` in :file:`BMM/energyscan.py`
#. Add its default value to the ``BMM_configuration``  class in :file:`BMM/modes.py`
#. Add it to ``html_dict`` in :file:`BMM/energyscan.py` around line 912
#. Correspondingly, add to the call arguments of
   ``scan_sequence_static_html()`` in :file:`BMM/energyscan.py`
#. make corresponding entries in the various automation spreadsheets

and, of course, use the new parameter in whatever way it needs to be used.

