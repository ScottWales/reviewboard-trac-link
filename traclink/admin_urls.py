from __future__ import unicode_literals

from django.conf.urls import patterns, url

from traclink.extension import TracLink
from traclink.forms import TracLinkSettingsForm


urlpatterns = patterns('',
    url(r'^$', 
        'reviewboard.extensions.views.configure_extension',
        {
            'ext_class': TracLink,
            'form_class': TracLinkSettingsForm,
        }),

)
