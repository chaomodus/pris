

parse_pris.py: pris.bnf
	grako -o parse_pris.py pris.bnf
