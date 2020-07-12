define(['module'], function(module) {
  var sm_backend = {
    init : function() {
      console.log(window.module.sm_backend.init_data)
      if (window.module.sm_backend.init_data.p1 == 'scan') {
        window.module.sm_backend.scan()
      }
      if (window.module.sm_backend.init_data.p1 == 'client') {
        window.module.sm_backend.client(window.module.sm_backend.init_data.p2, window.module.sm_backend.init_data.p3)
      }
    },
    stop : function() {
      $('#head_title').text('')
    },
    scan : function() {
      window.smcall({'client': 'sm_backend', 'cmd':'scan', 'data': {}}, function(data) {
        window.head.get_menu()
      })
    },
    client : function(ip, name) {
      window.smcall({'client': 'sm_backend', 'cmd':'get_plugins', 'data': {'ip':ip}}, function(data) {
        console.info(data)
      })
      $('#head_title').text(name)
      html = '<div id="sm_backend_menu"></div><div id="sm_backend_content"></div>'
      $('#client_area').html(html)
    }
  }
  sm_backend['init_data'] = window.module_const[module.id]
  window.module.sm_backend = sm_backend
  $('head').append('<link href="/lib/module/sm_backend.css" type="text/css" rel="stylesheet" />')
  return sm_backend
})
