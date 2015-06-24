### How to contribute

#### Some tips

- Install all the development dependencies by running `pip install -e .[all]
    -r docs_requirements.txt` when
you are in your local fork.
- To learn how to squash commits, read this
    [blog](http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html).
    Ignore the word of caution, since that only applies to main repositories on
    which people base their own work.
    You can do this when you have a couple of commits that are basically fix
    this typo/bug in the code I created for this same pull request.
- Look at the code that is already there when creating something new, for
    instance the classes for tables.


#### Some rules
There are just two things you really need to do:
- Follow the **PEP8** style guide and make sure it passes pyflakes.
    (You can use flake8 with the pep8-naming extension to test these both)
- Run the `testall.sh` script before making a pull request to check if you
    didn't break anything.

If you don't do these two things Travis will catch you anyway.


If you want you can also do these things and they are appreciated:

- If you add something new, show it off with an **example**.
- If you add new arguments, function or classes, add them to
    `tests/args.py` without forgetting to name the arguments. That way I will know when the external API is changed
    later on.
- If you fix something, add a **test** so it won't break again.
- Add your addition, change or fix to the **changelog** so it will be mentioned
    in the next release.

It would be nice if you would do these things. But to be fair, I don't do it
all the time either.
