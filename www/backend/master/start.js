define(['jquery'], function($) {
  return  {
    start : function() {
      window.smcall = function(data, cb) {
        $.ajax({
          url: '/api',
          context: cb,
          method: 'POST',
          crossDomain: true,
          data: JSON.stringify(data),
          dataType: 'json'
        })

        conaole.log(data)
      }
      html = '<div id="mainSplitter"><div id="panel-master"><input type="button" value="Scannen nach Clients" id="scan" />'
      $('body').append(html + '</div><div id="panel-clients">Panel2</div></div>')
      requirejs(['jqxsplitter', 'jqxbutton'], function() {
        $('#mainSplitter').jqxSplitter({height: '100%', width: '100%', orientation: 'horizontal', resizable: false,
            panels: [{size: 60 }, { size: 300 }] })
        $("#scan").jqxButton({ width: 200, height: 40 }).css('margin', '10px').on('click', function() {
          window.smcall({cmd:'scan_clients'}, 'xXx')
        });
      });
    }
  }
});
