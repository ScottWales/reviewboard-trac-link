from __future__ import unicode_literals

from reviewboard.extensions.packaging import setup


PACKAGE = "traclink"
VERSION = "0.2"

setup(
    name=PACKAGE,
    version=VERSION,
    description="Link review requests with Trac tickets",
    author="Scott Wales",
    packages=[str("traclink")],
    entry_points={
        'reviewboard.extensions':
            '%s = traclink.extension:TracLink' % PACKAGE,
    },
    install_requires=['Trac>=1.0','Django','ReviewBoard','Genshi'],
)
