define(['jquery', 'jqxinput', 'jqxnumberinput', 'jqxdata', 'jqxgrid', 'jqxtabs', 'jqxgrid_selection', 'jqxcheckbox',
    'jqxgrid_edit', 'jqxpanel', 'jqxgrid_columnsresize', 'jqxcombobox'],
    function($) {
  openweathermap = {
    func : function() {
      html = '<div id="openweathermap_tabs"><ul><li>Konfiguration</li><li>Sensoren</li></ul>'
      html += '<div id="openweathermap_konfig"></div>'
      html += '<div style="overflow: hidden"><div id="openweathermap_sensor"></div></div></div>'
      $('#sm_backend_content').html(html)
      html = '<table><tr><td><b>Name:</b></td><td><input type="text" id="openweathermap_name"/></td></tr>'
      html += '<tr><td><b>API-Key:</b></td><td><input type="text" id="openweathermap_apikey"/>'
      html += '</td></tr><tr><td><b>Timer:</b></td><td><div id="openweathermap_intervall"></div></td></tr>'
      html += '<tr><td style="height:40px;"> </td</tr><tr><td></td><td>'
      $('#openweathermap_konfig').html(html + '<input type="button" value="Senden" id="openweathermap_send" /></td></tr></table>')
      $('#openweathermap_konfig').css('margin', '10px')
      $("#openweathermap_name").jqxInput({placeHolder: "Pluginname", height: 40, width: 250});
      $("#openweathermap_apikey").jqxInput({placeHolder: "API-Key", height: 40, width: 250});
      $("#openweathermap_intervall").jqxNumberInput({
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
        var cmd = {'client': 'sm_backend', 'cmd':'openweathermap', 'data': {'ip':window.module.sm_backend.ip,
                                                                            cmd:'client_set_var',
                                                                            'api': $('#openweathermap_apikey').val(),
                                                                            'intervall': $('#openweathermap_intervall').val(),
                                                                            'friendly_name': $('#openweathermap_name').val()}}
        window.smcall(cmd, function(){})
      })
      $('#openweathermap_tabs').jqxTabs({ width: '100%', height: '100%', position: 'top'})
      calltab0 = function() {
        window.smcall({'client': 'sm_backend', 'cmd':'openweathermap', 'data': {'ip':window.module.sm_backend.ip, cmd:'client_get_var'}}, function(data) {
          var data = data.data
          $('#openweathermap_name').val(data.friendly_name)
          $('#openweathermap_apikey').val(data.api)
          $('#openweathermap_intervall').val(data.intervall)
        })
      }
      calltab1 = function() {
        window.smcall({'client': 'sm_backend', 'cmd':'openweathermap', 'data': {'ip':window.module.sm_backend.ip,
                                                                                cmd:'client_get_sensor'}}, function(data) {
          var source = {
            localdata: data.data.sensors,
            datatype: "array",
            datafields: [
              { name: 'name', type: 'string' },
              { name: 'friendly_name', type: 'string' },
              { name: 'value', type: 'string' },
              { name: 'unit', type: 'string' },
              { name: 'type', type: 'string' },
              { name: 'has_default', type: 'bool'},
              { name: 'default', type: 'string' },
              { name: 'seen', type: 'bool'},
              { name: 'send', type: 'bool'},
              { name: 'var_type', type: 'str'}
            ]}
          var dataAdapter = new $.jqx.dataAdapter(source)
          $("#openweathermap_sensor").jqxGrid({
            width: '100%',
            height: '100%',
            source: dataAdapter,
            columnsresize: true,
            editable: true,
            columns: [
              { text: 'Name', datafield: 'name', editable: false},
              { text: 'Bezeichnung', datafield: 'friendly_name'},
              { text: 'Wert', datafield: 'value', editable: false},
              { text: 'Einheit', datafield: 'unit', columntype: 'combobox',
                createeditor: function (row, column, editor) {
                  editor.jqxComboBox({ autoDropDownHeight: true, source: data.data.units, promptText: "Einheit festlegen:" });
                }
              },
              { text: 'Typ', datafield: 'type', columntype: 'combobox',
                createeditor: function (row, column, editor) {
                  editor.jqxComboBox({ autoDropDownHeight: true, source: data.data.types, promptText: "Typ festlegen:" });
                }
              },
              { text: 'Datentyp', datafield: 'var_type', columntype: 'combobox',
                createeditor: function (row, column, editor) {
                  editor.jqxComboBox({ autoDropDownHeight: true, source: ['Int', 'Float'], promptText: "Typ festlegen:" });
                }
              },
              { text: 'hat Standart', datafield: 'has_value', columntype: 'checkbox'},
              { text: 'Standart', datafield: 'default'},
              { text: 'gesehen', datafield: 'seen', columntype: 'checkbox'},
              { text: 'senden', datafield: 'send', columntype: 'checkbox'}
            ]
          })
          $("#openweathermap_sensor").off('cellendedit')
          $("#openweathermap_sensor").on('cellendedit', function (event) {
            var row = event.args.row
            row[event.args.datafield] = event.args.value
            window.smcall({'client': 'sm_backend', 'cmd':'openweathermap', 'data': {'ip':window.module.sm_backend.ip,
                                                                                     cmd:'client_set_sensor', 'row': row}}, function() {})
          })
        })
      }
      $('#openweathermap_tabs').on('selected', function (event) {
        var selectedTab = event.args.item
        if (selectedTab == 0) {
          calltab0()
        } else if (selectedTab == 1) {
          calltab1()
        }
      });
      calltab0()
    }
  }
  window.module.sm_backend.sm_client.openweathermap = openweathermap
  return openweathermap
})
