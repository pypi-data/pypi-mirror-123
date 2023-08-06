Richie plugin for `Tutor <https://docs.tutor.overhang.io>`__
============================================================

.. TODO add some information here

Installation
------------

::

    pip install tutor-richie

Usage
-----

::

    tutor plugins enable richie

Running the Richie plugin will require that you rebuild the "openedx" Docker image::

    tutor config save
    tutor images build openedx

This step is necessary to install the Richie connector app in edx-platform.

Then, the platform can be launched as usual with::

    tutor local quickstart

You will be able to access your course catalog at http(s):courses.LMS_HOST. In development, this url will be http://courses.local.overhang.io.

Once your Richie platform is running,

Create superuser::

    tutor local run richie ./sandbox/manage.py createsuperuser

Create demo site::

    # WARNING: do not attempt this in production!
    tutor local run richie ./sandbox/manage.py create_demo_site --force

Configuration
-------------

.. TODO


Development
-----------

Bind-mount volume::

    tutor dev bindmount richie /app/richie

Then, run a development server::

    tutor dev runserver --volume=/app/richie richie

The Richie development server will be available at http://courses.local.overhang.io:8003.

License
-------

This software is licensed under the terms of the `AGPLv3 <https://www.gnu.org/licenses/agpl-3.0.en.html>`__.
