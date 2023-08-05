PYEXE	= python3

info:
	$(PYEXE) -c "import sys, time; print('sys.hash_info.width', sys.hash_info.width, 'epoch', time.gmtime(0))"

PRODUCT = Product
B_PRODUCT = BaseProduct
PYDIR	= fdi/dataset
RESDIR	= $(PYDIR)/resources
P_PY	= $(shell $(PYEXE) -S -c "print('$(PRODUCT)'.lower())").py
B_PY	= $(shell $(PYEXE) -S -c "print('$(B_PRODUCT)'.lower())").py
B_INFO	= $(B_PY)
P_YAML	= $(RESDIR)/$(PRODUCT).yml
B_YAML	= $(RESDIR)/$(B_PRODUCT).yml
P_TEMPLATE	= $(RESDIR)
B_TEMPLATE	= $(RESDIR)
ARRAYD	= ArrayDataset_DataModel
ARRAYD_PY=$(shell $(PYEXE) -S -c "print('$(ARRAYD)'.lower())").py
ARRAYD_YAML	= $(RESDIR)/$(ARRAYD).yml
TABLED	= TableDataset_DataModel
TABLED_PY=$(shell $(PYEXE) -S -c "print('$(TABLED)'.lower())").py
TABLED_YAML	= $(RESDIR)/$(TABLED).yml
UNSTRUCTUREDD	= UnstructuredDataset_DataModel
UNSTRUCTUREDD_PY=$(shell $(PYEXE) -S -c "print('$(UNSTRUCTUREDD)'.lower())").py
UNSTRUCTUREDD_YAML	= $(RESDIR)/$(UNSTRUCTUREDD).yml

py: $(PYDIR)/$(B_PY) $(PYDIR)/$(P_PY) $(PYDIR)/$(ARRAYD_PY) $(PYDIR)/$(TABLED_PY) $(PYDIR)/$(UNSTRUCTUREDD_PY)

$(PYDIR)/$(P_PY): $(PYDIR)/yaml2python.py $(P_YAML) $(P_TEMPLATE)/$(PRODUCT).template $(PYDIR)/$(B_PY)
	$(PYEXE) -m fdi.dataset.yaml2python -y $(RESDIR) -t $(P_TEMPLATE) -o $(PYDIR) $(Y)


$(PYDIR)/$(B_PY): $(PYDIR)/yaml2python.py $(B_YAML) $(B_TEMPLATE)/$(B_PRODUCT).template 
	$(PYEXE) -m fdi.dataset.yaml2python -y $(RESDIR) -t $(P_TEMPLATE) -o $(PYDIR) $(Y)

$(PYDIR)/$(ARRAYD_PY)  $(PYDIR)/$(TABLED_PY) $(PYDIR)/$(UNSTRUCTUREDD_PY): $(PYDIR)/yaml2python.py $(ARRAYD_YAML) $(RESDIR)/$(ARRAYD).template $(TABLED_YAML) $(RESDIR)/$(TABLED).template  $(UNSTRUCTUREDD_YAML) $(RESDIR)/$(UNSTRUCTUREDD).template 
	$(PYEXE) -m fdi.dataset.yaml2python -y $(RESDIR) -t $(RESDIR) -o $(PYDIR) $(Y)

yamlupgrade: 
	$(PYEXE) -m fdi.dataset.yaml2python -y $(RESDIR) -u


.PHONY: runserver runpoolserver reqs install uninstall vtag FORCE \
	test test1 test2 test3 test4 test5\
	plots plotall plot_dataset plot_pal plot_pns \
	docs docs_api docs_plots docs_html \
	pipfile

# extra option for 'make runserver S=...'
S	=
# default username and password are in pnsconfig.py
runserver:
	$(PYEXE) -m fdi.pns.runflaskserver --username=foo --password=bar -v $(S)
runpoolserver:
	$(PYEXE) httppool_app.py --username=foo --password=bar --server=httppool_server $(S)

EXT	=
PKGS	= requests filelock ruamel.yaml tabulate paho-mqtt
PKGSDEV	=pytest pytest-cov aiohttp Flask Flask_HTTpAuth
PKGSDEP	= waitress twine sphinx_rtd_theme sphinx-copybutton

PIPOPT  = --disable-pip-version-check --no-color
install:
	$(PYEXE) -m pip install $(PIPOPT) -e .$(EXT) $(I)

uninstall:
	$(PYEXE) -m pip uninstall $(PIPOPT) fdi  $(I)

addsubmodule:
	git submodule add  --name leapseconds https://gist.github.com/92df922103ac9deb1a05 ext/leapseconds

