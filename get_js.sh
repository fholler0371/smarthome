#!/bin/bash

cd www/lib/requirejs
rm require.js
wget https://requirejs.org/docs/release/2.3.6/minified/require.js

cd ../jquery
rm jquery-3.5.1.min.js
wget https://code.jquery.com/jquery-3.5.1.min.js

cd ../jqwidgets
rm master.zip
wget https://github.com/jqwidgets/jQWidgets/archive/master.zip
rm -R jQWidgets-master
unzip -u master.zip
cp -R jQWidgets-master/jqwidgets/* ./
rm -R jQWidgets-master
