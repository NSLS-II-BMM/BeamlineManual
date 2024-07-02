..
   This document was developed primarily by a NIST employee. Pursuant
   to title 17 United States Code Section 105, works of NIST employees
   are not subject to copyright protection in the United States. Thus
   this repository may not be licensed under the same terms as Bluesky
   itself.

   See the LICENSE file for details.

.. _data:

Data access
===========

In May 2024, data security policies were implemented at BMM.  This has
impact on user operations and data access.

Data is now written to a secure location on central storage.  Access
to your data now requires authentication using your BNL domain
account, your password, and two-factor authentication with DUO or a
Yubi key.

The beamline operator account does not have access to user's data.

This section of the beamline manual explains how to access you data
during and after your experiment.

Downloading data
----------------

You will need an sftp client.  The recommendation of BMM staff is to
use `FileZilla <https://filezilla-project.org/>`__.  This is a free
program available for Windows, Apple, and Linux.  The explanation
below will be made using FileZilla.

:Windows users: Another option is `WinSCP
		<https://winscp.net/eng/index.php>`__. Be careful at
		the WinSCP website.  You will see multiple pop-up adds
		with download links to other software packages.  Be
		sure to click on the link to the WinSCP package.

:Mac users: Another options are `Termius
	    <https://apps.apple.com/us/app/termius-ssh-sftp-client/id1176074088?mt=12>`__
	    and `Flow <http://fivedetails.com/flow/>`__.

:Linux users: Your desktop file manager likely has an sftp client
	      built in.  Try typing
	      ``sftp://<username>@sftp.nsls2.bnl.gov`` into your file
	      manager.

.. admonition:: The short version

   #. Connect to sftp://sftp.nsls2.bnl.gov
   #. Authenticate using your BNL username/password and DUO two-factor
      authentication
   #. Navigate to ``/nsls2/data/bmm/proposals/``, then to the cycle
      folder corresponding to the date of your experiment, then to the
      folder with your proposal number.
   #. Transfer your data to your local computer.


What follows is a guide with screenshots of using FileZilla to connect
to the SFTP download site and begin downloading data.

To begin, open your sftp client.  Here is FileZilla at startup.  For
FileZilla, click on the File menu, then click on Site Manager.

.. _fig-fz-startup:
.. figure:: _images/filezilla_startup.png
   :target: _images/filezilla_startup.png
   :width: 50%
   :align: center

   FileZilla startup.  Go to the Site Manager to establish a new
   location.


In the site manager, click on the "New site" button and fill in the
details as shown below.  Select the SFTP protocol, enter
``sftp.nsls2.bnl.gov`` as the Host.  The correct port number is 22,
but you can usually leave that blank.  22 is the default port for the
sftp protocol.  

Finally, select "Interactive" as the logon type.  That will tell
FileZilla to prompt you for both user name and two-factor authentication.

.. _fig-fz-site_manager:
.. figure:: _images/filezilla_site_manager.png
   :target: _images/filezilla_site_manager.png
   :width: 50%
   :align: center

   Fill in the site manager with the location and logon type for the
   NSLS2 data center.

Click OK to finish this configuration, then connect to the host.


.. _fig-fz-connect:
.. figure:: _images/filezilla_connect.png
   :target: _images/filezilla_connect.png
   :width: 50%
   :align: center

   Select the NSLS2 host from the drop-down list and click to connect.


Connecting to the NSLS2 SFTP host will open up the password entry dialog.


.. _fig-fz-password:
.. figure:: _images/filezilla_password.png
   :target: _images/filezilla_password.png
   :width: 50%
   :align: center

   Enter your BNL password and click OK.

After entering your password, you will be prompted for two factor
authentication.  In the "Password" box, type ``1`` and hit OK.  Then
go to your phone and accept the DUO push.  

If you use a Yubikey, click on the "Password" box and touch the button
on your Yubikey.

Once you have completed the DUO push, you will be able to navigate on
the remote site.  Click your way to ``/nsls2/data/bmm/`` as shown below.

.. _fig-fz-remote:
.. figure:: _images/filezilla_remote.png
   :target: _images/filezilla_remote.png
   :width: 50%
   :align: center

   Navigate down to the BMM proposals area on the SFTP server.

Click into ``proposals`` then into the folder for the cycle in which
your experiment happened, then into the folder for your proposal
number:


.. _fig-fz-folder:
.. figure:: _images/filezilla_folder.png
   :target: _images/filezilla_folder.png
   :width: 50%
   :align: center

   Navigate into the folder for your proposal and the cycle in which
   it ran.

Now select the data files you want to transfer.  You may select
multiple files or even entire folders.

.. _fig-fz-queue:
.. figure:: _images/filezilla_queue.png
   :target: _images/filezilla_queue.png
   :width: 50%
   :align: center

   Select some or all of your data and add it to the queue.


Click on the transfer button at the top of the screen to initiate the
transfer.  At the beginning of the transfer, you will have to
re-authenticate yourself.

.. _fig-fz-transfer:
.. figure:: _images/filezilla_transfer.png
   :target: _images/filezilla_transfer.png
   :width: 50%
   :align: center

   Click the transfer button to download your data.  You may need to
   re-authenticate at the start of transfer.

Your data is now on your computer.  Yay!


Using the VDI virtual Desktop
-----------------------------

.. todo:: Need to flesh this out.


Accessing data from the beamline computers
------------------------------------------

In a terminal window ``su - <username>``, enter password and respond
to DUO push.

``cd`` to ``/nsls2/data3/bmm/proposals/2024-2/pass-123456``, replacing
``2024-2`` with the cycle of your visit and ``123456`` with your
proposal number.

``dathena`` at the command line to use Athena.  Or use jupyter.




Accessing data via Tiled
------------------------

.. todo:: Need to flesh this out.
