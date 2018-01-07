import re, shutil, tempfile, sys

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
                tmp_file.write(pattern_compiled.sub(replace, line))

    #overwrite original file with temp file such that file attributes are preserved
    shutil.copystat(filename, tmp_file.name)
    shutil.move(tmp_file.name, filename)

filename=sys.argv[1]
img=sys.argv[2]
replace_in_file(filename, r'<p class=\\"plantuml\\">\\n<img src=\\"\.\./_images/%s.*?</p>' % img, '<p><ac:image><ri:attachment ri:filename=\\"%s\\" ri:version-at-save=\\"1\\" /></ac:image></p>' % img)
