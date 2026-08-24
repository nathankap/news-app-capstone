User Guide
==========

Roles and Flow
--------------

1. Register a user account.
2. Journalists create articles and newsletters.
3. Editors approve pending articles.
4. Readers browse approved content and manage subscriptions.

Helpful Pages
-------------

* Home page: approved content overview.
* Dashboard: role-based actions and review queue.
* Article and newsletter pages: standalone content views.

API Endpoints
-------------

Main API routes are under ``/api/``:

* ``/api/token/``: obtain auth token.
* ``/api/articles/``: list/create articles.
* ``/api/articles/<id>/``: retrieve/update/delete article.
* ``/api/newsletters/``: list/create newsletters.

Troubleshooting
---------------

* If links appear stale, rebuild docs from ``docs``:

  .. code-block:: powershell

     .\make.bat html

* If Django import errors appear during doc build, confirm
  ``DJANGO_SETTINGS_MODULE`` is set in ``docs/source/conf.py``.
