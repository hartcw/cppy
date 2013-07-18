#!/usr/bin/env python3

import cppy.cppy
import os
import fnmatch
import filecmp

def test_file(file):
    src = os.path.join('src', file)
    dst = os.path.join('dst', file)
    ref = os.path.join('ref', file)
    cppy.cppy.expand(src, dst, newline='\n')
    if filecmp.cmp(dst, ref):
        print('Passed: ' + file)
        return True
    print('FAILED: ' + file)
    return False

def run():
    if os.path.exists('dst') == False:
        os.mkdir('dst')
    num = 0
    failed = 0
    for file in sorted(os.listdir('src')):
        for filter in ['*.h', '*.cpp', '*.xml', '*.html']:
            if fnmatch.fnmatch(file, filter):
                num += 1
                if test_file(file) == False:
                    failed += 1
    if failed == 0:
        print('PASSED ALL ' + str(num) + ' TESTS')
    else:
        print('FAILED ' + str(failed) + ' OF ' + str(num) + ' TESTS')

if __name__ == '__main__':
    run()
