requirejs.config({
    baseUrl: '/lib',
    paths: {
        jquery: 'jquery/jquery-3.5.1.min'
    }
});

requirejs(['jquery'], function( $ ) {
  $(document).ready(function() {
    $('body').append('<div id="mainSplitter"><div id="panel-master">Panel 1</div><div id="panel-clients">Panel 2</div></div>')
    console.log( $ )
  });
});
