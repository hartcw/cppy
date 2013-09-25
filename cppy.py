#!/usr/bin/env python
#
# ---------------------
# The MIT License (MIT)
#
# Copyright (c) 2013 Francis Hart
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ---------------------
#
# Written by Francis Hart
# http://hartcw.com
# http://github.com/hartcw/cppy

import io
import os
import re
import sys
import optparse
import platform
import builtins

class context:
    indent     = ''
    srcdir     = ''
    dstdir     = ''
    buffer     = None
    first      = True
    variables  = dict()
    colour_log = platform.system() != 'Windows'
    debug      = False

def parse_options():
    parser = optparse.OptionParser('cppy')
    parser.add_option('-i', '--input',
                      default='',
                      help='Specify the input file (defaults to stdin)')
    parser.add_option('-o', '--output',
                      default='',
                      help='Specify the output file (defaults to stdout)')
    parser.add_option('-t', '--type',
                      default='auto',
                      choices=['c', 'xml', 'auto'],
                      help='Set the type of embedded comment to match and expand (defaults to auto)')
    parser.add_option('-d', '--debug',
                      default=False,
                      action='store_true',
                      help='Enable debug information')
    (options, args) = parser.parse_args()
    return options

def log_set_colour(code):
    if context.colour_log:
        print('\033[' + str(code) + ';1m', end='', file=sys.stdout)

def log_unset_colour():
    if context.colour_log:
        print('\033[0m', end='', file=sys.stdout)
        sys.stdout.flush()

def log_error(message):
    log_set_colour(31)
    print('ERROR: ', message, file=sys.stdout)
    log_unset_colour()
    exit()

def log_warning(message):
    log_set_colour(33)
    print('WARNING: ', message, file=sys.stdout)
    log_unset_colour()

def log_message(message):
    log_set_colour(32)
    print(message, file=sys.stdout)
    log_unset_colour()

def log_debug(message):
    if context.debug:
        log_set_colour(32)
        print('DEBUG:', message, file=sys.stdout)
        log_unset_colour()

def print(*objects, sep=' ', end='\n', file=None, flush=False):
    if file == None:
        file = context.buffer
    if context.first:
        context.first = False
        text = sep.join(objects)
    else:
        text = context.indent + sep.join(objects)
    builtins.print(text, end=end, file=file)

def execute(code, indent, first):
    buffer = io.StringIO()
    indent = re.sub(r'[^\t]', ' ', indent)
    code = re.sub(r'^' + indent, '', code, flags=re.MULTILINE)
    log_debug('INDENT'+indent+'INDENTEND')
    log_debug('CODE\n' + code + '\nCODEEND')
    prev_buffer = context.buffer
    prev_indent = context.indent
    prev_first = context.first
    context.buffer = buffer
    context.indent = indent
    context.first = first
    exec(code, globals(), context.variables)
    context.buffer = prev_buffer
    context.indent = prev_indent
    context.first = prev_first
    output = buffer.getvalue().rstrip('\n')
    log_debug('OUTPUT\n' + output + '\nOUTPUTEND')
    return output

def match_with_indent(match):
    matches = list(match.groups())
    indent = matches[0]
    i = 1
    code = ''
    while i < len(matches):
        if matches[i] != None:
            code += matches[i]
        i += 1
    return execute(code, indent, False)

def match_without_indent(match):
    prefix = match.string[0:match.start()]
    indent = prefix[prefix.rfind('\n') + 1:]
    code = ''
    for m in list(match.groups()):
        if m != None:
            code += m
    return execute(code, indent, True)

def srcdir():
    return context.srcdir

def dstdir():
    return context.dstdir

def expand(input='', output='', type='auto', newline=None):
    log_debug('expand input=' + input + ' output=' + output)
    cwd = os.getcwd()
    prev_srcdir = context.srcdir
    prev_dstdir = context.dstdir
    if newline == None:
        newline = os.linesep
    if output == '':
        if context.buffer != None:
            dst = context.buffer
        else:
            dst = sys.stdout
    else:
        if not os.path.exists(os.path.dirname(output)):
            os.mkdir(os.path.dirname(output))
        dst = open(output, 'wt', newline=newline)
        context.dstdir = os.path.abspath(os.path.dirname(output))
    if input == '':
        src = sys.stdin
    else:
        src = open(input, 'rt')
        context.srcdir = os.path.abspath(os.path.dirname(input))
        dirname = os.path.dirname(input)
        if dirname != '':
            os.chdir(dirname)
    contents = src.read()
    regexes = [
        (re.compile(r'^([ \t]*)#[ \t]*py[ \t]*(?:(.*)\\(\n))*(.*)$', re.MULTILINE), match_with_indent),
        (re.compile(r'<!--[ \t]*py[ \t]*(.*?)[ \t]*-->', re.DOTALL | re.MULTILINE), match_without_indent),
        (re.compile(r'/\*\**[ \t]*py[ \t]*(.*?)[ \t]*\*/', re.DOTALL | re.MULTILINE), match_without_indent),
        (re.compile(r'//[ \t]*py[ \t]*(.*)$', re.MULTILINE), match_without_indent)
    ]
    for regex, match_function in regexes:
        contents = regex.sub(match_function, contents)
    dst.write(contents)
    os.chdir(cwd)
    context.srcdir = prev_srcdir
    context.dstdir = prev_dstdir
    if output != '':
        dst.close()
    if input != '':
        src.close()

def main():
    options = parse_options()
    context.debug = options.debug
    expand(options.input, options.output, options.type)

if __name__ == '__main__':
    main()
