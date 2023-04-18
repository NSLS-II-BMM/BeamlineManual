..
   This document was developed primarily by a NIST employee. Pursuant
   to title 17 United States Code Section 105, works of NIST employees
   are not subject to copyright protection in the United States. Thus
   this repository may not be licensed under the same terms as Bluesky
   itself.

   See the LICENSE file for details.

.. role:: key
    :class: key

.. _cheatsheet:

Command cheatsheet
==================

This section provides a quick summary of the data acquisition commands
discussed in the previous sections.

.. admonition:: Stopping a measurement

   To stop any command do :key:`Ctrl`-:key:`C` :key:`Ctrl`-:key:`C`

   That is, hit :key:`Ctrl`-:key:`C` twice!

   This will **pause** the running command and return you to the command line.

   Do ``RE.resume()`` to continue the command from where it stopped.

   Do ``RE.stop()`` to fully stop the command.


Command summary
---------------

Note that some command must be run through the run engine, other do
not.  The use of ``RE()`` is called explicitly in :numref:`Table %s
<command-list>`.  Any command that should be run through the run
engine will complain with this hint:

.. code-block:: text

   BMM D.111 [48] > mvr(xafs_x, 2)
   Out[48] <generator object mvr 0x7fefafd1df50>   Hint: enclose bsui commands in RE()



.. table:: Main BlueSky commands used at BMM (don't type the ``<`` or
	   ``>``, those symbols indicate that the argument is numeric.)
   :name:  command-list
   :align: left

   +------------------------------------------+----------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Shutter commands**                                                          |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``shb.open()`` / ``shb.close()``         |    Open / close the photon shutter                                         | 
   +------------------------------------------+----------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Mono tuning commands**                                                      |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(rocking_curve())``                  |    Measure the 2nd crystal rocking curve                                   |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``tu()`` / ``td()``                      |    Tune the mono 2nd crystal by hand                                       |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``TUNE_STEP=0.004``                      |    Tuning step size – 0.004 is good for Si(111), 0.002 for Si(311)         |
   +------------------------------------------+----------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Import an automation spreadsheet**                                          |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``xlsx()``                               |    Select an existing spreadsheet from a list                              |
   +------------------------------------------+----------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Mono movement commands**                                                    |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(mv(dcm.energy, <value>))``          |    Move TO an energy value                                                 |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(mv(dcm.energy, <e0value> + 50))``   |    Move 50 eV **above** the edge                                           |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(mv(dcm.energy, <e0value> - 50))``   |    Move 50 eV **below** the edge                                           |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(mvr(dcm.energy, <value>))``         |    Move BY an energy step                                                  |
   +------------------------------------------+----------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Motor movement commands**                                                   |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(mv(xafs_liny, <value>))``           |    Move any named motor TO a position (``xafs_y`` is an example)           |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(mvr(xafs_liny, <value>))``          |    Move any named motor BY an amount (``xafs_y`` is an example)            |
   +------------------------------------------+----------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Where are things?**                                                         |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``%w dcm``                               |    where's the mono?                                                       |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``%w slits3``                            |    where are the slits?                                                    |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``%w m2``                                |    where's mirror 2?  (toroidal focusing mirror)                           |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``%w m3``                                |    where's mirror 3?  (flat, harmonic rejection mirror)                    |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``%w xafs_table``                        |    where's the XAFS table?                                                 |
   +------------------------------------------+----------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Change edge and mono crystal**                                              |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(change_edge('Xx'))``                |    setup beamline for an absorption edge, 1- or 2-letter symbol            |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(change_xtals('h11'))``              |    set monochromator, Si(111) or Si(311), h=1 or h=3                       |
   +------------------------------------------+----------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Experiment setup**                                                          |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(slit_height())``                    |    explore position of slits3 (then pluck to move dm3_bct)                 |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(dark_current())``                   |    measure electrometer dark currents                                      |
   +------------------------------------------+----------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **ex situ sample stage**                                                      |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(slot(<N>))``                        |    Move sample wheel to slot #N (1 |le| N |le| 24)                         |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(find_slot())``                      |    align the *ex situ* wheel sample holder                                 |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(xafs_wheel.outer())``               |    move the *ex situ* wheel sample holder to the outer ring                |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(xafs_wheel.inner())``               |    move the *ex situ* wheel sample holder to the inner ring                |
   +------------------------------------------+----------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Glancing angle stage**                                                      |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(ga.to(N))``                         |    move glancing angle stage to sample N (1 |le| N |le| 8) + start spinner |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(ga.auto_align(pitch))``             |    automatically align glancing angle stage and move to pitch              |
   +------------------------------------------+----------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Linkam stage**                                                              |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(mv(linkam, T))``                    |    move Linkam stage to temperature T                                      |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``linkam.settle_time = 120``             |    set Linkam settling time (in seconds)                                   |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``linkam.status()``                      |    display Linkam status                                                   |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``linkam.on()`` / ``linkam.off()``       |    turn Linkam on or off                                                   |
   +------------------------------------------+----------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **LakeShore temperature controller**                                          |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(lakeshore.to(T, power))``           |    move cryostat to temperature T with heater at ``power``                 |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``lakeshore.settle_time = 120``          |    set Linkam settling time (in seconds)                                   |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``lakeshore.status()``                   |    display Linkam status                                                   |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(mv(lakeshore.power,3))``            |    turn heater to full power                                               |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(mv(lakeshore.power,0))``            |    turn heater off                                                         |
   +------------------------------------------+----------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Reference wheel**                                                           |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``RE(reference('Xx'))``                  |    Move to reference 'Xx'                                                  |
   +------------------------------------------+----------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Get help**                                                                  |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``%m``                                   |    Show motors                                                             |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``%h``                                   |    Show help                                                               |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``%k``                                   |    Show keyboard shortcuts                                                 |
   +------------------------------------------+----------------------------------------------------------------------------+
   | ``%se``                                  |    Show reference foil and ROI configurations                              |
   +------------------------------------------+----------------------------------------------------------------------------+



