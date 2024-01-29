..
   This document was developed primarily by a NIST employee. Pursuant
   to title 17 United States Code Section 105, works of NIST employees
   are not subject to copyright protection in the United States. Thus
   this repository may not be licensed under the same terms as Bluesky
   itself.

   See the LICENSE file for details.

.. _details:

Instrumentation Details
=======================

This section is a scattershot assortment of details about things at
the beamline.  This is basically an attempt to capture institutional
knowledge ... someplace.

BNC Cable Map
-------------

Here is an explanation of the BNC and SHV patch panels going between
rack D at the control station, Rack C on the roof of the hutch, and
the in-hutch patch panel.


.. _fig-bncpatch:
.. figure:: _images/Bnc_map.png
   :target: _images/Bnc_map.png
   :width: 100%
   :align: center

Inert Gas Plumbing
------------------

Needle valves are mounted on the outboard side of DM3. Quick connect
outlets for the gases are mounted on the upstream/inboard corner of
the XAFS table.  

.. _fig-inertgas:
.. figure:: _images/Gas_handling.png
   :target: _images/Gas_handling.png
   :width: 100%
   :align: center

Vendor link for quick-disconnect fixture: https://www.mcmaster.com/5012K122/


   
Analog Video Capture
--------------------

Implementing `this USB video adapter
<https://www.amazon.com/REDGO-Video-Capture-Converter-Adapter/dp/B01E5ITE2W>`__
to capture video from the small analog cameras in the hutch took a bit
of doing.

First, the adapter must be plugged directly into the computer.  Using
a USB hub makes for an unreliable interface to the camera.

Second, the file ``/etc/udev/rules.d/99-usb-camera-capture.rules`` is
needed to set permissions on ``/dev/video0`` correctly when the adapter is
plugged in.

.. code-block:: none

   ACTION!="add|change", GOTO="webcam_capture_end"
   SUBSYSTEM=="usb", ATTRS{idVendor}=="534d", ATTRS{idProduct}=="0021", MODE="0666"
   KERNEL=="video*", ATTRS{idVendor}=="534d", ATTRS{idProduct}=="0021", GROUP="video", MODE="0666"
   KERNEL=="video*", ATTRS{idVendor}=="534d", ATTRS{idProduct}=="0021", ATTRS{avoid_reset_quirk}=1
   KERNEL=="video*", ATTRS{idVendor}=="534d", ATTRS{idProduct}=="0021", ATTRS{quirks}=0x100
   LABEL="webcam_capture_end"

Putting this file in place will require assistance from DSSI. Beamline
staff do not have permission to make a file in that folder. See `this
Jira ticket <https://jira.nsls2.bnl.gov/browse/HXSS-779>`__ for an
example of what to ask for.

This recognizes the vendor and product IDs of the specific adapter
that I bought.  When inserted, it sets the device to RW for all users
and sets a couple of possibly relevant attributes.  (This udev rules
file was adapted from the rules file that comes with the easycap dc60
package – info and links `here
<http://easycap.blogspot.com/p/easycap-dc60.html>`__).

Next a small function was written as a wrapper around `fswebcam
<https://github.com/fsphil/fswebcam>`__ to grab frames from the
camera. The function is basically a wrapper around a call to
``fswebcam`` like so:

.. code-block:: sh

   fswebcam -d /dev/video0 -r 640x480 -S 30 -F 5 foo.jpg

along with some image processing using python's ``wand`` package. 

Required packages:

+ ``fswebcam``
+ ``python-wand``
+ ``imagemagick``

This whole setup is filled with quirk.  There is a delay accessing the
video capture.  The ``-S`` switch builds in a 1 second delay, giving the
capture device enough time to begin displaying the image.  The ``-F``
switch tells the script how many frames to accumulate for good signal.
5 is probably overkill.

In any case, it is now possible to grab screen shots of the currently
displayed analog video while collecting data.

All of this is implemented in ``BMM/camera_device.py`` for use in
Bluesky. The heart of the implementation is a system call to
``fswebcam``. From there, the image is saved as an asset and correctly
pointed to in databroker.  See:

+ https://github.com/NSLS-II-BMM/profile_collection/blob/master/startup/BMM/user_ns/detectors.py#L253
+ https://github.com/NSLS-II-BMM/profile_collection/blob/master/startup/BMM/camera_device.py#L62-L164


DI Water Flow
-------------

