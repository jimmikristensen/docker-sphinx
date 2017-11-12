import fileinput # This iterates over the lines of all files listed in sys.argv[1:]
import re # regex
import yaml

stream = open('/Users/jikr/Downloads/rst/_build/json/test.yml', 'r')
doc = yaml.load(stream)
for k,v in doc.items():
    print k, " -> ", v
print "\n"

#for line in fileinput.input(inplace=1):
#    line = re.sub('png', 'jpg', line.rstrip())
#    print(line)


#pysed.replace('../_images/plantuml-bb97be8c1bffd\
#ddd686367f7ea95a2f6249e5539.png', 'billed', '/Users/jikr/Downloads/rst/_build/json/README2.fjson')
