requirejs.config({
    baseUrl: '/lib',
    paths: {
        jquery: 'jquery/jquery-3.5.1.min',
        jqxcore: 'jqwidgets/jqxcore',
        jqxsplitter: 'jqwidgets/jqxsplitter'
    },
    shim:{
        jqxcore : {
            deps : ['jquery']
          },
        jqxsplitter : {
            deps : ['jqxcore']
          }
    }
});

requirejs(['jquery'], function( $ ) {
  $(document).ready(function() {
    $('body').append('<div id="mainSplitter"><div id="panel-master">Panel 1</div><div id="panel-clients">Panel 2</div></div>')
    requirejs(['jqxsplitter'], function() {
      $('#mainSplitter').jqxSplitter({height: '100%', width: '100%', orientation: 'horizontal', panels: [{ size: 100 }, { size: 300 }] });
      console.log( $ )
    });
  });
});
