How to contribute
=================

.. highlight:: bash

First of all, if anything is incorrect or something is missing on this page (or
any other for that matter), please send in a pull request. It is important that
setting up the development environment is as painless as possible.

Setting up the development environment
--------------------------------------
Unfortunately there are quite some steps involved in setting up a development
environment. If you don't want to do this and know how Vagrant works, see the
bottom of this section on how to use that instead.

OS specific dependencies
~~~~~~~~~~~~~~~~~~~~~~~~
Some dependencies are OS specific. Ofcourse you need to have LaTeX installed,
but that also comes in some different packages on most systems.

For Ubuntu and other Debian based systems::

    sudo apt-get install python3 python3-dev virtualenv \
        texlive-pictures texlive-science texlive-latex-extra \
        imagemagick


Getting the source code
~~~~~~~~~~~~~~~~~~~~~~~
You need your own fork of the `Github repository
<https://github.com/JelteF/PyLaTeX>`_ by using the Github fork button. You will
then need to clone your version of the repo using the normal way, something
like this::

    git clone git@github.com:YourUserName/pylatex
    cd pylatex

Make your own branch for your specific feature or fix (don't do this just on
master)::

    git checkout -b your-nice-feature


Python environment setup
~~~~~~~~~~~~~~~~~~~~~~~~
This method will use a virtual environment, this is the easiest way to get all
the dependencies.

1. Create a virtualenv by running::

    virtualenv venv -p python3

2. Activate it by running (you should do this whenever you start working on
   your changes)::

    . venv/bin/activate

3. Install all the development dependencies inside the virtual environment by
   running::

    pip install -r dev_requirements.txt

Vagrant support
~~~~~~~~~~~~~~~
This might be an easier way to obtain a development environment, but the script
is not very well maintained and might not work anymore. If everything goes as
planned Vagrant will launch and configure a small virtual machine with all
necessary tools for you, so that you can start working with PyLaTeX right away.

With Vagrant already installed, you can start the virtual machine with
``$ vagrant up`` and then use ``$ vagrant ssh`` to ssh into it. Your source
files will be located under ``/vagrant``.
To run all unit tests and build the documentation run
``$ ./testall.sh -p python3 -c`` from that directory.

You can download or read more about Vagrant on https://www.vagrantup.com/.

Some tips before starting
-------------------------
1. Look at the code that is already there when creating something new, for
   instance the classes for tables.
2. To learn how to squash commits, read this `blog
   <http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html>`_.
   Ignore the word of caution, since that only applies to main repositories on
   which people base their own work.  You can do this when you have a couple of
   commits that could be merged together. This mostly happens when you have
   commits that fix a typo or bug you made in a pull request and you fix that
   in a new commit.

Some rules
----------
There are two things that are needed for every pull request:

1. Run the ``testall.sh`` script before making a pull request to check if you
   didn't break anything.
2. Follow the **PEP8** style guide and make sure it passes pyflakes (this is
   also tested with the ``testall.sh`` script).

These are also tested for by Travis, but please test them yourself as well.

Depending on your type of changes some other things are needed as well.

1. If you add new arguments, function or classes, add them to
   ``tests/args.py`` without forgetting to name the arguments. That way it is
   easy to see when the external API is changed in the future.
2. Change docstrings when necessary. For instance when adding new arguments or
   changing behaviour.
3. If you fix something, add a **test** so it won't break again.
4. If your change is user facing, add it to the **changelog** so it will be
   mentioned in the next release. Its location is at
   ``docs/source/changelog.rst``.
5. If you add something new, show it off with an **example**. If you don't do
   this, I will probably still merge your pull request, but it is always nice
   to have examples of features.
