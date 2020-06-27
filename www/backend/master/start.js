define(['jquery'], function($) {
  return  {
    start : function() {
      window.server = {}
      window.server.hosts = []

      html = '<div id="mainSplitter"><div id="panel-master"><div id="host_select"></div>'
      html += '<input type="button" value="Scannen nach Clients" id="scan" />'
      html += '</div><div style="height: 100%, width: 100%"><div id="client_area"><h1>'
      $('body').append(html + '<p style="text-align: center">Bitte Client aussuchen</p></h1></div></div></div>')

      get_remote_hosts = function() {
        window.smcall({cmd:'get_remote_hosts'}, function(data) {
          window.server.hosts = data.hosts
          hosts = []
          var arrayLength = data.hosts.length;
          for (var i = 0; i < arrayLength; i++) {
            hosts.push(data.hosts[i].hostname);
          }
          $("#host_select").jqxDropDownList({source: hosts})
        })
      }
      check_scan_state = function() {
        window.smcall({cmd:'get_scan_state'}, scan_state)
      }
      scan_state = function(data) {
        if (data.scan_state) {
          setTimeout(check_scan_state, 2500)
        } else {
          get_remote_hosts()
        }
      }

      requirejs(['jqxsplitter', 'jqxbutton', 'jqxdropdownlist'], function() {
        $('#mainSplitter').jqxSplitter({height: '100%', width: '100%', orientation: 'horizontal', resizable: false,
            panels: [{size: 60 }, { size: 300 }] })
        $("#scan").jqxButton({ width: 200, height: 40 }).css('margin', '10px').css('float', 'right').on('click', function() {
          window.smcall({cmd:'scan_clients'}, scan_state)
        });
        $("#host_select").jqxDropDownList({ source: [], placeHolder: "Host aussuchen", width: 250, height: 40}).css('margin', '10px')
            .css('float', 'left')
        $($("#host_select").find('label')[0]).hide()
        $("#host_select").on('change', function (event) {
          var args = event.args;
          if (args) {
            var item = args.item
            window.server.host = item.label
            var arrayLength = window.server.hosts.length;
            for (var i = 0; i < arrayLength; i++) {
              if (item.label == window.server.hosts[i].hostname) {
                window.server.ip = window.server.hosts[i].ip
              }
            }
            window.client.init()
          }
        })
        get_remote_hosts()
        requirejs(['/lib/client.js'], function(mod) {
          window.client = mod.start
        })
      });
    }
  }
});
