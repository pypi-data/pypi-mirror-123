
filename = 'mca.spec'

from spec import FileSpec

f = FileSpec(filename)

for s in f:
    print( s.getCommand() )
    print( len( s.getMcas() ) )
