
import suffix_array

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
	used_escapes = []

	i = 0
	while True:

		if not escape_chars:
			break

		escape = escape_chars.pop(0)
		escape_len = len(escape)

		max_weight = 0
		for needle in list(matches):
			num_matches = script.count(needle)
			length = len(needle)
			weight = (
				(length * num_matches) -
				(length + (num_matches + 2) * escape_len)
			)

			if weight >= 1:
				if weight > max_weight:
					max_weight = weight
					max_needle = needle
					max_reps = num_matches
			else:
				matches.remove(needle)

		if not matches:
			break

		script = escape.join(script.split(max_needle) + [max_needle])

		matches = [
			escape.join(needle.split(max_needle))
			for needle in matches
			if needle != max_needle
		]

		used_escapes.append(escape)
		print '%2d: "%s" (%d)' % (i, max_needle, max_reps)

		i += 1

	quote = '"'
	decoder = ['_=','%s',';for(Y in $=','%s',')with(_.split($[Y]))_=join(pop());eval(_)']
	decoder = quote.join(decoder)
	script = decoder % (script, ''.join(used_escapes)[::-1])

	return script

#-------------------------------------------------------------------------------

def _find_matches(script):

	suffix = suffix_array.SuffixArray(script)
	dupes  = suffix.find_all_duplicates()

	matches = []
	for min_length, max_length, indices in dupes:
		start_pos = indices[0]
		for l in xrange(min_length, max_length+1):
			needle = script[start_pos:start_pos+l]
			matches.append(needle)

	return matches

#-------------------------------------------------------------------------------
