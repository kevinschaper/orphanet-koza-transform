#!/bin/sh

iconv -f ISO-8859-1 -t utf-8 data/en_product6.xml | xq '.JDBOR.DisorderList.Disorder' > data/en_product6.json
