define(['jquery'], function($) {
  return {
    start : function() {
//      requirejs(['/lib/head.js'], function(mod) {
//        mod.init()
//      })
      requirejs(['/lib/client.js'], function(mod) {
        window.client = mod.start
        window.client.init()
      })
    }
  }
})
