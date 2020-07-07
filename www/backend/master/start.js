define(['jquery'], function($) {
  return  {
    start : function() {
      requirejs(['/lib/head.js'], function(mod) {
        mod.init()
      })
    }
  }
});
