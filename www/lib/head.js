define(['jquery', 'jqxbutton'], function($) {
  return {
    init: function() {
      html = '<div id="mainTop"><div class="leftMenu" style="height:100%;"><input type="button" id="burgerMenu" />'
      html +='<span id="slogan">Smart Live</span><input type="button" id="menuSmall" />'
      html += '</div><span id="host_name"></span><input type="button" id="loginButton" /></div>'
      html += '<div id="client_area"></div>'
      $('body').html(html)
      $("#menuSmall").jqxButton({ width: '1.75rem', height: '1.75rem', imgSrc: "/lib/img/left-24-white.png", imgHeight: 24, imgWidth: 24})
      $("#loginButton").jqxButton({ width: '2.4rem', height: '2.4rem', imgSrc: "/lib/img/login-36-white.png", imgHeight: 36, imgWidth: 36})
      $("#burgerMenu").jqxButton({ width: '2.4rem', height: '2.4rem', imgSrc: "/lib/img/menu-36-white.png", imgHeight: 36, imgWidth: 36})
      $("#loginButton, #burgerMenu").css('position', 'absolute')
      $("#menuSmall > img, #loginButton > img, #burgerMenu > img").css({'top': 1, 'left': 1})
      $("#menuSmall").on('click', function() {
        $('#mainTop').toggleClass('leftMenuSmall')
        if ($('#mainTop').hasClass('leftMenuSmall')) {
          $('#slogan').hide()
          $('#menuSmall').jqxButton({ imgSrc: '/lib/img/right-24-white.png' });
        } else {
          $('#slogan').show()
          $('#menuSmall').jqxButton({ imgSrc: '/lib/img/left-24-white.png' });
        }
        $("#menuSmall > img").css({'top': 1, 'left': 1})
      })
      window.smcall({'client': 'master', 'cmd':'get_server'}, function(data) {
        $("#host_name").html("Server: " + data.friendly_name)
        $("#host_name").data('data', data)
        console.log(data)
      })
      console.log('xXx')
    }
  }
})
