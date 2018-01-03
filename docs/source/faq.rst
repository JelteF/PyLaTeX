Frequently Asked Questions
==========================

.. highlight:: bash

How do I...
-----------

... "Rerun LaTeX" 
   Sometimes the compiler will not be able to complete the document in one pass.  
   In this case it will instruct you to "Rerun LaTeX" via the log output

   In order to deal with this, you need to make sure that `latexmk
   <http://personal.psu.edu/jcc8//software/latexmk-jcc>`_ is installed.  
   Pylatex will detect and use it automatically.
  
   For Ubuntu and other Debian based systems::

       sudo apt-get install latexmk