The DI water is controled by manual valves, which should only be
operated by the utilities group, and by solenoid valves in the FOE.
The solenoid valves are triggered by a water-sensing strip along the
floor of the FOE. They are also actuated by switches on the CSS
utilities screen. These toggles are the ones circled in pink inthe
screenshot on the left. 

The valves themselves are the large yellow and black boxes mounted
high on the back wall of the FOE.  The valve indicators are the rods
with orange markings.  When the valves are open, the orange marks are
facing downstream.  When closed, the orange marks are rotated towards
the wall.  Opening and closing those valves is managed through CSS.
They must be open for the utilities group to do their work on the DI
delivery to the mono and the filter assemblies.  

.. subfigure::  ABC
   :layout-sm: ABC
   :gap: 8px
   :subcaptions: above
   :name: fig-diwater
   :class-grid: outline

   .. image:: _images/Water_flow_CSS.png

   .. image:: _images/Water_flow_valves_1.jpg

   .. image:: _images/Water_flow_valves_2.jpg

   (Left) The CSS utilities screen where the water valve controls are
   found.  (Middle) A view into the FOE.  (Right) The inboard wall
   where the physical valve is found.

Disabling an MCS8 axis after a move
-----------------------------------

From Adam Young at FMBO
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: none

   The motors can be disabled after a movement and this can be set at the
   Delta Tau level.

   First you will need to connect to each MCS8+ with the beamline laptop
   and start PEWin.

   Then please do the following:

   + Click on the 'View' menu at the top of the window. Then click
     'Program/PLC Status (and upload)'. 
   + Select PLC1 and click 'Upload'. An editor showing PLC1 will appear.
   + Scroll down to find the variables P105 to P805. The '1' to '8' part
     of these variables represent axis 1 to 8 on the MCS8+. The value of
     these variables determines whether or not the motors will be
     disabled after a move. They are likely all set to '0' meaning power
     stays on. The lateral motors are on axis 4 and 5 so P405 and P505
     should be set to '1'.
   + Click on the yellow downwards pointing arrow on the toolbar in the
     editor. This downloads the modified PLC1 from the editor to the
     Delta Tau. Close the editor. 
   + In the terminal window issue a 'save' to save the modified
     configuration to the Delta Tau non-volatile memory and issue '$$$'
     to refresh the controller. 

A follow up from Graeme Elliner, FMBO
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: none

   Just done a fast scan of the config file and I think it is probably
   because P302=1.

   Px02 and Px05 (where x is the motor number) are special Pvars for
   setting the final state of the motor once it has stopped moving, they
   are used in PLC1x and set as you know in PLC1

   If Px02=1 the PLC to check if the motor is in position and its
   desired velocity is zero, if these two conditions are set a Flag is
   set, If the conditions are still met 1second later then the motor
   is put into OPEN LOOP. This means the motor is still enabled but
   will ignore the encoder and the motor will hold its current rotary
   location. This is useful for the motors that have DPTs pushing
   against them in flexures (trapezoidal roll and pitch assy on the
   DCMs), it gives a firm base for the DPT to push against but will
   not try to hold position (as it would in closed loop) when the DPT
   pushes the top part of the stage and moves the encoder.  If Px05=1
   then the PLC checks to see if the motor is in position and has zero
   velocity, then 1second later it will kill that motor

   Due to the way the code is ordered (it looks for thePx02 first) it
   will enter Px02 check first, when the conditions are met it will
   set the first Flag After that check it then see the Px05 check and
   kills the motor. However on the next pass through the PLC it will
   again enter the Px02 check, see that the first flag has been set
   then trigger the open loop command, re-enabling the motor.

   Hence by setting P302=0 in PLC1, it will not go into the check and
   not accidentally enable the motor.  If this does not fix it then
   the issue is in EPICS

Conclusion
~~~~~~~~~~

The above suggestions were done for ``dm3_bct``, a motor that was
showing the re-enable behavior.  This made that motor tricky to
operate in bluesky. Setting ``P302=0`` and ``P305=1`` did the trick.


Vortex pressure
---------------

Using a probe to measure the voltage on the IP port of the Vortex ME4.
This reading will tell you the internal pressure according to the
table in the snapshot below.  

.. _fig-votexpressure:
.. figure:: _images/Vortex_pressure.jpeg
   :target: _images/Vortex_pressure.jpeg
   :width: 40%
   :align: center


======================  ==========
 IP reading (Voltage)    Pressure
