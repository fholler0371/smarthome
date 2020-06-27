define(['jquery'], function($) {
  return {
    start : {
      init : function() {
        requirejs(['jqxsplitter'], function() {
          $('#client_area').html('<div id="clint_left"></div><div id="clint_right"></div>')
          $('#client_area').jqxSplitter({height: '100%', width: '100%', panels: [{ size: 400, min: 250}, {min: 250}]})
        })
      }
    }
  }
})
