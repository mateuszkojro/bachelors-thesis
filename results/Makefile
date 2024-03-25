collect: ./recordings/ ./results/
	python3 ./combine_folders.py

collect_metadata: collect
	python3 ./collect_metadata.py ./combined/

filter: collect_metadata
	python3 ./filter.py ./combined/

combine: filter
	python3 ./combine.py ./combined/

clean:
	rm -rf ./combined