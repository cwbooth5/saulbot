
corpus.txt: $(wildcard *.log)
	./log2mc.py $^ > $@

