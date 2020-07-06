define(['jquery', 'jqxbutton', 'jqxmenu'], function($) {
  window.head = {
    init: function() {
      html = '<div id="mainTop"><div class="leftMenu" style="height:100%;"><input type="button" id="burgerMenu" />'
      html +='<span id="slogan">Smart Live</span><input type="button" id="menuSmall" />'
      html += '</div><span id="host_name"></span><input type="button" id="loginButton" /></div>'
      html += '<div id="client_area"></div>'
      $('body').html(html)
      $("#menuSmall").jqxButton({ width: '1.75rem', height: '1.75rem', imgSrc: "/lib/img/left-24-white.png", imgHeight: 24, imgWidth: 24})
      $("#loginButton").jqxButton({ width: '2.4rem', height: '2.4rem', imgSrc: "/lib/img/login-36-white.png", imgHeight: 36, imgWidth: 36})
      get_remote_hosts = function() {
        window.smcall({'client': 'master', 'cmd':'get_clients'}, function(data) {
          window.head.menu.jqxMenu('destroy')
          window.head.menu = makeMenu(data, true)
        })
      }
      $("#burgerMenu").jqxButton({ width: '2.4rem', height: '2.4rem', imgSrc: "/lib/img/menu-36-white.png", imgHeight: 36, imgWidth: 36})
      $("#burgerMenu").on('click', function() {
        window.head.menu.jqxMenu('open', 16 , 48);
        window.head.menu.off('itemclick')
        window.head.menu.on('itemclick', function(event) {
          var element = event.args;
          var mod = $(element).data('mod')
          var p1 = $(element).data('p1')+'1'
          var p2 = $(element).data('p2')+'2'
          var p3 = $(element).data('p3')+'3'
          if (window.module == undefined) {
            window.module = {}
          }
          if (window.module_const == undefined) {
            window.module_const = {}
          }
          var paths = {}
          paths['mod.'+mod] = 'module/'+mod
          requirejs.config({paths:paths})
          window.module_const['mod.'+mod] = {p1: p1, p2:p2, p3:p3}
          if (window.module[mod] == undefined) {
            requirejs(['mod.'+mod], function(mod) {
              mod.init(p1,p2,p3)
            })
          } else {
             window.module[mod].init_data = {p1: p1, p2:p2, p3:p3}
             window.module[mod].init()
          }
        })
      })
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
        if (data.master) {
          get_remote_hosts()
        }
      })
      makeMenu = function(server, scan) {
        html = '<div id="TopMenu" style="visibility: hidden;"><ul>'
        html += '<li data-mod="clock"><a href="#">Uhr</a></li>'
        var l = server.length
        if (l > 0) {
          html += '<li type="separator"></li>'
          html += '<li>Backend-Server<ul>'
          for (var i = 0; i < l; i++) {
            html += '<li data-cmd="sm_host" data-id="' + i + '"><a href="#">' + server[i].hostname + '</a></li>'
          }
          html += '</ul></li>'
        }
        if (scan) {
          html += '<li type="separator"></li>'
          html += '<li  data-cmd="sm_scan"><a href="#">Backenderver suchen</a></li>'
        }
        html += '</ul></div>'
        $('body').append(html)
        return $("#TopMenu").jqxMenu({ width: '250px', autoOpenPopup: false, mode: 'popup'})
      }
      window.head.menu = makeMenu([], false)
      console.log('xXx')
    },
    menu : false
  }
  return window.head
})
