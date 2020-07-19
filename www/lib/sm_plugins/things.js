
define(['jquery', 'jqxinput', 'jqxnumberinput', 'jqxdata', 'jqxgrid', 'jqxtabs', 'jqxgrid_selection', 'jqxcheckbox',
    'jqxgrid_edit', 'jqxpanel', 'jqxgrid_columnsresize', 'jqxcombobox'],
    function($) {
  things = {
    func : function() {
      html = '<div id="things_tabs"><ul><li>Konfiguration</li><li>Sensoren</li></ul>'
      html += '<div id="things_konfig"></div>'
      html += '<div style="overflow: hidden"><div id="things_sensor"></div></div></div>'
      $('#sm_backend_content').html(html)
      html = '<table><tr><td><b>Name:</b></td><td><input type="text" id="things_name"/></td></tr>'
      html += '<tr><td style="height:40px;"> </td</tr><tr><td></td><td>'
      $('#things_konfig').html(html + '<input type="button" value="Senden" id="things_send" /></td></tr></table>')
      $('#things_konfig').css('margin', '10px')
      $("#things_name").jqxInput({placeHolder: "Pluginname", height: 40, width: 250});
      $('#things_send').jqxButton({width: 250, height: 40}).css('margin', '10px')
      $('#things_send').on('click', function(event) {
        var cmd = {'client': 'sm_backend', 'cmd':'things', 'data': {'ip':window.module.sm_backend.ip,
                                                                            cmd:'client_set_var',
                                                                            'friendly_name': $('#things_name').val()}}
        window.smcall(cmd, function(){})
      })
      $('#things_tabs').jqxTabs({ width: '100%', height: '100%', position: 'top'})
      calltab0 = function() {
        window.smcall({'client': 'sm_backend', 'cmd':'things', 'data': {'ip':window.module.sm_backend.ip, cmd:'client_get_var'}}, function(data) {
          var data = data.data
          $('#things_name').val(data.friendly_name)
          $('#things_apikey').val(data.api)
          $('#things_intervall').val(data.intervall)
        })
      }
      calltab1 = function() {
        window.smcall({'client': 'sm_backend', 'cmd':'things', 'data': {'ip':window.module.sm_backend.ip,
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
              { name: 'time', type: 'int' }
            ]}
          var dataAdapter = new $.jqx.dataAdapter(source)
          var cellsrenderer = function (row, columnfield, value, defaulthtml, columnproperties) {
            if (columnfield == 'time') {
              var utc = new Date().getTime()
              var d = new Date(value*1000)
              if (utc-value*1000 < 86400000) {
                 var h = d.getHours()
                 var m = d.getMinutes()
                 var s = d.getSeconds()
                 var frm = '' + (h<=9 ? '0' + h : h) + ':' + (m<=9 ? '0' + m : m) + ':' + (s<=9 ? '0' + s : s)
                return defaulthtml.replace(value, frm)
              } else {
                return defaulthtml
              }
            }
            return defaulthtml
          }
          $("#things_sensor").jqxGrid({
            width: '100%',
            height: '100%',
            source: dataAdapter,
            columnsresize: true,
            editable: true,
            columns: [
              { text: 'Name', datafield: 'name', editable: false, hidden: true},
              { text: 'Bezeichnung', datafield: 'friendly_name'},
              { text: 'Wert', datafield: 'value', editable: false},
              { text: 'Einheit', datafield: 'unit', editable: false},
              { text: 'Zeitpunkt', datafield: 'time', editable: false, cellsrenderer: cellsrenderer},
              { text: 'Typ', datafield: 'type', editable: false}
            ]
          })
          $("#things_sensor").off('cellendedit')
          $("#things_sensor").on('cellendedit', function (event) {
            var row = event.args.row
            row[event.args.datafield] = event.args.value
            window.smcall({'client': 'sm_backend', 'cmd':'things', 'data': {'ip':window.module.sm_backend.ip,
                                                                                     cmd:'client_set_sensor', 'row': row}}, function() {})
          })
        })
      }
      $('#things_tabs').on('selected', function (event) {
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
  window.module.sm_backend.sm_client.things = things
  return things
})
