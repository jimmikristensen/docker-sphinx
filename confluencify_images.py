import re, shutil, tempfile

def replace_in_file(filename, pattern, replace):
    '''
    Perform a Python equivalent of in-place `sed` substitution: e.g.,
    `sed -i -e 's/'${pattern}'/'${repl}' "${filename}"`.
    '''
    # For efficiency, precompile the passed regular expression.
    pattern_compiled = re.compile(pattern)

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(filename) as src_file:
            for line in src_file:
                tmp_file.write(pattern_compiled.sub(repl, line))

    #overwrite original file with temp file such that file attributes are preserved
    shutil.copystat(filename, tmp_file.name)
    shutil.move(tmp_file.name, filename)

replace_in_file('/Users/jikr/Downloads/rst/_build/json/README2.fjson', r'../_images/plantuml-bb97be8c1bffd\
ddd686367f7ea95a2f6249e5539.png', '')
