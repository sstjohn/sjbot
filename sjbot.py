#!/usr/bin/python

import sys
import random
import re

stripper = lambda x: x.translate(None, " ~`!@#$%^&*()_+-=[]\{}|;':,./<>?\"").lower()

def cleanup(old):
	s = old
	ldq = len(re.findall('"[a-zA-Z]', s))
	rdq = len(re.findall('[a-zA-Z0-9.?,!]"',s))

	if ldq > rdq and s[-1] != '"':
		s = s + '"'
		rdq += 1
	
	if rdq > ldq and s[0] != '"':
		s = '"' + s
		ldq += 1

	if ldq != rdq:
		return None

	lp = len(re.findall("\([a-zA-Z]", s))
	rp = len(re.findall("[a-zA-Z0-9.,?,]\)",s))

	if lp > rp and s[-1] != ")":
		s = s + ")"
		rp += 1

	if rp > lp and s[0] != "(":
		s = "(" + s
		lp += 1
	
	if lp != rp or len(s) < 10:
		return None

	while True:
		p = re.search("[\.?!] [a-z]",s)
		if p is None:
			break
		s = s[0:p.start()] + "," + s[p.start() + 1:]	

	first = 0
	while not s[first].isalpha() and first < len(s):
		first += 1

	if first == len(s):
		return None

	if s[first].islower():
		s = s[:first] + s[first].upper() + s[first+1:]

	last = len(s) - 1
	while last > 0 and (s[last] == '"' or s[last] == "'" or s[last] == ")"):
		last -= 1

	if 0 == last:
		return None

	if s[last] == ",":
		s = s[:last] + "." + s[last+1:]

	if s[last] != "." and s[last] != "!" and s[last] != "?":
		s = s[:last+1] + random.choice([".","!","?"]) + s[last+1:]

	return s

if __name__ == "__main__":
	t = {(None,None): []}
	hashes = set()
	with open("input.txt","r") as f:
		buf = ""
		for inp in f.readlines():
			buf += " %s" % inp.strip()
			if not (buf[-1] == "." or buf[-1] == "!" or buf[-1] == "?" or buf[-1] == '"' or buf[-1] == "'" or buf[-1] == ")"):
				continue
			words = buf.split(" ")
			buf = ""
			last = None
			cur = None
			words = [w for w in words if len(stripper(w)) > 0]
			if len(words) < 2:
				continue
			hashes.add(stripper("".join(words)))
			words.append(None)
			for n in words:
				try: t[(last,cur)] += [n]
				except: t[(last,cur)] = [n]
				
				try: t[(None,cur)] += [n]
				except: t[(None,cur)] = [n]

				last = cur
				
				try: cur = stripper(n)
				except: pass
	i = 0
	while i < 200:
		gen = ""
		last = None
		cur = random.choice(t[(None,None)])
		while cur is not None:
			gen += "%s " % cur
			n = random.choice(t[(last, stripper(cur))])
			last = stripper(cur)
			cur = n
		o = cleanup(gen.strip())
		if o is None or stripper(o) in hashes or len(o) < 10 or len(o) > 140:
			continue
		print o
		print
		i += 1
