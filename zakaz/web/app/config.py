import os

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True

RECAPTCHA_API_SERVER = 'https://www.google.com/recaptcha/api/siteverify'
RECAPTCHA_DATA_ATTRS = {'callback': 'recaptchaCallback'}

SQLALCHEMY_DATABASE_URI = 'postgresql://simsim_order_user:root@localhost:5432/simsim_order'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_MIGRATE_REPO = os.path.normpath(os.path.join(basedir, '../migrations'))

ADMIN_URL = '/admin'

CHATRA_CODE = '''
<script>
window.ChatraSetup = {
    colors: {
        buttonText: '#ffffff', 
        buttonBg: '#e80016'    
    }
};
</script>
<!-- Chatra {literal} -->
<script>
    (function(d, w, c) {
        w.ChatraID = 'oqX63Gr8As8H39dpF';
        var s = d.createElement('script');
        w[c] = w[c] || function() {
            (w[c].q = w[c].q || []).push(arguments);
        };
        s.async = true;
        s.src = (d.location.protocol === 'https:' ? 'https:': 'http:')
        + '//call.chatra.io/chatra.js';
        if (d.head) d.head.appendChild(s);
    })(document, window, 'Chatra');
</script>
<!-- /Chatra {/literal} -->
'''

GA_CODE = '''
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-103079917-2', 'auto');
  ga('send', 'pageview');

</script>
'''
YANDEX_METRIKA_CODE = '''
<!-- Yandex.Metrika counter -->
<script type="text/javascript" >
    (function (d, w, c) {
        (w[c] = w[c] || []).push(function() {
            try {
                w.yaCounter45405879 = new Ya.Metrika({
                    id:45405879,
                    clickmap:true,
                    trackLinks:true,
                    accurateTrackBounce:true
                });
            } catch(e) { }
        });

        var n = d.getElementsByTagName("script")[0],
            s = d.createElement("script"),
            f = function () { n.parentNode.insertBefore(s, n); };
        s.type = "text/javascript";
        s.async = true;
        s.src = "https://mc.yandex.ru/metrika/watch.js";

        if (w.opera == "[object Opera]") {
            d.addEventListener("DOMContentLoaded", f, false);
        } else { f(); }
    })(document, window, "yandex_metrika_callbacks");
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/45405879" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->
'''

MINIFY_PAGE = True

from .config_private import *
