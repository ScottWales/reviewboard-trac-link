#!/usr/bin/env python
"""
file:   trac_link/extension.py
author: Scott Wales <scott.wales@unimelb.edu.au>

Copyright 2014 ARC Centre of Excellence for Climate Systems Science

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
# trac_link Extension for Review Board.

from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls.defaults import patterns, include
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import SignalHook
from reviewboard.reviews.signals import review_request_published
from trac import ticket, env, resource


class TracLink(Extension):
    metadata = {
        'Name': 'trac_link',
        'Summary': 'Post a link to review requests on Trac tickets',
    }
    is_configurable = True
    default_settings = {
        'tracsite': '/var/www/trac',
    }

    def initialize(self):
        # Hook on publishing & updating tickets
        SignalHook(self, review_request_published, self.on_published)

    def on_published(self, review_request=None, **kwargs):

        # Information about the review
        review_id = review_request.display_id
        ticket_ids = review_request.get_bug_list()

        # Connect to trac
        tracenv = env.open_environment(self.settings['tracsite'])

        # Add the review to each trac ticket
        for ticket_id in ticket_ids:
            try:
                tracticket = ticket.Ticket(tracenv,tkt_id=ticket_id)
                addTracLink(tracticket, 
                        review_request.display_id,
                        review_request.submitter)
            except resource.ResourceNotFound:
                # Ticket doesn't exist
                pass
        
        # Cleanup
        tracenv.shutdown()

def addTracLink(tracticket, review_id, submitter):
    "Add a link to the review to a Trac ticket"

    # Get the ticket's review list
    reviews = tracticket.get_value_or_default('reviews')
    if not reviews:
        reviews = u''

    # The link to the code review
    link=u'review:%s'%review_id

    # Add the new link to the review list
    reviewlist = [x.strip() for x in reviews.split(',')]
    if link in reviewlist:
        # Ticket already present
            return
    reviewlist.append(link)

    # Add a comment and save the change
    tracticket['reviews'] = u', '.join(reviewlist)
    reviewcomment = u"%s created review request review:%s\n"%(submitter,review_id)
    tracticket.save_changes(author=u'Reviewboard',comment=reviewcomment)

