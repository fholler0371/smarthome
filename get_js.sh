#!/bin/bash

cd www/lib/requirejs
rm require.js
wget https://requirejs.org/docs/release/2.3.6/minified/require.js

cd ../jquery
wget https://code.jquery.com/jquery-3.5.1.min.js
