# pyogctest

`pyogctest` is a Python tool to run OGC test suites from your terminal. This is
done by using the REST API provided by
[Teamengine](http://opengeospatial.github.io/teamengine/#). Then the resulting
XML report is parsed and displayed to be humanly readable "à la" `pytest` (as
much as possible).

`pyogctest` have been developed and tested with [QGIS
Server](https://docs.qgis.org/3.10/en/docs/server_manual/index.html) thanks to
[QGIS.org](https://www.qgis.org/en/site/). However, there's nothing specific to
QGIS Server itself (excepted for the HTML report CSS theme), so it should work
with other map servers too (while not tested).


## Install

To install Python dependencies:

```` python
$ git clone https://github.com/pblottiere/pyogctest
$ cd pyogctest
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -e .
````

Some system dependencies are also necessary:

- `docker` because Teamengine is used through Docker images provided on
  [Dockerhub](https://hub.docker.com/u/ogccite).
- `xmlstarlet` to convert a XML document into a HTML report (useful when the
  `html` format option is activated)


## Usage

`pyogctest` allows to run OGC tests on a map server instance, so the first
thing you need is an URL pointing to the map server itself. In this
documentation, we're going to use an online instance of QGIS Server (the one
used for official certifications).

To run the WMS 1.3.0 test suites:

```` bash
$ ./pyogctest.py -s wms130 http://qgis4.qgis.org:8080/certification_qgisserver_master
======================================== OGC test session starts =========================================
testsuite: WMS 1.3.0
collected 183 items

data-independent ...................................................................................................................................................................
data-preconditions .
basic ......
recommendations .........
queryable .........

======================================== 183 passed in 69 seconds ========================================
````

If you want more details about tests, you can use the `-v` option:

```` bash
$ ./pyogctest.py -s wms130 -v http://qgis4.qgis.org:8080/certification_qgisserver_master
======================================== OGC test session starts =========================================
testsuite: WMS 1.3.0
collected 183 items

data-independent::basic_elements::param-rules::extra-GetMap-param PASSED
data-independent::basic_elements::param-rules::extra-GetFeatureInfo-param PASSED
data-independent::basic_elements::param-rules::extra-GetCapabilities-param PASSED
data-independent::basic_elements::version-negotiation::negotiate-no-version PASSED
...
````
