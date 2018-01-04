### Labnotebook

A simple working notebook that makes it easy to include text, images,
syntax-highlighted code, math, and links to reference materials.

The input is a very basic text file with a few simple markup tags.

The output is an html file, which can easily be converted to pdf (see
`example.pdf`, above).

Markup tags and rules can be found in the top of `labnote.py`.

![alt text](resources/ex1.png "Example 1, Part 1.")


```
============================================================ 2017-12-21 1:59 AM
%% bold Some file-inclusion with syntax highlighting tests:

Let's include only a few lines from this file:

%% INCL resources/testfile.py:7-19

Now, how about a few more from the same file:

%% INCL resources/testfile.py:21-24

And an output file: (text format - which can also take a range, so you don't need more than one).

%% incl resources/outfile.txt
```


![alt text](resources/ex2.png "Example 1, Part 2.")

#### Usage:

It's easiest to just put a makefile in your working folder, and map a key to run
`make`.

I use `<Leader> m` in Vim, and run a python file server locally, using `python
-m http.server`.

That way you can see your output file, including MathJax-rendered equations at `localhost:8000/<yourfile>.html`.

Using a split-screen arrangement with a browser and a text editor, you can achieve
near-instant gratification (upon reload of the browser page, anyways).

![alt text](resources/split.png "Split-screen working view.")

#### Why not an Ipython or Jupyter notebook?

Those are both excellent solutions - but some people want something a little
simpler, that exports to different formats easily, makes nice reports if necessary, and does not
include all the `ln[1]:` line numbers for every input and output.

###### License:

This is a personal tool, in no way fit to be relied upon for any reason.  
Use it as you please, but 100% at your own risk.
