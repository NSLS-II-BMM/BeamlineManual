..
   This document was developed primarily by a NIST employee. Pursuant
   to title 17 United States Code Section 105, works of NIST employees
   are not subject to copyright protection in the United States. Thus
   this repository may not be licensed under the same terms as Bluesky
   itself.

   See the LICENSE file for details.

Photo Galleries
===============

Harmonic Rejection Mirror
-------------------------

The HRM at BMM is a bounce-down mirror.  The light enters as indicated
by the yellow arrow.  The beam coming from the collimating mirror and
mono is inclined upward.  In :numref:`mode D (high energy,
non-focusing) (Section %s) <photon_delivery_modes>`, the HRM makes the
beam approximately level with the floor.


.. subfigure::  ABC
   :layout-sm: ABC
   :gap: 8px
   :subcaptions: above
   :name: fig-hrm
   :class-grid: outline

   .. image:: _images/HRM1.jpg

   .. image:: _images/HRM_top.jpg

   .. image:: _images/HRM_bottom.jpg

   (Left) The HRM with the vacuum vessel removed.  (Middle) The top of
   the silicon block of the mirror.  This is the **non-reflecting**
   side.  (Right) The reflecting surface of the mirror.  Note the
   differently colored stripes. The bare silicon is the darker stripe
   on the left.  The Pt/Rh is the brighter stripe on the right.


Hoisting
--------

Here are some notes on heavy things get hoisted at BMM.

.. _fig-hoist-cryo:
.. figure:: _images/Hoist_cryostat.jpg
   :target: _images/Hoist_cryostat.jpg
   :width: 70%
   :align: center

   4 foot strap with buckles through the rings on the cyrostat. 


.. subfigure::  AB
   :layout-sm: AB
   :gap: 8px
   :subcaptions: above
   :name: fig-hoist-m3
   :class-grid: outline

   .. image:: _images/Hoist_m3.jpg

   .. image:: _images/Strap_length_m3.jpg

   Two 5-foot straps + rotating rings at the mount points. 


DM3 BCT Failure
---------------

May 5, 2023: Failure of the DM3_BCT axis

**Symptoms**: BCT could not be moved from CSS or bsui. Immediate encoder
loss. No motion.

After several times restarting the IOC and one power cycle of the
motor controller, I finally thought to take a look at the physical
device. This is what I found.

.. subfigure::  ABC
   :layout-sm: ABC
   :gap: 8px
   :subcaptions: above
   :name: fig-bct
   :class-grid: outline

   .. image:: _images/BCT3.jpg

   .. image:: _images/BCT2.jpg

   .. image:: _images/BCT1.jpg

   The threaded rod had slipped free of the coupler connecting it to
   the DM3 BCT motor.  Once uncoupled, it wound it's way through the
   carriages all the way down, finally coming to rest on the base of
   DM3.


**Solution**: Rethread lead screw through upper carriage. Reinsert
into coupler. Tighten coupler.
