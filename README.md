cppy
====
cppy is a tool for programmatically generating embedded content within a file.
It is similar in concept to the C/C++ preprocessor macro, except that the
embedded code is expressed in python, allowing a far richer set of possibilities
for content generation. The tool reads an input file and searches for the
embedded python code. It extracts this code, runs it through a python
interpreter, and replaces it with the output from the interpreter.

Input files are not limited to C/C++ source. The embedded python code blocks can
be placed within any text file, such as xml/html, css, or javascript files.

Embedding Code
--------------
The embedded code must be contained with specific markers within the file.
Three types of markers are currently supported.

### C/C++ preprocessor directives
    #py 'some python code'

### C++ single line comments
    //py 'some python code'

### C/C++ multi line comments
    /*py
        'some python code'
    */

### Xml style comments
    <!--py 'some python code' -->

License
-------
cppy is licensed under the MIT license.

The source code is available at <http://github.com/hartcw/cppy>.

Acknowledgements
----------------
cppy was created by Francis Hart for <http://hartcw.com>.
