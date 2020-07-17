define(['module', 'jqxlistbox'], function(module) {
  var sm_backend = {
    init : function() {
      if (window.module.sm_backend.init_data.p1 == 'scan') {
        window.module.sm_backend.scan()
      }
      if (window.module.sm_backend.init_data.p1 == 'client') {
        window.module.sm_backend.client(window.module.sm_backend.init_data.p2, window.module.sm_backend.init_data.p3)
      }
    },
    stop : function() {
      $('#client_area').removeData('min')
      $('#head_title').text('')
    },
    scan : function() {
      window.smcall({'client': 'sm_backend', 'cmd':'scan', 'data': {}}, function(data) {
        window.head.get_menu()
      })
    },
    client : function(ip, name) {
      $('#head_title').text(name)
      window.module.sm_backend.ip = ip
      html = '<div id="sm_backend_menu"><div id="client_plugins"></div></div><div id="sm_backend_content"></div>'
      $('#client_area').html(html)
      $('#client_area').data('min', 'sm_backend')
      window.module.sm_backend.setMinMenu()
      window.smcall({'client': 'sm_backend', 'cmd':'get_plugins', 'data': {'ip':ip}}, function(data) {
        window.module.sm_backend.plugins = data.data.plugins
        var plugins = []
        var arrayLength = data.data.plugins.length
        for (var i = 0; i < arrayLength; i++) {
          plugins.push(data.data.plugins[i].label);
        }
        $('#client_plugins').jqxListBox({selectedIndex: 0, width: '100%', height: '100%', itemHeight: 40, source: plugins})
        $('#client_plugins').on('select', function(event) {
          var args = event.args;
          if (args) {
            var index = args.index
            window.module.sm_backend.plugin = window.module.sm_backend.plugins[index]
            if (window.module.sm_backend.plugin.name in window.module.sm_backend.sm_clients) {
              window.module.sm_backend.sm_clients[window.module.sm_backend.plugin.name].func()
            } else {
              requirejs(['sm_plugins/' + window.module.sm_backend.plugin.name], function(mod) {
                window.module.sm_backend.sm_client[window.module.sm_backend.plugin.name] = mod
                window.module.sm_backend.sm_client[window.module.sm_backend.plugin.name].func()
              })
            }
          }
        })
        window.module.sm_backend.plugin = window.module.sm_backend.plugins[0]
        requirejs(['sm_plugins/' + window.module.sm_backend.plugin.name], function(mod) {
          window.module.sm_backend.sm_client[window.module.sm_backend.plugin.name] = mod
          window.module.sm_backend.sm_client[window.module.sm_backend.plugin.name].func()
        })
      })
    },
    setMinMenu : function() {
      if ($('#mainTop').hasClass('leftMenuSmall')) {
        $('#sm_backend_menu').css('width', 0)
        $('#sm_backend_content').css('width', '100%')
        $('#sm_backend_content').css('left', '0')
      } else {
        var w = $('.leftMenu').width()
        $('#sm_backend_menu').width(w)
        $('#sm_backend_content').css('width', 'calc( 100% - '+w+'px )')
        $('#sm_backend_content').css('left', w+'px')
        $('#client_plugins').jqxListBox('render')
      }
    },
    plugins : undefined,
    sm_clients : [],
    sm_client : [],
    ip : ''
  }
  sm_backend['init_data'] = window.module_const[module.id]
  window.module.sm_backend = sm_backend
  $('head').append('<link href="/lib/module/sm_backend.css" type="text/css" rel="stylesheet" />')
  return sm_backend
})
