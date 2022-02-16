..
   This manual is copyright 2018 Bruce Ravel and released under
   The Creative Commons Attribution-ShareAlike License
   http://creativecommons.org/licenses/by-sa/3.0/

.. _automation:

Beamline automation
===================

BMM currently supports four categories of spreadsheet-based automation:

#. Sample wheels, both single and double ring  
#. Linkam stage temperature control
#. Glancing angle stage
#. Generic XY grids

The latest spreadsheets for each of these can always be found at
https://wiki-nsls2.bnl.gov/beamline6BM/index.php/Automation_Spreadsheets


Each of the spreadsheets looks much like this, although there are some
differences in the columns corresponding to the different instruments.

.. _fig-wheel-spreadsheet:
.. figure::  _images/wheel_spreadsheet.png
   :target: _images/wheel_spreadsheet.png
   :width: 70%
   :align: center

   Example spreadsheet for running an experiment from a wheel with a
   single sample ring.



Common features
---------------

Default information
~~~~~~~~~~~~~~~~~~~

All the spreadsheets use the concept of "default" scan information,
that is, information that is expected to be used for most or all of the
indicated measurements.  In :numref:`Figure %s
<fig-wheel-spreadsheet>`, the defults are entered into the row with the
green background.  All rows underneath the green line are used to
describe individual measurements.

For an individual measurement, if a cell is left blank, the default
value will be used.  If a cell is filled in, that value will be used
for that measurement.

Experimenters
~~~~~~~~~~~~~

The other green part of the spreadsheet is a cell for entering the
names of all the experimenters involved in the measurement.

This should **always** be filled in.  Doing so allows for the
possibility of searching BMM's master database for data associated
with a particular user.

.. _spreadsheet_options:

Measurement options
~~~~~~~~~~~~~~~~~~~

Beneath the experimenter cell, there are three drop-down menus for
setting aspects of the sequence of measurements described on the
spreadsheet tab.

#. A yes/no menu for forcing Bluesky to run the ``change_edge()``
   command at the beginning of the measurement sequence.

#. A yes/no menu for telling Bluesky to close the shutter at the end
   of the measurement sequence.

#. A menu of options for modifying filenames to contain information
   about things like absorber element, edge symbol, LInkam stage
   temperature, and so on.  This simplifies data entry into the
   ``filename`` column of the spreadsheet.



Selecting an spreadsheet
~~~~~~~~~~~~~~~~~~~~~~~~

All spreadsheets are imported using the :file:`xlsx()` command.  The
spreadsheets are self-identifying.  Every spreadsheet has an
identifying string spanning cells B1:C1.  This is the cell with the
pink background.  **Never** change the text in that cell or you run
the risk of your spreadsheet being interpreted incorrectly.

To convert a spreadsheet into a macro then run the macro, do the
following:

.. sourcecode:: python

   xlsx()

This will show a numbered list of all :file:`.xlsx` files in your data
folder, something like this:

.. sourcecode:: text

  Select your xlsx file:

    1: 20210127-KB1.xlsx
    2: 20210127-KB3.xlsx
    3: 20210128-KB2.xlsx
    4: 20210128-KB4.xlsx
    5: 20210128-KB5.xlsx
    7: wheel_template.xlsx

    r: return

  Select a file > 

Select the :file:`.xlsx` file you want to import.  Based on the
content of the pink identifying cell, your spreadsheet will be
interpreted appropriately.

You may have multiple tabs in the spreadsheet file.  If the file you
selected from the menu shown above has multiple tabs, you will be
presented with a menu of tabs, something like this:

.. sourcecode:: text

  Select a sheet from yourfile.xlsx:

    1: tab1
    2: tab2
    3: tab3

    r: return

  Select a file > 

Enter the number corresponding to the tab to be measured.

The menu of tab selections will only be presented if there is more
than one tab in the spreadsheet file.

You may organize your experiment in a single file with multiple tabs
or in multiple files (each with one or more tabs).  That is enturely
up to you.

Generating Bluesky instructions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The tab on the selected spreadsheet file will be parsed, then a macro
file generated called :file:`<tab>_macro.py` and an INI file called
:file:`<tab>.ini`, where :file:`<tab>` is the name of the tab from
which the instructions were read.

It is, therefor, a very good idea to give your tabs names that
indicate something about the experiment being described on that tab.

The INI file contains the default values from the green line (see
:numref:`Figure %s <fig-wheel-spreadsheet>`).  The macro file is
imported into the BlueSky session, providing a new with the name of
the spreadsheet file.  If the tab in the spreadsheet was called
:file:`mysamples.xlsx`, the new BlueSky command is called
``mysemaples_macro()``.



Sample wheel automation
-----------------------

