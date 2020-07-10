requirejs.config({
    baseUrl: '/lib',
    paths: {
        jquery: 'jquery/jquery-3.5.1.min',
        datepicker: 'jquery/datepicker',
        jqxcore: 'jqwidgets/jqxcore',
        jqxsplitter: 'jqwidgets/jqxsplitter',
        jqxbutton: 'jqwidgets/jqxbuttons',
        jqxdropdownlist: 'jqwidgets/jqxdropdownlist',
        jqxlistbox: 'jqwidgets/jqxlistbox',
        jqxscrollbar: 'jqwidgets/jqxscrollbar',
        jqxdatatable: 'jqwidgets/jqxdatatable',
        jqxdata: 'jqwidgets/jqxdata',
        jqxtabs: 'jqwidgets/jqxtabs',
        jqxgrid: 'jqwidgets/jqxgrid',
        jqxgrid_selection: 'jqwidgets/jqxgrid.selection',
        jqxgrid_edit: 'jqwidgets/jqxgrid.edit',
        jqxcheckbox: 'jqwidgets/jqxcheckbox',
        jqxpanel: 'jqwidgets/jqxpanel',
        jqxinput: 'jqwidgets/jqxinput',
        jqxpasswordinput: 'jqwidgets/jqxpasswordinput',
        jqxnumberinput: 'jqwidgets/jqxnumberinput',
        jqxmenu: 'jqwidgets/jqxmenu',
        jqxwindow: 'jqwidgets/jqxwindow'
    },
    shim:{
        jqxcore : {
            deps : ['jquery']
          },
        jqxsplitter : {
            deps : ['jqxcore']
          },
        jqxgrid_selection : {
            deps : ['jqxgrid']
          },
        jqxgrid_edit : {
            deps : ['jqxgrid']
          },
        jqxtabs : {
            deps : ['jqxcore']
          },
        jqxsdata : {
            deps : ['jqxcore']
          },
        jqxdropdownlist : {
            deps : ['jqxlistbox']
          },
        jqxlistbox : {
            deps : ['jqxscrollbar']
          },
        jqxpanel : {
            deps : ['jqxscrollbar']
          },
        jqxscrollbar : {
            deps : ['jqxbutton']
          },
        jqxdatatable : {
            deps : ['jqxscrollbar', 'jqxdata']
          },
        jqxbutton : {
            deps : ['jqxcore']
          }
    }
});

requirejs(['jquery', '/start.js', 'jqxcore'], function($, mod) {
  window.smcall = function(data, cb) {
    if (('server' in window) && ('ip' in window.server)) {
      data.client = window.server.ip
    }
    token = sessionStorage.getItem("token")
    if (token != null) {
      data.token = token
    }
    $.ajax({
      url: '/api',
      context: cb,
      method: 'POST',
      crossDomain: true,
      data: JSON.stringify(data),
      dataType: 'json'
    }).done(function(data) {
      if (!data.login) {
        sessionStorage.removeItem("token")
        try {
          window.head.logout()
        } catch(err) {}
      } else {
        sessionStorage.setItem("token", data.token)
      }
      this(data)
    })
  }
//  $.jqx.theme = 'metrodark';
  $.jqx.theme = 'custom-scheme';
  mod.start()
})
