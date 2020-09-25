from subprocess import PIPE, run, STDOUT

def build_python(input_code: str):
	# Exec path
	pypath = '/Library/Frameworks/Python.framework/Versions/3.8/bin/python3'

	# Save user's python to a file THIS IS BAD
	print(input_code)

	file = open('bad/usercode.py', 'w')
	file.write(input_code)
	file.close()

  # Run the file THIS IS WORSE
	proc = run([pypath, 'bad/usercode.py'], stderr=STDOUT, stdout=PIPE)
	print(proc)

	out = proc.stdout

	return out