define(['jquery', 'jqxdatatable', 'jqxinput', 'jqxtabs', 'jqxdata', 'jqxgrid', 'jqxgrid_selection', 'jqxcheckbox',
    'jqxgrid_edit', 'jqxpanel'],
    function($) {
  system = {
    func : function() {
      html = '<div id="system_tabs"><ul><li>Status</li><li>Konfiguration</li><li>Wartung</li><li>Plugins</li><li>Log</li></ul>'
      html += '<div id="system_status"></div><div id="system_config"></div>'
      html += '<div id="sytem_tool"></div><div><div id="system_plugins"></div></div><div><div id="system_log"></div></div></div>'
      $('#sm_backend_content').html(html)
      $('#system_tabs').jqxTabs({ width: '100%', height: '100%', position: 'top'})
      $('#sytem_tool').html('<input type="button" value="update/upgrade" id="1" />')
      $('#sytem_tool').append('<input type="button" value="Neu Booten" id="2" />')
      $('#sytem_tool').append('<input type="button" value="Restart" id="3" />')
      $('#sytem_tool').append('<input type="button" value="Neu Installtion" id="4" />')
      $('#sytem_tool > input').jqxButton({width: 250, height: 40}).css('margin', '10px')
      html = '<table><tr><td><b>Masterserver:</b></td><td><div id="system_master"></td></tr>'
      html += '<tr><td><b>Servername:</b></td><td><input type="text" id="system_name"/>'
      html += '<tr><td><b>Latitude:</b></td><td><input type="text" id="system_lat"/>'
      html += '</td></tr><tr><td><b>Longitude:</b></td><td><input type="text" id="system_long"/></td></tr>'
      html += '<tr><td style="height:40px;"> </td</tr><tr><td></td><td>'
      $('#system_config').html(html + '<input type="button" value="Senden" id="system_send" /></td></tr></table>')
      $("#system_name").jqxInput({placeHolder: "Servername", height: 40, width: 250});
      $("#system_lat").jqxInput({placeHolder: "Latitude", height: 40, width: 250});
      $("#system_long").jqxInput({placeHolder: "Longitude", height: 40, width: 250});
      $('#system_send').jqxButton({width: 250, height: 40}).css('margin', '10px')
      $("#system_master").jqxCheckBox({ width: 120, height: 25});
      $('#system_send').on('click', function() {
        $("#host_name").html("Server: "+$('#system_name').val())
        data = {'ip':window.module.sm_backend.ip, cmd:'client_set_var', 'friendly_name': $('#system_name').val(),
                'master': $("#system_master").jqxCheckBox('val'),
                'geo': {'lat': $('#system_lat').val(), 'long': $('#system_long').val()}}
        window.smcall({'client': 'sm_backend', 'cmd':'system', 'data': data}, function(data) {})
      })
      $('#sytem_tool > input').on('click', function(event) {
        var id = $(event.currentTarget).attr('id')
        if (id == 1) {
          window.smcall({'client': 'sm_backend', 'cmd':'system', 'data': {'ip':window.module.sm_backend.ip, cmd:'client_update'}}, function(data) {})
        } else if (id == 2) {
          window.smcall({'client': 'sm_backend', 'cmd':'system', 'data': {'ip':window.module.sm_backend.ip, cmd:'client_reboot'}}, function(data) {})
        } else if (id == 3) {
          window.smcall({'client': 'sm_backend', 'cmd':'system', 'data': {'ip':window.module.sm_backend.ip, cmd:'client_restart'}}, function(data) {})
        } else if (id == 4) {
          window.smcall({'client': 'sm_backend', 'cmd':'system', 'data': {'ip':window.module.sm_backend.ip, cmd:'client_install'}}, function(data) {})
        }
      })
      calltab0 = function() {
        window.smcall({'client': 'sm_backend', 'cmd':'system', 'data': {'ip':window.module.sm_backend.ip, cmd:'client_get_state'}}, function(data) {
          var data = data.data
          html = '<table id="state_table"><thead><tr><th  align="left">Name</th><th align="left">Wert</th></tr></thead><tbody>'
          html += '<tr><td>Typ</td><td>' + data.type + '</td></tr>'
          html += '<tr><td>Serien Nr.</td><td>' + data.serial + '</td></tr>'
          html += '<tr><td>Hostname</td><td>' + data.hostname + '</td></tr>'
          html += '<tr><td>IP-Adresse</td><td>' + data.ip + '</td></tr>'
          html += '<tr><td>Arbeitsspeicher</td><td>' + data.mem + '</td></tr>'
          html += '<tr><td>Frei</td><td>' + data.free + '</td></tr>'
          html += '<tr><td>Festplatte</td><td>' + data.disk + '</td></tr>'
          html += '<tr><td>Laufzeit</td><td>' + data.uptime + '</td></tr>'
          html += '<tr><td>SmartHome Up</td><td>' + data.shtime + '</td></tr>'
          html += '<tr><td>System Last</td><td>' + data.last + '</td></tr>'
          html += '<tr><td>SmartHome Version</td><td>' + data.version + '</td></tr>'
          html += '<tr><td>Temperature</td><td>' + data.temp + '</td></tr>'
          html += '<tr><td>Kernal-Version</td><td>' + data.kernalversion + '</td></tr>'
          html += '<tr><td>OS-Name</td><td>' + data.osname + '</td></tr>'
          html += '<tr><td>Python Version</td><td>' + data.python + '</td></tr>'
          $('#system_status').html(html + '</tbody></table>')
          $('#state_table').jqxDataTable({
            selectionMode: 'singleRow',
            columns: [
              { text: 'Parameter', dataField: 'Name', width: 250 },
              { text: 'Wert', dataField: 'Wert', width: 300 }
            ]
          })
          $('#state_table').css('margin', '10px')
        })
      }
      calltab2 = function() {
        window.smcall({'client': 'sm_backend', 'cmd':'system', 'data': {'ip':window.module.sm_backend.ip, cmd:'client_get_plugins'}}, function(data) {
          var source = {
            localdata: data.data,
            datatype: "array",
            datafields: [
              { name: 'name', type: 'string' },
              { name: 'friendly', type: 'string' },
              { name: 'active', type: 'bool' },
              { name: 'background', type: 'bool' },
              { name: 'description', type: 'string' }
            ]
          }
          var dataAdapter = new $.jqx.dataAdapter(source, {
            downloadComplete: function (data, status, xhr) { },
            loadComplete: function (data) { },
            loadError: function (xhr, status, error) { }
          })
          var cellbeginedit = function (row, datafield, columntype, value) {
            var data = $('#system_plugins').jqxGrid('getrowdatabyid', row);
            return !data.background
          }
          $("#system_plugins").jqxGrid({
            width: '100%',
            height: '100%',
            source: dataAdapter,
            editable: true,
            columns: [
              { text: 'Plugin', editable: false, datafield: 'name', width: 200 },
              { text: 'Name',  editable: false, datafield: 'friendly', width: 200 },
              { text: 'Aktiv', columntype: 'checkbox', cellbeginedit: cellbeginedit, datafield: 'active', width: 100 },
              { text: 'Background',  editable: false, columntype: 'checkbox', datafield: 'background', width: 100 },
              { text: 'Beschreibung',  editable: false, datafield: 'description'}
            ]
          })
          $("#system_plugins").on('cellendedit', function (event) {
            var args = event.args
            var data = $('#system_plugins').jqxGrid('getrowdatabyid', args.rowindex);
            window.smcall({'client': 'sm_backend', 'cmd':'system', 'data': {'ip':window.module.sm_backend.ip,
                                                                            cmd:'client_set_plugins',
                                                                            'name': data.name,
                                                                            'value': args.value}},
                function() {})
          })
        })
      }
      calltab3 = function() {
        window.smcall({'client': 'sm_backend', 'cmd':'system', 'data': {'ip':window.module.sm_backend.ip, cmd:'client_get_logs'}}, function(data) {
          console.log(data)
          $('#system_log').jqxPanel('clearcontent')
          $('#system_log').jqxPanel('append', data.data)
        })
      }
      $('#system_tabs').on('selected', function (event) {
        var selectedTab = event.args.item
        if (selectedTab == 0) {
          calltab0()
        } else if (selectedTab == 3) {
          calltab2()
        } else if (selectedTab == 4) {
          calltab3()
        }
      });
      $("#system_plugins, #system_log").parent().css('overflow', 'hidden')
      $("#system_log").jqxPanel({ width: '100%', height: '100%'});
      $("#system_log").parent().css('overflow', 'hidden')
      calltab0()
      window.smcall({'client': 'sm_backend', 'cmd':'system', 'data': {'ip':window.module.sm_backend.ip, cmd:'client_get_var'}}, function(data) {
        var data = data.data
        $("#system_master").jqxCheckBox('val', data.master)
        $('#system_name').val(data.friendly_name)
        $('#system_lat').val(data.geo.lat)
        $('#system_long').val(data.geo.long)
      })
    }
  }
  window.module.sm_backend.sm_client.system = system
  return system
})
