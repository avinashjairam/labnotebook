#! /usr/bin/python

''' Labnote:    A quick, simple working notebook, which supports inclusion of
                highlighted code blocks, images, math equations (via MathJax),
                and formatted hyperlinks to sources/references.

                Soon to come:  Bibliography citations - for building papers.

    Usage:  $ ./labnote.py <project_log>.ln

    The output is html, so it helps to be serving your working folder locally.
    To do so, navigate to your working directory and run:
    python -m http.server

    Then your compiled html log file should be visible at:
    http://localhost:8000/<project_log>.html

    Export to .pdf can be accomplished by either pandoc, or simply
    printing to pdf from the browser.


    Markup Specification:
        === <text>      :  Draw horizontal line - with <text> right-justified.
        /* comment */   :  Line-based comment (one line only)
        %% <tag>        :  Tag identifier.  Following '%%' you can put:
            IMG <path/to/image> :  Include image from /path/to/<imagename>
            INCL <path/to/file> :  Include text of code file (.py or .txt)
            INCL <file>:10-20   :  Only include lines 10-20 of <file>.
            BOLD <text>         :  Bold text
            CODE <code line>    :  Line of code - python syntax highlighting.
            LINK <title> <link> :  Link with display title and entire link.

        Tags do not have to be capitalized.
'''

import sys

from pygments import highlight
from pygments.lexers import PythonLexer, TextLexer
from pygments.formatters import HtmlFormatter


HEADER = ("""<!DOCTYPE html>\n<html lang="en">\n"""
          """<meta charset="utf-8"/>\n"""
          """<link rel="stylesheet" type='text/css'"""
          """ href="resources/styles.css">\n"""
          """<script type="text/javascript" async """
          """src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/"""
          """MathJax.js?config=TeX-MML-AM_CHTML">"""
          """</script>\n"""
          """</body>\n"""
          """<div style="width: 90%; padding: 25px;">\n""")

IMAGE = ("""<div style="text-align: center; width: 100%%">"""
         """<img src="%s"></div>\n""")
#  """<img src="%s" style="width: 80%%;"></div>\n""")

LINK = """<a href="%s" target="_blank">%s</a><br>\n"""

FOOTER = "</div>\n</body>\n</html>"


def format_python(code):
    """ Pygments built-in colorschemes:
        'default', 'emacs', 'friendly', 'colorful', 'autumn', 'murphy',
        'manni', 'monokai', 'perldoc', 'pastie', 'borland', 'trac', 'native',
        'fruity', 'bw', 'vim', 'vs', 'tango', 'rrt', 'xcode', 'igor',
        'paraiso-light', 'paraiso-dark', 'lovelace', 'algol', 'algol_nu',
        'arduino', 'rainbow_dash', 'abap'
    """
    result = highlight(code, PythonLexer(), HtmlFormatter(
            noclasses=True, style='friendly'))
    return result


def format_text(text):
    result = highlight(text, TextLexer(), HtmlFormatter(
            noclasses=True, style='friendly'))
    return result


def img_handler(htmlfile, line):
    image = line.strip('\n').lstrip('[').rstrip(']')
    image_code = (IMAGE % image)
    htmlfile.write(image_code)


def link_handler(htmlfile, line):
    title, link = line.replace('%', '').split()
    linkstring = LINK % (link, title)
    htmlfile.write(linkstring)


def code_handler(htmlfile, line):
    ''' Currently defaults to python - later add Linux Bash shell, etc.'''
    new_line = format_python(line)
    html = ("""<div style="padding-left: 50px; padding-right: 50px; """
            """width: 80%%">%s</div>""")
    htmlfile.write(html % new_line)


def incl_file_handler(htmlfile, filepath):
    ''' Include the text of the file at <filepath>.
        Currently only supports Python or text.
        C and C++ to be added shortly.
    '''

    divstart = ("""<div style="padding-left: 50px; padding-right: 60px; """
                """width: 80%%">""")

    divend = """</div>"""

    if ':' in filepath:
        path, linerange = filepath.split(':')
        start, end = linerange.split('-')
        start, end = int(start), int(end)
    else:
        path = filepath
        start = 0
        end = 500  # 500 lines max - will you ever need to include more?

    included_range = ''

    with open(path, 'rt') as includefile:
        for index, line in enumerate(includefile):
            if index >= start and index <= end:
                included_range += (line)

        if path.split('.')[1] == 'py':
            contents = format_python(included_range)
        else:
            contents = format_text(included_range)
        htmlfile.write(divstart + contents + divend)


def exec_handler(htmlfile, filepath):  # or code?
    ''' Execute code, and paste the results into the html file. '''
    pass


def bold_handler(htmlfile, line):
    new_line = "%s%s%s" % (
        '<b>', line, '</b><br>\n')  # noqa
    htmlfile.write(new_line)


def div_line(htmlfile, line):
    htmlfile.write('<hr>\n<div style="float: right; font-size: 8px";>')
    htmlfile.write(line.split(' ', 1)[1])
    htmlfile.write("</div>\n")


def setup_handlers():
    keys = 'img bold link code incl exec div_line'.split()
    handlers = [img_handler, bold_handler, link_handler,
                code_handler, incl_file_handler, exec_handler, div_line]

    string_func_map = dict(zip(keys, handlers))
    return string_func_map


def generate_html(logfile):
    ''' The newline chars are for human-readability of the html source code.'''
    handlers = setup_handlers()

    with open(logfile, 'r+t') as infile:
        outfile = "%s%s" % (logfile.split('.')[0], '.html')
        with open(outfile, 'wt') as htmlfile:
            htmlfile.write(HEADER)

            for line in infile:
                line = line.strip()  # Kill newline.
                if not line:
                    htmlfile.write('<br>\n')
                else:
                    if line.startswith('/*'):  # Comments
                        continue
                    elif line.startswith('=='):  # Section divider + Date
                        div_line(htmlfile, line)
                        continue

                    elif line.startswith('%%'):  # Tag identifier:
                        tag = line.split()[1].lower()
                        if tag in handlers:
                            args = line.split(' ', 2)[2]
                            handlers[tag](htmlfile, args)  # Just the args
                    else:  # it's a regular line of text:
                        new_line = "%s%s" % (line, '<br>\n')
                        htmlfile.write(new_line)

            htmlfile.write(FOOTER)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python generator.py <logfile>")
        sys.exit(0)
    generate_html(sys.argv[1])
