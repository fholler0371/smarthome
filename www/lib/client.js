define(['jquery'], function($) {
  return {
    start : {
      init : function() {
        window.client_data = {}
        requirejs(['jqxsplitter', 'jqxlistbox'], function() {
          $('#client_area').html('<div id="clint_left"><div id="client_plugins"></div></div><div id="clint_right"></div>')
          $('#client_area').jqxSplitter({height: '100%', width: '100%', panels: [{ size: 400, min: 250}, {min: 250}]})
          window.smcall({cmd:'client_get_plugins'}, function(data) {
            window.client_data.plugins = data.plugins
            var plugins = []
            var arrayLength = data.plugins.length
            for (var i = 0; i < arrayLength; i++) {
              plugins.push(data.plugins[i].label);
            }
            $('#client_plugins').jqxListBox({width: '100%', height: '100%', itemHeight: 40, source: plugins})
            $('#client_plugins').on('select', function(event) {
              var args = event.args;
              if (args) {
                var index = args.index
                window.client_data.plugin = window.client_data.plugins[index]
                requirejs(['plugins/' + window.client_data.plugin.name], function() {
                  console.log(window.client_data)
                })
              }
            })
          })
        })
      }
    }
  }
})
