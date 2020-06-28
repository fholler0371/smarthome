define(['jquery', 'jqxdatatable', 'jqxtabs'], function($) {
  return {
    func : function() {
      html = '<div id="system_tabs"><ul><li>Status</li><li>Wartung</li><li>Plugins</li></ul><div id="system_status"></div>'
      html += '<div id="sytem_tool"></div><div></div></div>'
      $('#client_right').html(html)
      $('#system_tabs').jqxTabs({ width: '100%', height: '100%', position: 'top'})
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
        } else {
          console.log($(event.currentTarget).attr('id'))
        }
      })
      $('#system_tabs').on('selected', function (event) {
        var selectedTab = event.args.item
        console.log(selectedTab)
      });
      window.smcall({cmd:'client_get_state'}, function(data) {
        html = '<table id="state_table"><thead><tr><th  align="left">Name</th><th align="left">Wert</th></tr></thead><tbody>'
        html += '<tr><td>Typ</td><td>' + data.type + '</td></tr>'
        html += '<tr><td>Hostname</td><td>' + data.hostname + '</td></tr>'
        html += '<tr><td>IP-Adresse</td><td>' + data.ip + '</td></tr>'
        html += '<tr><td>Arbeitsspeicher</td><td>' + data.mem + '</td></tr>'
        html += '<tr><td>Frei</td><td>' + data.free + '</td></tr>'
        html += '<tr><td>Festplatte</td><td>' + data.disk + '</td></tr>'
        html += '<tr><td>Laufzeit</td><td>' + data.uptime + '</td></tr>'
        html += '<tr><td>SmartHome Up</td><td>' + data.shtime + '</td></tr>'
        html += '<tr><td>Temperature</td><td>' + data.temp + '</td></tr>'
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
  }
})
