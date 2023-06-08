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

#. Document use of ``XDI_record`` to control what motors get recorded
   in the XDI header
#. Flesh out documentation on using automation + spreadsheets
#. Explain contents of dossier more fully
#. Current batch of cameras
#. Document using the Xspress3
#. Better abstraction of spreadsheet-to-macro components, less cargo-cult code
#. How redis is used at the BL


This is an aggregate list of things mentioned in this document that
the BMM data collection system needs to do.

#. Mode C lookup table
#. Lookup table for E < 8 keV at goniometer


How to add a scan.ini parameter
-------------------------------

#. Add its entry into ``scan_metadata()`` in :file:`BMM/energyscan.py`
#. Add its default value to the ``BMM_configuration``  class in :file:`BMM/modes.py`
#. Add it to ``html_dict`` in :file:`BMM/energyscan.py` around line 912
#. Correspondingly, add to the call arguments of
   ``scan_sequence_static_html()`` in :file:`BMM/energyscan.py`
#. make corresponding entries in the various automation spreadsheets

and, of course, use the new parameter in whatever way it needs to be used.

