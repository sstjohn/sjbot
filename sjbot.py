#!/usr/bin/python

import sys
import random
import re

stripper = lambda x: x.translate(None, " ~`!@#$%^&*()_+-=[]\{}|;':,./<>?\"").lower()

def match(s, l, r):
	if None is s:
		return None
	lc = len(re.findall(l + '[a-zA-Z]', s))
        rc = len(re.findall('[a-zA-Z0-9.?,!]' + r,s))

        if lc > rc and s[-1] != r[-1]:
                s = s + r[-1]
                rc += 1
        
        if rc > lc and s[0] != l[-1]:
                s = l[-1] + s
                lc += 1

        if lc != rc:
                return None
	
	return s

def cleanup(old):
	s = old
	s = match(s, '"', '"')
	s = match(s, "'", "'")
	s = match(s, '\(', '\)')
	if None is s:
		return None

	while True:
		p = re.search("[\.?!] [a-z]",s)
		if p is None:
			break
		if s[p.start()] == ".":
			s = s[:p.start()] + s[p.start() + 1:]
		else:
			s = s[0:p.start() + 2] + s[p.start() + 2].upper() + s[p.start()+3:]	

	first = 0
	while first < len(s) and not s[first].isalpha():
		first += 1

	if first == len(s):
		return None

	if s[first].islower():
		s = s[:first] + s[first].upper() + s[first+1:]

	last = len(s) - 1
	while last > 0 and (s[last] == '"' or s[last] == "'" or s[last] == ")"):
		if s[last] == ":":
			last = 0
			break
		last -= 1

	if 0 != last:
		if s[last] == ",":
			s = s[:last] + "." + s[last+1:]

		if s[last] != "." and s[last] != "!" and s[last] != "?":
			s = s[:last+1] + random.choice([".","!","?"]) + s[last+1:]

	return s

def build_htable(hashtags):
	xht = {}
	for ht in hashtags:
		for w in hashtags[ht]:
			try:
				xht[w].append(ht)
			except:
				xht[w] = [ht]
	return xht

def get_hashtag(sentence, xht):
	choices = []
	for w in sentence.split(" "):
		try:
			choices.extend(xht[w])
		except:
			pass
	if len(choices) < 2:
		return None
	return random.choice(choices)

if __name__ == "__main__":
	t = {(None,None): []}
	hashes = set()
	hashtags = {}
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
			words = [w for w in words if len(stripper(w)) > 0 and w[0] != "@"]
			hts = [w for w in words if w[0] == "#"]
			for ht in hts:
				try:
					hashtags[ht].extend([w for w in words if w != ht])
				except:
					hashtags[ht] = [w for w in words if w != ht]
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

	xht = build_htable(hashtags)
	
	i = 0
	while i < 200:
		gen = ""
		last = None
		cur = random.choice(t[(None,None)])
		while cur is not None:
			gen += "%s " % cur
			choices = []
			try: 
				choices.extend(t[(last, stripper(cur))])
			except: pass
			if len(choices) < 2:
				try:
					choices.extend(t[(None, stripper(cur))])
				except: pass

			if len(choices) < 2:
				gen = ""
				break

			n = random.choice(choices)
			last = stripper(cur)
			cur = n
		o = cleanup(gen.strip())
		if o is None or stripper(o) in hashes or len(o) < 10 or len(o) > 140:
			continue
		if o.count("#") == 0:
			newht = get_hashtag(o, xht)
			if newht is not None:
				o += " " + newht
		print o
		print
		i += 1
