define(['jquery', 'jqxdatatable'], function($) {
  return {
    func : function() {
      window.smcall({cmd:'client_get_state'}, function(data) {
        html = '<table id="state_table"><thead><tr><th  align="left">Name</th><th align="left">Wert</th></tr></thead><tbody>'
        html += '<tr><td>Typ</td><td>' + data.type + '</td></tr>'
        html += '<tr><td>Hostname</td><td>' + data.hostname + '</td></tr>'
        html += '<tr><td>IP-Adresse</td><td>' + data.ip + '</td></tr>'
        html += '<tr><td>Arbeitsspeicher</td><td>' + data.mem + '</td></tr>'
        html += '<tr><td>Frei</td><td>' + data.free + '</td></tr>'
        html += '<tr><td>Festplatte</td><td>' + data.disk + '</td></tr>'
        html += '<tr><td>Laufzeit</td><td>' + data.uptime + '</td></tr>'
        html += '<tr><td>Temperature</td><td>' + data.temp + '</td></tr>'
        $('#client_right').html(html + '</tbody></table>')
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
