define(['jquery', 'jqxbutton', 'jqxmenu'], function($) {
  window.head = {
    init: function() {
      window.head.logout()
      html = '<div id="mainTop"><div class="leftMenu" style="height:100%;"><input type="button" id="burgerMenu" />'
      html +='<span id="slogan">Smart Live</span><input type="button" id="menuSmall" />'
      html += '</div><span id="head_title"></span><span id="user_name"></span>'
      html += '<input type="button" id="logoutButton" /><input type="button" id="loginButton" /></div>'
      html += '<div id="client_area"></div>'
      $('body').html(html)
      $("#menuSmall").jqxButton({ width: '1.75rem', height: '1.75rem', imgSrc: "/lib/img/left-24-white.png", imgHeight: 24, imgWidth: 24})
      $("#loginButton").jqxButton({ width: '2.4rem', height: '2.4rem', imgSrc: "/lib/img/login-36-white.png", imgHeight: 36, imgWidth: 36})
      $("#logoutButton").jqxButton({ width: '2.4rem', height: '2.4rem', imgSrc: "/lib/img/logout-36-white.png", imgHeight: 36, imgWidth: 36})
      $("#logoutButton").hide()
      $("#logoutButton").on('click', function() {
        window.head.logout()
      })
      $("#burgerMenu").jqxButton({ width: '2.4rem', height: '2.4rem', imgSrc: "/lib/img/menu-36-white.png", imgHeight: 36, imgWidth: 36})
      $("#burgerMenu").on('click', function() {
        window.head.menu.jqxMenu('open', 16 , 48);
        window.head.menu.off('itemclick')
        window.head.menu.on('itemclick', function(event) {
          var element = event.args;
          if ($(element).data('display') != 'no') {
            for (const[name, mod] of Object.entries(window.module)) {
              mod.stop()
            }
          }
          var mod = $(element).data('mod')
          var p1 = $(element).data('p1')
          var p2 = $(element).data('p2')
          var p3 = $(element).data('p3')
          var paths = {}
          paths['mod.'+mod] = 'module/'+mod
          requirejs.config({paths:paths})
          window.module_const['mod.'+mod] = {p1: p1, p2:p2, p3:p3}
          if (window.module[mod] == undefined) {
            requirejs(['mod.'+mod], function(mod) {
              mod.init()
            })
          } else {
             window.module[mod].init_data = {p1: p1, p2:p2, p3:p3}
             window.module[mod].init()
          }
        })
      })
      $("#loginButton, #logoutButton, #burgerMenu").css('position', 'absolute')
      $("#menuSmall > img, #loginButton > img, #logoutButton > img, #burgerMenu > img").css({'top': 1, 'left': 1})
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
        mod = $('#client_area').data('min')
        if (mod != undefined) {
          window.module[mod].setMinMenu()
        }
      })
      window.head.menu = window.head.makeMenu([])
      window.module = {}
      window.module_const = {}
      var paths = {}
      paths['mod.clock'] = 'module/clock'
      requirejs.config({paths:paths})
      window.module_const['mod.clock'] = {p1: 0, p2: 0, p3: 0}
      requirejs(['mod.clock'], function(mod) {
        mod.init()
      })
      $('#loginButton').on('click', function() {
        requirejs(['jqxwindow', 'jqxinput', 'jqxpasswordinput', 'jqxbutton'], function() {
          if ($('#login_window').length == 0) {
            var html = '<div id="login_window"><div><span>Anmelden</span></div><div>'
            html += '<table><tr><td><b>Nutzer<b></td><td><input type="text" id="login_user"/></td><tr>'
            html += '<tr><td><b>Password<b></td><td><input type="password" id="login_passwd"/></td><tr>'
            html += '<tr><td> </td><td> </td><tr>'
            html += '<tr><td><td><input style="float:right" id="login_button" type="button" value="Anmelden" /></td><tr>'
            $('body').append(html + '</table></div></div>')
            $('#login_window').jqxWindow({isModal: true, width:375, height: 165, resizable: false})
            $('#login_user').jqxInput({placeHolder: "Nutzer", height: 30, width: 250, minLength: 4})
            $('#login_passwd').jqxPasswordInput({placeHolder: "Passwort", height: 30, width: 250, minLength: 4})
            $('#login_button').jqxButton({height: 30, width: 200})
            $('#login_button').on('click', function() {
              $('#login_user').jqxInput({disabled: true })
              $('#login_passwd').jqxPasswordInput({disabled: true })
              $('#login_button').jqxButton({disabled: true })
              window.smcall({'client': 'master', 'cmd':'get_salt', 'data': {'user': $('#login_user').val(),
                                                                            'passwd': $('#login_passwd').val()}}, function(data) {
                $('#login_window').jqxWindow('close')
                if (data.login) {
                  $('#loginButton').hide()
                  $('#logoutButton').show()
                  $('#user_name').show()
                  $('#user_name').html(data.name)
                  window.head.tick()
                  window.head.get_menu()
                } else {
                  window.head.logout()
                  sessionStorage.removeItem("token")
                }
              })
            })
          } else {
            $('#login_user').jqxInput({disabled: false })
            $('#login_passwd').jqxPasswordInput({disabled: false })
            $('#login_passwd').val('')
            $('#login_button').jqxButton({disabled: false })
            $('#login_window').jqxWindow('open')
          }
        })
      })
      if (sessionStorage.getItem("token") != null) {
        window.head.get_menu()
      }
      $('*').on('mousemove click mouseup mousedown keydown keypress keyup submit change mouseenter scroll resize dblclick',
                window.head.get_user_movement)
    },
    logout : function() {
      if ($('#login_window').length != 0) {
        $('#login_window').jqxWindow('close')
      }
      $('#loginButton').show()
      $('#logoutButton').hide()
      $('#user_name').hide()
      sessionStorage.removeItem("token")
      window.head.menu = window.head.makeMenu([])
      if (window.module != undefined) {
        for (const[name, mod] of Object.entries(window.module)) {
          mod.stop()
        }
        window.module.clock.init()
      }
    },
    get_menu : function() {
      window.smcall({'client': 'master', 'cmd':'get_menu', 'data': {}}, function(data) {
        if (data.login) {
          window.head.menu = window.head.makeMenu(data.data)
        } else {
          window.head.menu = window.head.makeMenu([])
        }
      })
    },
    get_user_movement : function() {
      window.head.count = 600
    },
    tick : function() {
      window.head.count = window.head.count - 1
      window.head.keep = window.head.keep - 1
      if (sessionStorage.getItem("token") != null) {
        setTimeout(window.head.tick, 1E3)
      }
      if (window.head.count <= 0) {
        window.head.logout()
      }
      if (window.head.keep <= 0) {
        window.head.keep = 60
        window.head.keep_alive()
      }
    },
    keep_alive : function() {
      window.smcall({'client': 'master', 'cmd':'keep_alive', 'data': {}}, function() {})
    },
    makeMenu : function(data) {
      try {
        window.head.menu.jqxMenu('destroy')
      } catch(err) {}
      html = '<div id="TopMenu" style="visibility: hidden;"><ul>'
      html += '<li data-mod="clock"><a href="#">Uhr</a></li>'
      var l = data.length
      if (l > 0) {
        for (var i=0; i<l; i++) {
          entry = data[i]
          if ('sub' in entry) {
            html += '<li>'+entry.label+'<ul>'
            var l1 = entry.sub.length
            for (var i1=0; i1<l1; i1++) {
              entry1 = entry.sub[i1]
              html += '<li  data-mod="'+entry1.mod+'" data-p1="'+entry1.p1+'" data-p2="'+entry1.p2+'" data-p3="'+entry1.p3+'"'
              if (entry1.display != undefined) {
                if (!entry1.display) {
                  html += ' data-display="no"'
                }
              }
              html += '>'+entry1.label+'</li>'
            }
            html += '</ul></li>'
          } else {
            html += '<li  data-mod="'+entry.mod+'" data-p1="'+entry.p1+'" data-p2="'+entry.p2+'" data-p3="'+entry.p3+'"'
            if (entry.display != undefined) {
              if (!entry.display) {
                html += ' data-display="no"'
              }
            }
            html += '>'+entry.label+'</li>'
          }
        }
      }
      html += '</ul></div>'
      $('body').append(html)
      return $("#TopMenu").jqxMenu({ width: '250px', autoOpenPopup: false, mode: 'popup'})
    },
    menu : false,
    count : 600,
    keep: 60
  }
  return window.head
})
