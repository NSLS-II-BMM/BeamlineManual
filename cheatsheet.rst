..
   This manual is copyright 2018 Bruce Ravel and released under
   The Creative Commons Attribution-ShareAlike License
   http://creativecommons.org/licenses/by-sa/3.0/

.. _cheatsheet:

Command cheatsheet
==================

This section provides a quick summary of the data acquisition commands
discussed in the previous sections.


Command summary
---------------

.. table:: Main BlueSky command for BMM
   :name:  command-list

   +------------------------------------------+--------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Shutter commands**                                                        |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``shb.open()`` / ``shb.close()``         |    Open / close the photon shutter                                       | 
   +------------------------------------------+--------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Mono tuning commands**                                                    |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``tu()`` / ``td()``                      |    Tune the mono 2nd  crystal                                            |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``TUNE_STEP=0.004``                      |    Tuning step size – 0.004 is good for Si(111), 0.002 for Si(311)       |
   +------------------------------------------+--------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Mono movement commands**                                                  |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``RE(mv(dcm.energy, <value>))``          |    Move TO an energy value                                               |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``RE(mvr(dcm.energy, <value>))``         |    Move BY an energy step                                                |
   +------------------------------------------+--------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Motor movement commands**                                                 |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``RE(mv(xafs_liny, <value>))``           |    Move motor TO a position                                              |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``RE(mvr(xafs_liny, <value>))``          |    Move motor BY an amount                                               |
   +------------------------------------------+--------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Where are things?**                                                       |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``%w dcm``                               |    where's the mono?                                                     |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``%w slits3``                            |    where are the slits?                                                  |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``%w m2``                                |    where's mirror 2?  (focusing)                                         |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``%w m3``                                |    where's mirror 3?  (flat, harmonic rejection)                         |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``%w xafs_table``                        |    where's the XAFS table?                                               |
   +------------------------------------------+--------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Change mono and mode**                                                    |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``RE(change_mode('X'))``                 |    set mirror mode, see table below                                      |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``RE(change_xtals('h11'))``              |    set monochromator, Si(111) or Si(311), h=1 or h=3                     |
   +------------------------------------------+--------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Mono and experiment setup**                                               |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``RE(rocking_curve())``                  |    optimize pitch of 2nd DCM crystal (moves automagically)               |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``RE(rocking_curve(detector='Bicron'))`` |    same, but for XRD mode                                                |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``RE(slit_height())``                    |    explore position of slits3 (then pluck to move dm3_bct)               |
   +------------------------------------------+--------------------------------------------------------------------------+
   | |mquad| |mquad| |mquad| |mquad| |mquad| **Get help**                                                                |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``%m``                                   |    Show motors                                                           |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``%h``                                   |    Show help                                                             |
   +------------------------------------------+--------------------------------------------------------------------------+
   | ``%k``                                   |    Show keyboard shortcuts                                               |
   +------------------------------------------+--------------------------------------------------------------------------+



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
  ``slits3.vsize`` (nominally 1.4 mm)

Vertical center
  ``slits3.vcenter`` (nominally 0 mm)

  The vertical center is normally not changed.  Instead, align the
  slits using ``dm3_bct`` and the ``slit_height()`` plan


Motor positions and limits
--------------------------

Where is a sample motor?
   ``%w xafs_x``

What are the soft limits?
   ``xafs_x.hlm.value`` / ``xafs_x.llm.value``

Set a soft limit: 
   ``xafs_x.hlm.put(-95)`` / ``xafs_x.llm.put(-157)``


Line scans
----------

.. code-block:: text

   RE(linescan(<detector>, <motor>, <start>, <stop>, <N>))

where

+ ``<detector>`` is one of: ``'it'``, ``'if'``, or ``'i0'``
+ ``<motor>`` is one of: ``'x'``, ``'y'``, ``'pitch'``, ``'wheel'``,
  or a motor name
+ ``<start>``, ``<stop>``, ``<N>`` are the boundaries relative to the
  current position and the number of steps.

The plot will be determined from the values of ``<motor>`` and ``<detector>``

This is a relative scan.

After prompt, single click the left button  after a linescan to move to a position.

.. code-block:: text

   RE(pluck()) 

to repeat that on the current plot.  ``RE(pluck())`` only works on *most recent* plot.


Energy scans
------------

.. code-block:: text

   RE(xafs('myscan.ini'))

In the INI file, set ``mode`` to transmission, fluorescence,
reference, or both to control the in-scan plotting display (both =
show transmission and fluorescence)

Experiment log
--------------

Log entries are made for each scan.  System and beamtime specific logs
are maintained.  To insert a comment in the log, do:

.. code-block:: text

   BMM_log_info(“This is my log entry”)
