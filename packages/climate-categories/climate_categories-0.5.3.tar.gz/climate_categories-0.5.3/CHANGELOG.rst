=========
Changelog
=========

0.5.3 (2021-10-12)
------------------

* Add gas categorization which includes commonly used climate forcing substances.

0.5.2 (2021-05-18)
------------------

* Add IPCC2006_PRIMAP categorization.
* Add refrigerant sub-classes and additional codes to CRFDI_class.

0.5.1 (2021-05-04)
------------------

* Add BURDI, CRFDI, BURDI_class, and CRFDI_class categorizations and scripts to generate
  them from the UNFCCC DI flexible query API.

0.5.0 (2021-03-23)
------------------

* Switch ``to_yaml()`` output to ruamel.yaml so that valid, correctly typed YAML 1.2
  is written. This should enable easier re-use of the data in other contexts.
* Consistently use title case for titles in IPCC categorizations.

0.4.0 (2021-03-17)
------------------

* Add more unit tests.
* Add consistency tests for IPCC categorizations.
* Update documentation.
* Add data format documentation.

0.3.2 (2021-03-16)
------------------

* Use tbump for simpler versioning.

0.3.1 (2021-03-16)
------------------

* Properly include data files in binary releases.

0.3.0 (2021-03-16)
------------------

* Add IPCC1996 categorization and scripts to generate it from the source pdf.
* Change packaging to declarative style.
* Automate generation of pickled files via Makefile.
* Automate loading of included categorizations.

0.2.2 (2021-03-09)
------------------

* Re-release again to trigger zenodo.

0.2.1 (2021-03-09)
------------------

* Re-release to include correct changelog.

0.2.0 (2021-03-09)
------------------

* Introduce API for multiple codes and multiple children.
* Implement classes and functions.
* Add IPCC2006 categorization and scripts to generate it from the source pdf.

0.1.0 (2021-01-18)
------------------

* First release on PyPI.
* Contains documentation and a stub API for querying, but no working code yet.
