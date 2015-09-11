How to contribute
=================

This section needs to be filled. For now, see the `CONTRIBUTING.md
<https://github.com/JelteF/PyLaTeX/blob/master/CONTRIBUTING.md>`_ file in the
git repository.

Vagrant support
---------------
If you don't want to manually setup a suitable development environment in
order to contribute, PyLaTeX comes with a ready-made Vagrantfile. Vagrant
will launch and configure a small virtual machine with all necessary
tools for you, so that you can start working with PyLaTeX right away.

With Vagrant already installed, you can start the virtual machine with
``$ vagrant up`` and then use ``$ vagrant ssh`` to ssh into it. Your source
files will be located under ``/vagrant``.
To run all unit tests and build the documentation run
``$ ./testall.sh -p python3 -c`` from that directory.

You can download or read more about Vagrant on https://www.vagrantup.com/.
