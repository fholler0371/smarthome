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


requirejs(['/start.js'], function(mod) {
  mod.start()
})
