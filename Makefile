SHELL := /bin/bash
cwd := $(shell pwd)
ui_path =${cwd}/cesi/ui

release: build-ui clean
	@echo 'Releasing...'
	tar -czvf ${cwd}/../cesi-extended.tar.gz .

build-ui: install-ui
	@echo 'Building UI'
	pushd ${ui_path}; \
	yarn build; \
	tar -czvf ${cwd}/../build-ui.tar.gz build; \
	popd;
	@echo 'Builded UI'

install-ui:
	@echo 'Installing dependecies for UI'
	pushd ${ui_path}; \
	yarn install; \
	popd;
	@echo 'Installed dependecies for UI'

clean-ui-node-modules:
	pushd ${ui_path}; \
	rm -rf node_modules; \
	popd;


clean: clean-ui-node-modules
	@echo 'Cleaning...'
	rm -f *.db *.log
	rm -f */*.db */*.log
	@echo 'Cleaned'
