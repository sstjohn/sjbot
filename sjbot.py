#!/usr/bin/python

import sys
import random

stripper = lambda x: x.translate(None, " ~`!@#$%^&*()_+-=[]\{}|;':,./<>?\"").lower()

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
			words = [w.strip() for w in words if len(w) > 0 and w[0] != "@" and (w[0] != "[" or w[-1] != "]") and w[0:4] != "http"]
			if len(words) < 3:
				continue
			hashes.add(stripper("".join(words)))
			words.append(None)
			for n in words:
				try: t[(last,cur)] += [n]
				except: t[(last,cur)] = [n]
				
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
		if stripper(gen) in hashes:
			continue
		print gen
		i += 1