The standard ex-situ sample holder at BMM is a plastic wheel that get
mounted on a rotation stage.  Examples are shown in figures
:numref:`fig-samplewheel` and :numref:`fig-doublewheel`.  The rotation
stage is mounted on an XY stage, so when one slot on the sample wheel
is aligned, all the slots are aligned.

.. subfigstart::

.. _fig-samplewheel:
.. figure::  _images/Samplewheel.jpg
   :target: _images/Samplewheel.png
   :width: 100%
   :align: center

   A single-ring sample wheel with 24 sample positions.  There are
   options with 13mm x 3 mm slots or 13mm diameter holes.

.. _fig-doublewheel:
.. figure::  _images/double_wheel_sm.jpg
   :target: _images/double_wheel_sm.png
   :width: 100%
   :align: center

   Double-ring sample wheels with 48 sample positions.  There are
   options with 13mm x 3 mm slots or 13mm diameter holes.

.. subfigend::
   :width: 0.45
   :label: _fig-normalization

The automation concept is that each slot on the sample wheel is
described by a row in the spreadsheet.  Each column of the spreadsheet
carries one parameter of the XAFS scan.  


.. _fig-doublewheel-spreadsheet:
.. figure::  _images/doublewheel_spreadsheet.png
   :target: _images/doublewheel_spreadsheet.png
   :width: 70%
   :align: center

   Example spreadsheet for running an experiment from a wheel with a
   two sample rings.


If you have read :numref:`Section %s <ini>` about the INI file, then
most of the columns in this spreadsheet will be quite familiar.  Most
of the columns are used to specify the same set of parameters as in
the INI file |nd| file name, element, edge, and so on.

.. note:: February 2020

   The E\ :sub:`0` column is no longer used.  E\ :sub:`0` is now
   always taken from the tabulated value for ``element`` and ``edge``

The green cell in the first row is used to input the names of all the
people involved in the experiment, as explained above.

As explained above, row 6, row with an entirely green background, is
used to specify the default values for all the parameters.  The
concept here is to try to avoid having in input repetitive
information.  For instance, in this case, all measurements will be
made at the Fe K edge.  The element and edge are all specified in the
green row.  Those cells are left blank for all subsequent rows, so the
default values will be used.

In short, any cell that is left blank will use the value from the
green, default row.  Any cell for which a value is specified will be
used in the macro that gets generated.

The first column is used to specify the slot number for each sample on
the sample wheel.

The second column is a simple way of excluding the slot from
measurement simply by specifying *No*.

The next several columns correspond to lines in the INI file as
explained in :numref:`Section %s <ini>`.

Energy changes can be included in the macro by specifying different
values for element and/or edge in a row.  When specified
and different from the previous row, a call to the ``change_edge()``
command (:numref:`Section {number} <pds>`) is inserted into the macro.

Not shown in :numref:`Figure %s <fig-wheel-spreadsheet>` are columns for
tweaking the ``xafs_x`` and ``xafs_y`` positions, adjusting the
horizontal size of :numref:`slits3 (see Section %s) <slits3>`, and
adjusting the fluorescence detector position.


Again, assuming the tab in the spreadsheet was called ``mysamples``,
you can then run the macro generated from the spreadsheet by::

   RE(mysamples_macro())


Here are the first few lines of the macro generated from this
spreadsheet. Note that for each sample, the macro first moves using
the ``slot()`` command, then measures XAS using the ``xafs()``
command.  The ``xafs()`` command uses the INI file generated from the
green default line and has explicit arguments for the filled-in
spreadsheet cells.

.. sourcecode:: python
   :linenos:

   yield from slot(1)
   yield from xafs('MnFewheel.ini', filename='Fe-Rhodonite', sample='MnSiO3', comment='ID:93 Russia')
   close_last_plot()

   yield from slot(2)
   yield from xafs('MnFewheel.ini', filename='Fe-Johannsonite', sample='CaMnSi2O6 - LT', comment='B –Iron Cap Mine; Graham Country, Arizona')
   close_last_plot()

   yield from slot(3)
   yield from xafs('MnFewheel.ini', filename='Fe-Spessartine', sample='Mn3Al2(SiO4)3', comment='Grants Mining District; New Mexico')
   close_last_plot()


Linkam stage automation
-----------------------

One of the temperature control options at BMM is a `Linkam stage
<https://www.linkam.co.uk/thms600>`_.  Ours is the kind that can cool
using liquid nitrogen flow or heat up to 600 C using a resistive
heater.  The linkam stage is typically mounted upright on top fo the
XY stage.

