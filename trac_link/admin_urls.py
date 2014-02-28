from __future__ import unicode_literals

from django.conf.urls.defaults import patterns, url

from trac_link.extension import TracLink


urlpatterns = patterns('',
    url(r'^$', 
        'reviewboard.extensions.views.configure_extension',
        {
            'ext_class': TracLink,
            'form_class': TracLinkSettingsForm,
        }),

)