update:
	git submodule update --init --recursive --remote

PNSDIR=~/pns
installpns:
	mkdir -p $(PNSDIR)
	$(MAKE) uninstallpns
	for i in init run config clean; do \
	  cp fdi/pns/resources/$${i}PTS.ori  $(PNSDIR); \
	  ln -s $(PNSDIR)/$${i}PTS.ori $(PNSDIR)/$${i}PTS; \
	done; \
	mkdir -p $(PNSDIR)/input $(PNSDIR)/output
	if id -u apache > /dev/null 2>&1; then \
	chown apache $(PNSDIR) $(PNSDIR)/*PTS.ori $(PNSDIR)/input $(PNSDIR)/output; \
	chgrp apache $(PNSDIR) $(PNSDIR)/*PTS* $(PNSDIR)/input $(PNSDIR)/output; \
	fi

uninstallpns:
	for i in init run config clean; do \
	  rm -f $(PNSDIR)/$${i}PTS* $(PNSDIR)/$${i}PTS.ori*; \
	done; \
	rm -f $(PNSDIR)/.lock $(PNSDIR)/hello.out || \
	sudo rm -f $(PNSDIR)/.lock $(PNSDIR)/hello.out

PYREPO	= pypi
INDURL	= 
#PYREPO	= testpypi
#INDURL	= --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/
LOCAL_INDURL	= $(CURDIR)/dist/*.whl --extra-index-url https://pypi.org/simple/
wheel:
	# git ls-tree -r HEAD | awk 'print $4' > MANIFEST
	rm -rf dist/* build *.egg-info
	$(PYEXE) setup.py sdist bdist_wheel
	twine check dist/*
	check-wheel-contents dist
upload:
	$(PYEXE) -m twine upload --repository $(PYREPO) dist/*

virtest:
	rm -rf /tmp/fditestvirt
	virtualenv -p $(PYEXE) /tmp/fditestvirt
	. /tmp/fditestvirt/bin/activate && \
	$(PYEXE) -m pip uninstall -q -q -y fdi ;\
	$(PYEXE) -m pip cache remove -q -q -q fdi ;\
	$(PYEXE) -m pip install $(LOCAL_INDURL) "fdi" && \
	$(PYEXE) -m pip show fdi && \
	echo Testing newly installed fdi ... ; \
	$(PYEXE) -c 'import sys, fdi.dataset.arraydataset as f; a=f.ArrayDataset(data=[4,3]); sys.exit(0 if a[1] == 3 else a[1])' && \
	$(PYEXE) -c 'import sys, pkgutil as p; sys.stdout.buffer.write(p.get_data("fdi", "dataset/resources/Product.template")[:100])' && \
	deactivate

J_OPTS	= ${JAVA_OPTS} -XX:MaxPermSize=256M -Xmx1024M -DloggerPath=conf/log4j.properties
J_OPTS	= ${JAVA_OPTS} -Xmx1024M -DloggerPath=conf/log4j.properties
VERYOLD	=-t ../swagger-codegen/modules/swagger-codegen/src/main/resources/flaskConnexion
FCTEMPL	=../swagger-codegen-generators/src/main/resources/handlebars/pythonFlaskConnexion/
AGS	=  -vv
SWJAR	= ../swagger-codegen/swagger-codegen-cli-3.0.25.jar
# The one below is not working probably because mvn is not working
#SWJAR	= ../swagger-codegen/modules/swagger-codegen-cli/target/swagger-codegen-cli.jar

SCHEMA_DIR	=fdi/httppool/schema
# so that flsgger can understand.
de-ref:
	swagger-cli bundle  -t yaml ${SCHEMA_DIR}/pools.yml -o ${SCHEMA_DIR}/pools_resolved.yml

# make swagger server subs
api:
	rm -rf fdi/httppool/flaskConnexion/*
	java $(J_OPTS) -jar $(SWJAR) generate $(AGS) -i ./fdi/httppool/schema/pools.yml -l python-flask -o ./fdi/httppool/swagger -Dservice -DpackageName=fdi.httppool.swagger -DpackageVersion=2.0 -DserverPort=9000

# $ref: works, unlike swagger editor
watchapi:
	swagger-ui-watcher fdi/httppool/schema/pools.yml

swagger-editor:
	@echo browser open file:///d:/code/swagger-editor/index.html
reqs:
	pipreqs --ignore tmp --force --savepath requirements.txt.pipreqs

gitadd:
	git add LICENSE README.rst CHANGELOG.rst setup.py MANIFEST.in \
	.gitignore noxfile.py Makefile .gitmodules .gitlab-ci.yml \
	.readthedocs.yml .dockerignore CONTRIBUTORS
	git add bin/reinstall bin/installpns bin/update
	git add resources
	git add fdi/*.py
	git add fdi/dataset/*.py fdi/dataset/resources
	git add fdi/pns/*.py fdi/pns/resources
	git add fdi/pal/*.py fdi/pal/resources
	git add fdi/utils/*.py
	git add fdi/httppool
	git add tests/*.py tests/resources tests/serv/*.py tests/serv/resources
	git add docs/sphinx/index.rst docs/sphinx/usage docs/sphinx/api \
	docs/sphinx/conf.py docs/sphinx/Makefile \
	docs/sphinx/_static docs/sphinx/_templates

# update _version.py and tag based on setup.py
# VERSION	= $(shell $(PYEXE) -S -c "from setuptools_scm import get_version;print(get_version('.'))")
# @ echo update _version.py and tag to $(VERSION)


VERSIONFILE	= fdi/_version.py
VERSION	= $(shell $(PYEXE) -S -c "_l = {};f=open('$(VERSIONFILE)'); exec(f.read(), None, _l); f.close; print(_l['__version__'])")

vtag:
	@ echo  version = \"$(VERSION)\" in $(VERSIONFILE)
	git tag  $(VERSION)
	git push origin $(VERSION)

PYTEST	= python3 -m pytest
TESTLOG	= /tmp/fdi-tests.log
L	= INFO #WARNING
OPT	= -r P -v --no-cov-on-fail --no-cov -l --pdb -s --show-capture=all  --log-level=$(L)
T	= 
test: test1 test2 test5

testpns: test4

testhttp: test6 test7 test8 test9

test1: 
	$(PYTEST) tests/test_dataset.py -k 'not _mqtt' --cov=fdi/dataset $(OPT) $(T)

test2:
	$(PYTEST) tests/test_pal.py -k 'not _http' $(T) --cov=fdi/pal $(OPT)

test3:
	$(PYTEST)  $(OPT) -k 'server' $(T) tests/serv/test_pns.py --cov=fdi/pns

test4:
	$(PYTEST) $(OPT) -k 'not server' $(T) tests/serv/test_pns.py --cov=fdi/pns

test5:
	$(PYTEST)  $(OPT) $(T) tests/test_utils.py --cov=fdi/utils

test6:
	$(PYTEST) $(OPT) $(T) tests/serv/test_httppool.py

test7:
	$(PYTEST) $(OPT) $(T) tests/serv/test_httpclientpool.py

test8:
	$(PYTEST) $(OPT) $(T) tests/test_pal.py -k '_http'

test9:
	$(PYTEST) tests/test_dataset.py -k '_mqtt' $(T)


FORCE:

PLOTDIR	= $(SDIR)/_static
plots: plot_dataset plot_pal plot_pns

plotall:
	pyreverse -o png -p all fdi/dataset fdi/pal fdi/pns fdi/utils
	mv classes_all.png packages_all.png $(PLOTDIR)

qplot_%: FORCE
	pyreverse -o png -p $@ fdi/$@
	mv classes_$@.png packages_$@.png $(PLOTDIR)


plot_dataset:
	pyreverse -o png -p dataset fdi/dataset
	mv classes_dataset.png packages_dataset.png $(PLOTDIR)

plot_pal:
	pyreverse -o png -p pal fdi/pal
	mv classes_pal.png packages_pal.png $(PLOTDIR)

plot_pns:
	pyreverse -o png -p pns fdi.pns
	mv classes_pns.png packages_pns.png $(PLOTDIR)

DOCSDIR	= docs
SDIR = $(DOCSDIR)/sphinx
APIOPT	= -T -M --ext-viewcode
APIOPT	= -M --ext-viewcode

docs: docs_api docs_plots docs_html

docs_api:
	rm -rf $(SDIR)/api/fdi
	mkdir -p  $(SDIR)/api/fdi
	sphinx-apidoc $(APIOPT) -o $(SDIR)/api/fdi fdi

docs_plots:
	rm  $(PLOTDIR)/classes*.png $(PLOTDIR)/packages*.png ;\
	make plots

docs_html:
	cd $(SDIR) && make html

########
# docker
########

build_docker \
launch_docker \
build_server \
launch_server \
rm_docker \
rm_dockeri \
it \
t \
i \
push_docker \
push_server \
pull_server \
vol \
backup_server \
restore_server \
restore_test \
update_docker:
	$(MAKE) --no-print-directory -f Makefile_docker.mk -C . $@


