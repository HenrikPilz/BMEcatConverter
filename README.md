# BMEcatConverter

## Build and Analysis Stat&#x016b;s
Overview about build and besting status as well as status of compliance of coding principles.

### CodeClimate

[![Test Coverage](https://api.codeclimate.com/v1/badges/c292f2fef2bebec76323/test_coverage)](https://codeclimate.com/repos/59d3e32587947702910006a6/test_coverage)

[![Maintainability](https://api.codeclimate.com/v1/badges/c292f2fef2bebec76323/maintainability)](https://codeclimate.com/repos/59d3e32587947702910006a6/maintainability)


### Circle CI

Build: [![CircleCI](https://circleci.com/gh/HenrikPilz/BMEcatConverter.svg?style=svg&circle-token=84c7ca4ac6fed76f1a113efb0fa4ddea1db3a7b2)](https://circleci.com/gh/HenrikPilz/BMEcatConverter)

### Scrutinizer

[![Code Coverage](https://scrutinizer-ci.com/b/contorion/bmecatconverter/badges/coverage.png?b=master&s=0d1533b61f1242d1681844224c30360bd22bb2c4)](https://scrutinizer-ci.com/b/contorion/bmecatconverter/?branch=master)

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/b/contorion/bmecatconverter/badges/quality-score.png?b=master&s=753fffe485486cf8661110b5289091f523e2c6fe)](https://scrutinizer-ci.com/b/contorion/bmecatconverter/?branch=master)

[![Build Status](https://scrutinizer-ci.com/b/contorion/bmecatconverter/badges/build.png?b=master&s=1ee396307d71cf85d657e3b0e30e75bc240b584f)](https://scrutinizer-ci.com/b/contorion/bmecatconverter/build-status/master)

[![Code Intelligence Status](https://scrutinizer-ci.com/b/contorion/bmecatconverter/badges/code-intelligence.svg?b=master&s=d11f2a9888d211bf8ea23e04fe83535672386a58)](https://scrutinizer-ci.com/code-intelligence)


## Introduction
The BMEcatConverter is a tool to convert BMEcats into a special Excel-Workbook (Mappiong-Master) and vice versa.

The first case, converting from BMEcat into Excel  covers the following aspects:
* The first Sheet is called 'Artikel'. It contains the following fields:
	- Article/Product
		- suplierArticleID
	- Article/ProductDetails
		- title(descriptionShort)
		- description(descriptionLong)
		- manufacturerArticleID
		- manufactuerName
		- GTIN
		- deliverytime
	- orderDetails
		- OrderUnit
		- ContentUnit
		- No_CU_per_OU
		- quantityMin
		- quantityInterval
		- priceQuantity
	- PriceDetails
		- Prices
	- MimeInfo
		- Mime
	- FeatureSets
		- Feature