.. _fig-linkamstage:
.. figure::  _images/linkam.png
   :target: _images/linkam.png
   :width: 40%
   :align: center

   The linkam stage at BMM is much like this one, except with a 3mm
   diameter hole in the heating block to allow for transmission XAFS.

The automation concept for the Linkam stage is quite similar to the
ex-situ sample holder.  Instead of specifying the slot position of the
sample, you will specify the target temperature for the measurement.
There is also a column for specifying the holding time after arriving
at temperature before beginning the XAFS measurement.

The feature described in :numref:`Section %s <spreadsheet_options>`
for modifying filenames is particularly useful in this context.  It
can be used to put the measurement temperature in the filename,
allowing you to simply specify a default filename, leaving that cell
in each row blank.  The generated data files will then have sensible
names. 


.. _fig-linkam-spreadsheet:
.. figure::  _images/linkam_spreadsheet.png
   :target: _images/linkam_spreadsheet.png
   :width: 70%
   :align: center

   Example spreadsheet for running a temperature-dependent experiment
   using the Linkam stage.


Glancing angle stage automation
-------------------------------

This stage is used to automate measurement at glancing angle, usually
on thin film samples.  The stage can be mounted horizontally or
vertically, allowing measurement of in- or out-of-plane strain in thin
films.

.. _fig-glancinganglestage:
.. figure::  _images/glancing_angle_stage.jpg
   :target: _images/glancing_angle_stage.jpg
   :width: 50%
   :align: center

   The glancing angle stage with 8 sample positions.

This stage is mounted on a rotation stage to move between samples.
The rotation stage is mounted on a tilt stage to set the incident
angle of the beam relative to the sample surface.  This entire set up
is mounted on the XY stage for alignment on the beam.

Each sample is affixed to a sample spinner (which is simply a cheap, 24 VDC
CPU fan).  The 8 spinners are independently controlled via slip ring
electrical connection that runs through the axis of the rotation
stage.  In practice, only the sample that is being measured is spinning.

Again, the automation concept is very similar to the ex situ sample
wheel.  Instead of specifying slot number, the spinner number is
specified on each row.  There is also a yes/no menu for specifying
whether the sample spins during measurement.

.. _fig-glancingangle-spreadsheet:
.. figure::  _images/glancingangle_spreadsheet.png
   :target: _images/glancingangle_spreadsheet.png
   :width: 70%
   :align: center

   Example spreadsheet for running an experiment using the glancing
   angle stage.

Not shown in :numref:`Figure %s <fig-glancingangle-spreadsheet>` are
columns for specifying how sample alignment is handled.  The default
is to do automated alignment.  This works by following this script:

#. Move the stage to an incident angle that is close to flat for the
   sample and start the sample spinning.
#. Do a scan in the vertical direction, measuring the signal in the
   transmission chamber. Fit an error function to the transmission
   signal.  The centroid of that function is the position with the
   sample half-way in the beam.
#. Do a scan in pitch, measuring the signal in the transmission
   chamber.  The peak of that measurement is the position where the
   sample is flat relative to the beam direction.
#. Repeat steps 2 and 3.
#. Move the sample tilt to the angle specified by the user in the
   spreadsheet.
#. Do a scan in the vertical direction, measuring the signal in the
   fluorescence detector.  The center of mass of that measurement is
   the position where the beam is well-centered on the sample.

The result of this fully automated sequence is shown in
:numref:`Figure %s <fig-spinner_alignment>`.

.. _fig-spinner_alignment:
.. figure::  _images/spinner-alignment.png
   :target: _images/spinner-alignment.png
   :width: 50%
   :align: center

   This visual representation of the automated glancing angle
   alignment is posted to Slack and presented in the measurement
   :numref:`dossier (Section %s) <dossier>`.

For some samples, the automated alignment is unreliable, so there is
an option in the spreadsheet for manual alignment.  In that case, find
the ``xafs_y`` and ``xafs_pitch`` positions for the sample at its
measurement angle and well-aligned in the beam.  Enter those numbers
and they will be used by the macro rather than performing the
automated alignment.

XY grid automation
------------------

The final kind of automation-via-spreadsheet available is BMM is for a
generic XY grid.  The most common XY grid used for measurement is the
sample XY stage, ``xafs_x`` and ``xafs_y``.  However, any two motors
on the beamline can be used for the grid.

There are columns (to the left of the view shown in :numref:`Figure %s
<fig-grid-spreadsheet>`) for specifying the axes in the grid.

In all other ways, this spreadsheet is identical to the ex-situ sample
wheel spreadsheet.

.. _fig-grid-spreadsheet:
.. figure::  _images/grid_spreadsheet.png
   :target: _images/grid_spreadsheet.png
   :width: 70%
   :align: center

   Example spreadsheet for running an experiment on an XY grid.

