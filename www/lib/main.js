requirejs.config({
    baseUrl: '/lib',
    paths: {
        jquery: 'jquery/jquery-3.5.1.min',
        jqxcore: 'jqwidgets/jqxcore',
        jqxsplitter: 'jqwidgets/jqxsplitter',
        jqxbutton: 'jqwidgets/jqxbuttons',
        jqxdropdownlist: 'jqwidgets/jqxdropdownlist',
        jqxlistbox: 'jqwidgets/jqxlistbox',
        jqxscrollbar: 'jqwidgets/jqxscrollbar'
    },
    shim:{
        jqxcore : {
            deps : ['jquery']
          },
        jqxsplitter : {
            deps : ['jqxcore']
          },
        jqxdropdownlist : {
            deps : ['jqxlistbox']
          },
        jqxlistbox : {
            deps : ['jqxscrollbar']
          },
        jqxscrollbar : {
            deps : ['jqxbutton']
          },
        jqxbutton : {
            deps : ['jqxcore']
          }
    }
});

requirejs(['jquery', '/start.js'], function($, mod) {
  window.smcall = function(data, cb) {
    $.ajax({
      url: '/api',
      context: cb,
      method: 'POST',
      crossDomain: true,
      data: JSON.stringify(data),
      dataType: 'json'
    }).done(function(data) {
      this(data)
    })
  }
  mod.start()
})
