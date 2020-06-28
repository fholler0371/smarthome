define(['jquery', 'jqxinput', 'jqxnumberinput', /**/'jqxdatatable', 'jqxtabs', 'jqxdata', 'jqxgrid', 'jqxgrid_selection', 'jqxcheckbox', 'jqxgrid_edit', 'jqxpanel'],
    function($) {
  return {
    func : function() {
      html = '<div id="openweathermap_tabs"><ul><li>Konfiguration</li><li>Wartung</li><li>Plugins</li><li>Log</li></ul>'
      html += '<div id="openweathermap_konfig"></div>'
      html += '<div id="sytem_tool"></div><div><div id="system_plugins"></div></div><div><div id="system_log"></div></div></div>'
      $('#client_right').html(html)
      html = '<table><tr><td><b>API-Key:</b></td><td><input type="text" id="openweatherapi_apikey"/>'
      html += '</td></tr><tr><td><b>Timer:</b></td><td><div id="openweatherapi_intervall"></div></td></tr>'
      html += '<tr><td style="height:40px;"> </td</tr><tr><td></td><td>'
      $('#openweathermap_konfig').html(html + '<input type="button" value="Senden" id="openweathermap_send" /></td></tr></table>')
      $('#openweathermap_konfig').css('margin', '10px')
      $("#openweatherapi_apikey").jqxInput({placeHolder: "API-Key", height: 40, width: 250});
      $("#openweatherapi_intervall").jqxNumberInput({
        height: 40,
        width: 250,
        decimalDigits: 0,
        groupSeparator: '',
        spinButtonsStep: 60,
        spinButtons: true,
        min : 0
      })
      $('#openweathermap_send').jqxButton({width: 250, height: 40}).css('margin', '10px')
      $('#openweathermap_send').on('click', function(event) {
        var cmd = {'cmd': 'client.openweathermap.set_config',
                   'api': $('#openweatherapi_apikey').val(),
                   'intervall': $('#openweatherapi_intervall').val()
                  }
        window.smcall(cmd, function(){})
      })
      $('#openweathermap_tabs').jqxTabs({ width: '100%', height: '100%', position: 'top'})
      $('#sytem_tool').html('<input type="button" value="update/upgrade" id="1" />')
      $('#sytem_tool').append('<input type="button" value="Neu Booten" id="2" />')
      $('#sytem_tool').append('<input type="button" value="Restart" id="3" />')
      $('#sytem_tool').append('<input type="button" value="Neu Installtion" id="4" />')
      $('#sytem_tool > input').jqxButton({width: 250, height: 40}).css('margin', '10px')
      $('#sytem_tool > input').on('click', function(event) {
        var id = $(event.currentTarget).attr('id')
        if (id == 1) {
          window.smcall({cmd:'client_system_update'}, function() {})
        } else if (id == 2) {
          window.smcall({cmd:'client_system_reboot'}, function() {})
        } else if (id == 3) {
          window.smcall({cmd:'client_system_restart'}, function() {})
        } else if (id == 4) {
          window.smcall({cmd:'client_system_install'}, function() {})
        } else {
          console.log($(event.currentTarget).attr('id'))
        }
      })
      calltab0 = function() {
        window.smcall({cmd:'client.openweathermap.get_config'}, function(data) {
          $('#openweatherapi_apikey').val(data.api)
          $('#openweatherapi_intervall').val(data.intervall)
        })
      }
      calltab2 = function() {
      }
      calltab3 = function() {
      }
      $('#openweathermap_tabs').on('selected', function (event) {
        var selectedTab = event.args.item
        if (selectedTab == 0) {
          calltab0()
        } else if (selectedTab == 2) {
          calltab2()
        } else if (selectedTab == 3) {
          calltab3()
        } else {
          console.log(selectedTab)
        }
      });
      calltab0()
    }
  }
})
