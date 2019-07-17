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
	@echo 'Installing all dependecies of UI'
	pushd ${ui_path}; \
	yarn install; \
	popd;
	@echo 'Installed all dependecies of UI'

remove-ui-node-modules:
	pushd ${ui_path}; \
	rm -rf node_modules; \
	popd;

remove-python-cache-files:
	find . -type d -name '__pycache__' -exec rm -r {} +

remove-project-cache-files:
	find . -type f -name '*.log' -exec rm {} +
	find . -type f -name '*.db' -exec rm {} +

clean: remove-ui-node-modules remove-python-cache-files remove-project-cache-files

upgrade: upgrade-all-dependecies-of-ui

upgrade-all-dependecies-of-ui:
	@echo 'Upgrading all dependecies of UI'
	pushd ${ui_path}; \
	yarn upgrade --latest; \
	popd;
	@echo 'Upgradedd all dependecies of UI'

