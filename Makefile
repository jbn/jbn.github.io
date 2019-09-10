SOURCES := $(shell find * -type f -name "*.ipynb" | grep -v ".ipynb_checkpoints")
OBJECTS := $(SOURCES:.ipynb=.html)
MD_OBJS := $(SOURCES:.ipynb=.md)


.PHONY: build
build: $(OBJECTS)
	@echo "DONE!"

.PHONY: serve
serve: 
	python -m http.server 8001

%.html: %.md
	pandoc \
	   --template=templates/post.html -s $< -o $@
	rm $<

%.md: %.ipynb
	jupyter nbconvert --config config/nb_config.py --to markdown $<
	./bin/build_md_header.py $< > $@.tmp
	cat $@ | ./bin/empty_cell_kludge.py >> $@.tmp
	mv $@.tmp $@

.PHONY: clean
clean:
	rm -f $(OBJECTS)
	rm -f $(MD_OBJS)

.PHONY: rebuild
rebuild: clean build


