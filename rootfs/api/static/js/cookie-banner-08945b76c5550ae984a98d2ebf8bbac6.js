
// Uses cookies to see if users have dismissed the cookie banner.
// If they haven't, inserts the banner:
// - if an element with ID = Heroku.CookieBanner.domElementId exists, inserts the content of the banner there
// - if not, inserts the banner at the top of the body element
var Heroku = Heroku || {};

Heroku.CookieBanner = {
  cookieName: 'heroku-cookie-banner-dismissed',
  cookieDismissedValue: '1',
  domElementId: 'heroku-cookie-banner',
  dismissElementClass: 'heroku-cookie-banner__dismiss',
  domain: '.heroku.com', // accessible to all subdomains
  init: function () {
    var isDismissed = Heroku.CookieBanner.getCookie(Heroku.CookieBanner.cookieName) == Heroku.CookieBanner.cookieDismissedValue;
    var cookieBannerDismiss = document.getElementsByClassName(Heroku.CookieBanner.dismissElementClass)[0]

    if (!isDismissed) {
      Heroku.CookieBanner.show()
    }
    cookieBannerDismiss.onclick = function (e) {Heroku.CookieBanner.dismiss(e)};
  },
  show: function () {
    var cookieBanner = document.getElementById(Heroku.CookieBanner.domElementId);
    cookieBanner.style.display = "block"
  },
  getCookie: function (name) {
    var v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return v ? v[2] : null;
  },
  setCookie: function (name, value, domain, days) {
    var d = new Date;
    d.setTime(d.getTime() + 24 * 60 * 60 * 1000 * days);
    document.cookie = name + '=' + value + ';domain=' + domain + ';path=/;expires=' + d.toGMTString();
  },
  dismiss: function (event) {
    Heroku.CookieBanner.setCookie(Heroku.CookieBanner.cookieName, Heroku.CookieBanner.cookieDismissedValue, Heroku.CookieBanner.domain, 365);
    var cookieBanner = document.getElementById(Heroku.CookieBanner.domElementId);
    cookieBanner.parentElement.removeChild(cookieBanner);
    event.preventDefault();
  }
};

document.addEventListener("DOMContentLoaded", function (event) {
  Heroku.CookieBanner.init();
});
