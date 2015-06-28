

pris/parse_pris.py: pris.bnf
	grako -o pris/parse_pris.py pris.bnf

clean:
	find -name *.pyc -print0 |xargs -0 rm
	find -name *~ -print0 |xargs -0 rm
