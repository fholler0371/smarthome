define(['module', 'datepicker'], function(module) {
  var clock = {
    init : function() {
      var html = '<div id="mod_clock_outer"><div id="mod_clock_hour" class="mod_clock_circle"></div>'
      html += '<div id="mod_clock_minute" class="mod_clock_circle"></div>'
      html += '<div id="mod_clock_second" class="mod_clock_circle"></div>'
      html += '<div id="mod_clock_date" class="mod_clock_text"></div>'
      html += '<div id="mod_clock_week" class="mod_clock_text"></div>'
      $('#client_area').html(html + '</div>')
      $('.mod_clock_circle').html('<canvas height="200" width="200"></canvas><div class="mod_clock_number"></div>')
      window.module.clock.run = true
      $.datepicker.regional.de = {
        monthNames: "Januar Februar M\u00e4rz April Mai Juni Juli August September Oktober November Dezember".split(" "),
        dayNames: "Sonntag Montag Dienstag Mittwoch Donnerstag Freitag Samstag".split(" ")
      };
      $.datepicker.setDefaults($.datepicker.regional.de)
      window.module.clock._tick()
    },
    stop : function() {
      window.module.clock.run = false
    },
    _tick : function() {
      if (window.module.clock.run) {
        var time = new Date;
        window.module.clock._circle('#mod_clock_hour', time.getHours(), 24)
        window.module.clock._circle('#mod_clock_minute', time.getMinutes(), 60)
        window.module.clock._circle('#mod_clock_second', time.getSeconds(), 60)
        $('#mod_clock_date').html($.datepicker.formatDate("DD, d. MM yy", time))
        $('#mod_clock_week').html($.datepicker.iso8601Week(time) + ". Woche")
        setTimeout(window.module.clock._tick, 1E3)
      }
    },
    _circle : function(id, value, max) {
      var canvas = $(id).find('canvas')[0].getContext('2d')
      canvas.clearRect(0, 0, 200, 200)
      canvas.beginPath()
      canvas.arc(100, 100, 80, -.5 * Math.PI, value / max * 2 * Math.PI +  -.5 * Math.PI)
      canvas.lineWidth = 20
      canvas.strokeStyle = '#0288d1'
      canvas.stroke()
      $(id).find("div").html(("0" + value).slice(-2))
    },
    run : false
  }
  clock['init_data'] = window.module_const[module.id]
  window.module.clock = clock
  return clock
})
