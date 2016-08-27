

pris/parse_pris.py: pris.bnf
	grako -o pris/parse_pris.py pris.bnf

clean:
	find -name '*.pyc' -or -name '*~' -print0 |xargs -0 rm
