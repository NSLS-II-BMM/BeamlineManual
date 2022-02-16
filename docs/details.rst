..
   This manual is copyright 2018 Bruce Ravel and released under
   The Creative Commons Attribution-ShareAlike License
   http://creativecommons.org/licenses/by-sa/3.0/


Data collection software
========================

.. todo::

   Write me!

This section of the document dives deeply into the BlueSky startup
code used at BMM.  This is intended as a reference for someone digging
into the guts of the beamline.


.. _hierarchy-details:

BlueSky startup hierarchy
------------------------- 

#. Working towards cookie cutter:
   https://nsls-ii.github.io/scientific-python-cookiecutter/index.html
#. scripts imported into ipython namespace
#. `BMM/` folder contains most of the juice
#. `ML/` contains files associated with data evaluation, `telemetry/`
   contains files associated with telemetry approximations


.. _xafs-details:

The XAFS plan
-------------

Like many of the commands defined at BMM, the `xafs()` plan uses
BlueSky's `finalize_wrapper
<https://nsls-ii.github.io/bluesky/generated/bluesky.preprocessors.finalize_wrapper.html>`_
preprocessor.  This allows us to define sensible behavior for a scan
or scan sequence in the event of an interruption.

Upon starting and before invoking the finalize_wrapper preprocessor,
the `xafs()` plan defines a bunch of local symbols for symbols from
the main Ipython namespace.  Then:

.. sourcecode:: python
   :linenos:

   dotfile = '/home/xf06bm/Data/.xafs.scan.running'
   html_scan_list = ''
   html_dict = {}
   BMMuser.final_log_entry = True
   RE.msg_hook = None
   if inifile[-4:] != '.ini':
      inifile = inifile+'.ini'
   

At line 1, define a file that is used to interact with the
`cadashboard` tool that gets displayed at the top of the big monitor.

At lines 2 and 3, define some variables local to the full `xafs()`
plan such that they are available to main and final parts of the plan.

At lines 4 and 5, silence some logging functionality.

At lines 6 and 7, be sure that the argument to the `xafs()` plan, the
name of the INI file containing the measurement instructions has the
`.ini` suffix.

Now let's dig into the main plan.

The main plan
~~~~~~~~~~~~~

In sequence, here's what happens in the main plan.




The final plan 
~~~~~~~~~~~~~~
