define(['module'], function(module) {
  var sm_backend = {
    init : function() {
      console.log(window.module.sm_backend.init_data)
      if (window.module.sm_backend.init_data.p1 == 'scan') {
        window.module.sm_backend.scan()
      }
    },
    stop : function() {
    },
    scan : function() {
      window.smcall({'client': 'sm_backend', 'cmd':'scan', 'data': {}}, function(data) {
        window.head.get_menu()
      })
    }
  }
  sm_backend['init_data'] = window.module_const[module.id]
  window.module.sm_backend = sm_backend
  return sm_backend
})
