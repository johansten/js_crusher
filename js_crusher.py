
#-------------------------------------------------------------------------------

def crush(script):

	escape_chars = [unichr(i).encode('utf-8') for i in range(1024)]
	escape_chars[:] = (
		escape_chars[32:128] +
		escape_chars[0:32] +
		escape_chars[128:1024])

	used_chars = set()
	used_chars.add('"')
	for s in script:
		used_chars.add(s)

	for c in used_chars:
		escape_chars.remove(c.decode('iso 8859-1').encode('utf-8'))

	#
	#
	#

	matches = _find_matches(script)
	escape_chars = []

	while True:

		if not escape_chars:
			break

		escape = escape_chars.pop(0)
		escape_len = len(escape)

		max_weight = 0
		for needle in list(matches):
			num_matches = script.count(needle)
			length = len(needle)
			weight = (length * num_matches) - length - (num_matches + 2)*escape_len
			if weight < 1:
				matches.remove(needle)
			else:
				if weight > max_weight:
					max_weight = weight
					max_needle = needle

		if not matches:
			break

		escape_chars.append(escape)

		s = script.split(max_needle)
		s.append(max_needle)
		script = escape.join(s)

		matches = set([
			escape.join(needle.split(max_needle))
			for needle in matches
			if needle != max_needle
		])

	quote = '"'
	decoder = ['_=','%s',';for(Y in $=','%s',')with(_.split($[Y]))_=join(pop());eval(_)']
	decoder = quote.join(decoder)
	script = decoder % (script, ''.join(escape_chars)[::-1])

	return script

#-------------------------------------------------------------------------------

def _find_matches(script):

	l = len(script)

	matches = set()
	for length in range(2, l/2):
		for n in range(l - length):
			needle = script[n:n+length]
			num_matches = len(script.split(needle)) - 1
			if num_matches >= 2:
				matches.add(needle)

	return matches

#-------------------------------------------------------------------------------

