#!/usr/bin/python

import sys
import random
import re
import csv

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
	s = match(old, '"', '"')
	s = match(s, "'", "'")
	s = match(s, '\(', '\)')
	if None is s:
		return None

	words = s.split()
	s = ""
	while len(words) > 0 and len(words[0]) > 0 and words[0][0] == "@":
		words.pop(0)

	while len(words) > 0:
		w = words.pop(0)
		if w[0] == "@":
			return None
		s += w + " "	

	return s.strip()

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

def tweet(t, xht):
	o = None
	while o is None:
		gen = ""
		llast = None
		last = None
		cur = random.choice(t[(None,None,None)])
		while cur is not None:
			gen += "%s " % cur
			choices = []
			try: 
				choices.extend(t[(llast, last, stripper(cur))])
			except: pass
			if len(choices) < 4:
				try:
					choices.extend(t[(None, last, stripper(cur))])
				except: pass
			if len(choices) < 1:
				gen = ""
				break

			n = random.choice(choices)
			llast = last
			last = stripper(cur)
			cur = n
		o = cleanup(gen.strip())
		if (o is None or stripper(o) in hashes or len(o) < 10 or
				len(o) > 140 or o.count("@") > 0 or o.count(" ") < 1):
			o = None
		elif o.count("#") == 0 and random.random() > 0.5:
			newht = get_hashtag(o, xht)
			if newht is not None:
				o += " " + newht
	return o

if __name__ == "__main__":
	t = {(None,None): []}
	hashes = set()
	hashtags = {}
	with open("input.csv","r") as f:
		tweetreader = csv.reader(f)
		for inp in tweetreader:
			words = inp[2].split()
			if words[0] == "RT":
				continue
			llast = None
			last = None
			cur = None
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
				try: t[(llast,last,cur)] += [n]
				except: t[(llast,last,cur)] = [n]

				try: t[(None,last,cur)] += [n]
				except: t[(None,last,cur)] = [n]
		
				llast = last
				last = cur
				
				try: cur = stripper(n)
				except: pass

	xht = build_htable(hashtags)
	
	i = 0
	while i < 200:
		print tweet(t, xht)
		i += 1