======================  ==========
 -0.01                   5E-9
 -0.1                    5E-8
 -1                      5E-7
 -10                     5E-6 
======================  ==========


Temperature reading should be 1.5 V when the TEC is at proper
temperature. 

`Vortex SDD manual
<https://www.aps.anl.gov/files/download/DET/Detector-Pool/Spectroscopic-Detectors/Vortex_SDD/Vortex_ME4/Vtx-ME4%20Multi-El%20User%20Manual%20Rev.4.pdf>`__
(link to copy at APS detector pool).

DM3 CAT6 Patch Panel
--------------------

13 more CAT6 ports for use in the hutch. Note that ports listed as
SCI/EPICS are tagged ports on both subnets.

This is needed by workstations (like ``xf06bm-ws5``), display machines
running CSS (like ``xf06bm-disp1``), and machines running IOCs (like
``xf06bm-xspress3``).

Note that ``xf06bm-em1`` needs to be on an INST port while the ion
chambers are on EPICS ports. The difference is that the ion chambers
are running their own on-board IOCs, making them more like IOC servers
than instruments.




+-----------+----------+--------------------+----------------+---------------------+-------------------+
| **Patch** | **Port** |  **xf06bm-a port** |  **Network**   |  **Role**           |  **Cable number** |
+-----------+----------+--------------------+----------------+---------------------+-------------------+
| **DM3-A** |  1       |  44                |  EPICS         |  xf06bm-ic1         |  200235           |
+-----------+----------+--------------------+----------------+---------------------+-------------------+
|           |  2       |  45                |  EPICS         |  xf06bm-ic2         |  200236           |
+-----------+----------+--------------------+----------------+---------------------+-------------------+
|           |  3       |  46                |  EPICS         |  xf06bm-ic3         |  200237           |
+-----------+----------+--------------------+----------------+---------------------+-------------------+
|           |  4       |  06bm-agg 36       |  INST          |  xf06bm-em1         |  200238           |
+-----------+----------+--------------------+----------------+---------------------+-------------------+
| **DM3-B** |  1       |  17                |  SCI/EPICS     |  xf06bm-ws5         |  200239           |
+-----------+----------+--------------------+----------------+---------------------+-------------------+
|           |  2       |  18                |  SCI/EPICS     |  xf06bm-disp1       |  200240           |
+-----------+----------+--------------------+----------------+---------------------+-------------------+
|           |  3       |  19                |  SCI/EPICS     |  xf06bm-xspress3    |  200241           |
+-----------+----------+--------------------+----------------+---------------------+-------------------+
|           |  4       |                    |  SCI/EPICS     |                     |  200242           |
+-----------+----------+--------------------+----------------+---------------------+-------------------+
| **DM3-C** |  1       |                    |                |                     |  200243           |
+-----------+----------+--------------------+----------------+---------------------+-------------------+
|           |  2       |                    |                |                     |  200244           |
+-----------+----------+--------------------+----------------+---------------------+-------------------+
|           |  3       |                    |                |                     |  200245           |
+-----------+----------+--------------------+----------------+---------------------+-------------------+
|           |  4       |                    |                |                     |  200246           |
+-----------+----------+--------------------+----------------+---------------------+-------------------+
| **DM3-D** |  1       |                    |                |                     |  200247           |
+-----------+----------+--------------------+----------------+---------------------+-------------------+
|           |  2       |                    |                |  unused             |                   |
+-----------+----------+--------------------+----------------+---------------------+-------------------+
|           |  3       |                    |                |  unused             |                   |
+-----------+----------+--------------------+----------------+---------------------+-------------------+
|           |  4       |                    |                |  unused             |                   |
+-----------+----------+--------------------+----------------+---------------------+-------------------+


Some photos of the patch panel:

.. subfigure::  AB
   :layout-sm: AB
   :gap: 8px
   :subcaptions: above
   :name: fig-dm3cat6
   :class-grid: outline

   .. image:: _images/DM3_patch_panel.jpg

   .. image:: _images/DM3_first_cat6.jpg

   (Left) CAT6 patch panel at DM3.  (Right) Lowest numbered label on
   the CAT6 cables in the DM3 patch panel


Logitech controller
-------------------

.. _fig-logitech:
.. figure:: _images/Logitech.png
   :target: _images/Logitech.png
   :width: 100%
   :align: center


.. todo::

   Explain how to configure buttons in CSS
