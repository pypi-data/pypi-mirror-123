.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://coveralls.io/repos/github/plone/plone.autoinclude/badge.svg?branch=main
    :target: https://coveralls.io/github/plone/plone.autoinclude?branch=main
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/v/plone.autoinclude.svg
    :target: https://pypi.org/project/plone.autoinclude/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/plone.autoinclude.svg
    :target: https://pypi.org/project/plone.autoinclude
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/plone.autoinclude.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/plone.autoinclude.svg
    :target: https://pypi.org/project/plone.autoinclude/
    :alt: License


=================
plone.autoinclude
=================

Automatically include zcml of a package when it is loaded in a Plone site.

Features
--------

- It is an alternative to ``z3c.autoinclude``.
- When a package registers an autoinclude entry point, we load its Python code at Zope/Plone startup.
- And we load its zcml.
- Works with Buildout-installed packages.
- Works with pip-installed packages.


Compatibility
-------------

This is made for Python 3.6+.
It works on Plone 5.2 and 6.0.

It is intended (at least by some) to be used in core Plone 6.
See "pre-PLIP" `3053 <https://github.com/plone/Products.CMFPlone/issues/3053>`_.


For add-on authors
------------------

When you have an existing package that has some zcml, you probably already have something like this in your ``setup.py``::

    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """

or in a dictionary::

    entry_points={
        "z3c.autoinclude.plugin": [
            "target = plone",
        ],
    }

or in ``setup.cfg``::

    [options.entry_points]
    z3c.autoinclude.plugin =
        target=plone

This still works!
You do not need to change anything.

But if you do not care about compatibility with ``z3c.autoinclude``, you could use this new entry point::

    entry_points="""
    [plone.autoinclude.plugin]
    target = plone
    """

It does the same thing, but it only works with ``plone.autoinclude``.


Entry point details
-------------------

This is an entry point with all options specified::

    entry_points="""
    [plone.autoinclude.plugin]
    target = plone
    module = example.alternative
    """

You must specify at least one option, otherwise the entry point does not exist.

``target``
    In which framework should your zcml be loaded?
    For a Plone add-on you would use ``plone``.
    If Zope ever wants to use something similar, it could add configuration to look for packages with ``target="zope"``.
    You can come up with targets yourself, and load them in a policy package, maybe: cms, frontend, companyname, customername, nl/de (language).
    If target is empty, or the option is not there, the zcml will get loaded by all frameworks.

``module``
    Use this when your package name is different from what you import in Python.


Comparison with ``z3c.autoinclude``
-----------------------------------

- ``z3c.autoinclude`` supports ``includeDependencies`` in a zcml file in your package.
  This would look in the ``setup_requires`` of the package to find dependencies.
  For each, it would load the zcml.
  This can take quite long.
  It might not work for packages installed by ``pip``, but this is not confirmed.
  In the Plone community this is discouraged, and Plone already disables this in the tests.
  ``plone.autoinclude`` does not support this.
  You should load the zcml of the dependencies explicitly in the ``configure.zcml`` of your package.
- ``z3c.autoinclude`` tries hard to find packages in non-standard places, installed in weird or old ways,
  or with a module name that differs from the package name, with code especially suited for eggs that buildout installs.
  ``plone.autoinclude`` simply uses ``importlib.import_module`` on the module name.
  If there is a mismatch between package name and module name, you can set ``module = modulename`` in your entry point.
- ``z3c.autoinclude`` does not support empty targets.
  The target of the entry point must match the target that is being loaded.
  ``plone.autoinclude`` *does* support empty targets: they will always get loaded.
  This is not good or bad, it is just a different choice.
- ``z3c.autoinclude`` supports disabling loading the plugins, via either an environment variable or an api call.
  ``plone.autoinclude`` does not.
  But ``Products.CMFPlone`` currently loads the ``z3c.autoinclude`` plugins unless a zcml condition is true: ``not-have disable-autoinclude``.
  When ``Products.CMFPlone`` switches to ``plone.autoinclude``, it can use this same condition.

In general, ``plone.autoinclude`` is a bit more modern, as it only started in 2020, and only supports Python 3.


Installation
------------

Note: this will change when/if Plone 6 uses ``plone.autoinclude`` by default.
You do not have to worry about this then.
But this package should be usable with targets other than Plone.

To install ``plone.autoinclude``, first add it to your buildout::

    [buildout]
    ...
    eggs =
        plone.autoinclude
    zcml =
        plone.autoinclude-meta

and then run ``bin/buildout``.

You may need to disable ``z3c.autoinclude``, as it does not seem useful to let them both run.
In a ``meta.zcml`` file, add::

    <meta:provides feature="disable-autoinclude" />

If the ``z3c.autoinclude`` package is present, it will see this and do nothing.

For core Plone my intention would be to do this:

- Remove code that loads the ``z3c.autoinclude`` package, mostly in ``Products.CMFPlone``.
  Replace it with the ``plone.autoinclude`` variant.

- In ``Products.CMFPlone/meta.zcml`` set::

    <include package="plone.autoinclude" file="meta.zcml" />
    <autoIncludePlugins target="plone" file="meta.zcml" />

- In ``Products.CMFPlone/configure.zcml`` set::

    <autoIncludePlugins target="plone" file="configure.zcml" />

- In ``Products.CMFPlone/overrides.zcml`` set::

    <autoIncludePluginsOverrides target="plone" file="overrides.zcml" />

See also the ``package-includes`` directory in this repository and ``test-packages/example.ploneintegration``.
And see `CMFPlone branch plone-autoinclude <https://github.com/plone/Products.CMFPlone/tree/plone-autoinclude>`_, based on 5.2.x.


Installation with pip
---------------------

Let's leave buildout completely out of the picture and only use pip, in this case with plone 5.2.3::

    # Create virtual environment in the current directory:
    python3.8 -mvenv .
    # Install Plone:
    bin/pip install -c https://dist.plone.org/release/5.2.3/constraints3.txt Products.CMFPlone
    # Install plone.autoinclude from the current git checkout:
    bin/pip install -e .
    # When I try bin/mkwsgiinstance it complains that Paste is missing.
    # We could use waitress instead, but let's try Paste for now:
    bin/pip install -c https://dist.plone.org/release/5.2.3/constraints3.txt Paste
    # Create the Zope WSGI instance:
    bin/mkwsgiinstance -d . -u admin:admin
    # Copy our zcml that disables z3c.autoinclude and enables our own:
    cp -a package-includes etc/
    # Start Zope:
    bin/runwsgi -v etc/zope.ini


Contribute or get support
-------------------------

- If you are having issues, please let us know in the issue tracker: https://github.com/plone/plone.autoinclude/issues
- The source code is on GitHub: https://github.com/plone/plone.autoinclude


License
-------

The project is licensed under the GPLv2.
