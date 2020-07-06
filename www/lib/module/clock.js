define(['module'], function(module) {
  var clock = {
    init : function() {
      console.log(window.module.clock.init_data)
    }
  }
  clock['init_data'] = window.module_const[module.id]
  window.module.clock = clock
  return clock
})