Photon delivery system modes
----------------------------

.. table:: Photon delivery system modes
   :name:  pds-mode-table

   =======  =============  =================
    Mode     focused        energy range
   =======  =============  =================
    A        |checkmark|    8 keV and up
    B        |checkmark|    below 6 keV
    C        |checkmark|    6 keV to 8 keV
    D        |xmark|        8 keV and up
    E        |xmark|        6 keV to 8 keV
    F        |xmark|        below 6 keV
    XRD      |checkmark|    8 keV and up
   =======  =============  =================


Slits3 coordinated motions
--------------------------

These coordinated motions behave just like single motors and can be
used with the motor movement commands in :numref:`Table %s <command-list>`.

Horizontal size
  ``slits3.hsize`` (nominally 8 mm)	

Horizontal center
  ``slits3.hcenter`` (nominally 0 mm)


Vertical size
  ``slits3.vsize`` (nominally 1 mm)

Vertical center
  ``slits3.vcenter`` (nominally 0 mm)

  The vertical center should never be changed.  Instead, align the
  slits using ``dm3_bct`` and the ``slit_height()`` plan
  (:numref:`Section %s <special-linescans>`)



Example movement: ``RE(mv(slits3.vsize, 0.5))``

Individual slits are named ``slits3.top``, ``slits3.bottom``,
``slits3.inboard``, ``slits3.outboard``.


Motor positions and limits
--------------------------

These commands work on any named motor (:numref:`Table %s <motor-list>`).

Where is a sample motor?
   ``%w xafs_x``

What are the soft limits?
   ``xafs_x.hlm.value`` / ``xafs_x.llm.value``

Set a soft limit: 
   ``xafs_x.hlm.put(-95)`` / ``xafs_x.llm.put(-157)``


Line scans
----------

.. code-block:: python

   RE(linescan(<detector>, <motor>, <start>, <stop>, <N>))

where

+ ``<detector>`` is one of: ``'it'``, ``'if'``, ``'ir'``, or ``'i0'``
+ ``<motor>`` is one of: ``'x'``, ``'y'``, ``'pitch'``, ``'wheel'``,
  or a named motor (:numref:`Table %s <motor-list>`)
+ ``<start>``, ``<stop>``, ``<N>`` are the boundaries relative to the
  current position and the number of steps.

The plot will be determined from the values of ``<motor>`` and
``<detector>``

This is a relative scan.

After prompt, single click the left button after a linescan to move to
a position.

.. code-block:: python

   RE(pluck()) 

to repeat that on the current plot.  ``RE(pluck())`` only works on the
*most recent* plot.


Energy scans
------------

Start an XAFS scan, prompting for an :numref:`INI file (section %s) <ini>` 

.. code-block:: python

   RE(xafs())

Start an XAFS scan using a specified :numref:`INI file (section %s) <ini>` 

.. code-block:: python

   RE(xafs('myscan.ini'))

In the INI file, set ``mode`` to transmission, fluorescence,
reference, or both to control the in-scan plotting display (both =
show transmission and fluorescence)

Import a spreadsheet to perform automated XAFS measurements:

.. code-block:: python

   xlsx()

You will be prompted first for the name of a spreadsheet file, then
for the tab to be read.

..
  Experiment log
  --------------

  Log entries are made for each scan.  System and beamtime specific logs
  are maintained.  To insert a comment in the log, do:

  .. code-block:: text

     BMM_log_info(“This is my log entry”)

Common user motors
------------------

.. table:: Main motors BMM users will interact with
   :name:  motor-list
   :align: left

   +----------------------+--------------------------------------------------------------------------+
   | ``xafs_x``           |    X sample stage (+ inboard / - outboard)                               |
   +----------------------+--------------------------------------------------------------------------+
   | ``xafs_y``           |    Y sample stage (+ up / - down)                                        |
   +----------------------+--------------------------------------------------------------------------+
   | ``xafs_det``         |    detector stage (+ out / - in)                                         |
   +----------------------+--------------------------------------------------------------------------+
   | ``xafs_pitch``       |    sample pitch (Rx)                                                     |
   +----------------------+--------------------------------------------------------------------------+
   | ``xafs_roll``        |    sample roll (Rz)                                                      |
   +----------------------+--------------------------------------------------------------------------+
   | ``xafs_wheel``       |    sample wheel (+ higher slot number, 15 degrees apart)                 |
   +----------------------+--------------------------------------------------------------------------+
   | ``xafs_ref``         |    reference wheel (+ higher slot number, 15 degrees apart)              |
   +----------------------+--------------------------------------------------------------------------+
   | ``xafs_garot``       |    glancing angle rotation wheel                                         |
   +----------------------+--------------------------------------------------------------------------+
   | ``dm3_bct``          |    slit assembly height (+ up / - down) (normally use ``slit_height()``) |
   +----------------------+--------------------------------------------------------------------------+
   | ``slits3.vsize``     |    vertical slit size                                                    |
   +----------------------+--------------------------------------------------------------------------+
   | ``slits3.vcenter``   |    horizontal slit size                                                  |
   +----------------------+--------------------------------------------------------------------------+
