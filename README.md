# BMEcatConverter

## Build and Analysis Stat<span style="text-decoration: overline;">u</span>s
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

## Prerequisites
In order to use the BMEcatConverter you need a python installation. The Python version, for which this Converter was developed is [python 3.4.4](https://www.python.org/ftp/python/3.4.4/python-3.4.4.amd64.msi) due to its availability as an Windows Installer.
It should be able to run on higher version as well.
Please make sure you added python to the _path_-Environmentvariable and that you installed the _*requirements.txt*_ within a commandline shell with administrator permissions using _*pip install -r requirements.txt*_.

## Introduction
The BMEcatConverter is a tool to convert BMEcats into a special Excel-Workbook (Mappiong-Master) and vice versa.

*	The first case, converting from BMEcat into Excel, which result in a workbook with three sheets:
	-	Article Data - all the data belonging to one article is in one row (This is called _Mapping-Master_-Format.)
	-	Article Relations - the relation between two articles is defined in one row
	-	Search Words per Article - one row contains all searchwords, for this article
*	The second case is converting from an Excel-Workbook \(Mapping-Master\)
	The outcome is a [BMEcat Version 1.2](https://www.bme.de/fileadmin/content/Initativen/BMEcat/Download_BMEcat_1.2/BMEcatV12e.pdf). The BMEcat contains only one featureset per article. 

## Usage
## Default behavior
The BMEcat-Converter has to be used with the following arguments:

*	-i "%path_to_inputfile%"
	this can be a relative or absolute path, it has to be either an Excelfile \(\*.xlsm or \*.xlsx\) or a BMEcat-file \(\*.xml\).
*	-o "%path_to_outputfile%"
	this can be a relative or absolute path, it has to be either an Excelfile \(\*.xlsm or \*.xlsx\) or a BMEcat-file \(\*.xml\).
*	\-\-dateformat="%Y-%m-%d"
	the dateformat has to be provided, if you convert from XML to Excel \(Case one\). You can usually derive the dateformat from the generation date of the BMEcat.	If you use a _*cmd*_-file for running the converter you should escape the percentage sign by double-typing, i.e., "%%Y-%%m-%%d".

Thus with calling _*python src/main.py -i "%path_to_inputfile%" -o "%path_to_outputfile%"*_ will work if you convert from an Excelfile to a BMEcat.

The following options are set to default values:

*	-	dateformat
*	\-\-merchant="fiege"
	Default merchant dissolves to _*fiege*_, this means if an validation fails, an exception is raised and the conversion fails.
*	\-\-manufacturer=None
	Default Manufacturer if no manufacturername is provided in the BMEcat.
*	\-\-separators=autodetect
	Default is _*autodetect*_, which tries to resolve the thousands- and decimalseparator
	three states are possible
	-	autodetect:
		tries to autodetect thousands- and decimalseparators
	-	

### Additional options
The options can be changed as follows:

*	\-\-dateformat
*	\-\-merchant="fiege"
	In order to loosen the validationrules one could set a merchant with the option *\-\-merchant="MerchantName*.
	_*fiege*_ means if an validation fails, an exception is raised and the conversion fails.
	_*anything_else*_ only writes warnings but will create a BMEcat if nothing really bad is inserted.
*	\-\-manufacturer
*	\-\-separators=autodetect
	three states are possible
	-	autodetect:
		tries to autodetect thousands- and decimalseparators
	-	english:
		set thousandsseparator to comma and decimalseparator to dot.
	-	german:
		set thousandsseparator to dot and decimalseparator to comma.

## Detailed Information
The first case, converting from BMEcat into Excel covers the following aspects:

*	The first sheet is called 'Artikel'. It contains the following fields:
	-	Article/Product
		-	suplierArticleID
	-	Article/ProductDetails
		-	title(descriptionShort)
		-	description(descriptionLong)
		-	manufacturerArticleID
		-	manufactuerName
		-	GTIN
		-	deliverytime
	-	orderDetails
		-	OrderUnit
		-	ContentUnit
		-	No_CU_per_OU
		-	quantityMin
		-	quantityInterval
		-	priceQuantity
	-	PriceDetails
		-	Prices
			-	validFrom
			-	validTo
			-	priceType
			-	priceAmount
			-	priceCurrency
			-	tax1
			-	priceFactor1
			-	lowerBound1
	-	MimeInfo
		-	Mime
			-	mimeType1
			-	mimeSource1
			-	mimeDescription1
			-	mimePurpose1
			-	mimeOrder1
	-	FeatureSets
		-	Feature
			-	attributeName1
			-	attributeValue1
			combination of value and unit
*	The second sheet is called 'Artikelbeziehungen'. It contains all relations between all articles in the BMEcat. Every row contains one relation.
	The columns are named as follows:
	-	supplierArticleId
	-	referencType
	-	referencedSupplierArticleId
*	The third sheet is called 'Artikelsuchbegriffe'. It contains all searchwords for all articles. One row contains all searchwords for one article.
	The columns are named as follows:
	-	supplierArticleId
	-	keywords