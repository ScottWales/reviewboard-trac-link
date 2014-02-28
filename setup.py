from __future__ import unicode_literals

from reviewboard.extensions.packaging import setup


PACKAGE = "trac_link"
VERSION = "0.1"

setup(
    name=PACKAGE,
    version=VERSION,
    description="Link review requests with Trac tickets",
    author="Scott Wales",
    packages=[str("trac_link")],
    entry_points={
        'reviewboard.extensions':
            '%s = trac_link.extension:TracLink' % PACKAGE,
    },
    install_requires=['Trac>=1.0','Django<1.6','ReviewBoard'],
)
