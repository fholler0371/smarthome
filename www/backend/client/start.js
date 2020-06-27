define(['jquery'], function($) {
  return {
    start : function() {
      requirejs(['/lib/client.js'], function(mod) {
        window.client = mod.start
        window.client.init()
      })
    }
  }
})
