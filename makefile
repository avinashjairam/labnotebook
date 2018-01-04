all: example.html

example.html: example.ln labnote.py
	./labnote.py example.ln

