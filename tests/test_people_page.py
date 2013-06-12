#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert
from pages.link_crawler import LinkCrawler

from pages.people import People


class TestPeoplePage:

    @pytest.mark.nondestructive
    def test_people_map_is_visible(self, mozwebqa):
        people_page = People(mozwebqa)
        people_page.go_to_people_page()
        Assert.true(people_page.is_people_map_visible)

    @pytest.mark.nondestructive
    def test_profile_grid_is_visible(self, mozwebqa):
        people_page = People(mozwebqa)
        people_page.go_to_people_page()
        Assert.true(people_page.is_profile_grid_visible)
        Assert.true(people_page.is_profile_name_visible)
        Assert.true(people_page.is_profile_image_visible)

    @pytest.mark.nondestructive
    def test_people_page_links(self, mozwebqa):
        crawler = LinkCrawler(mozwebqa)
        urls = crawler.collect_links('/people', id='wrapper')
        bad_urls = []

        Assert.greater(len(urls), 0, u'something went wrong. no links found.')

        for url in urls:
            check_result = crawler.verify_status_code_is_ok(url)
            if check_result is not True:
                bad_urls.append(check_result)

        Assert.equal(
            0, len(bad_urls),
            u'%s bad links found. ' % len(bad_urls) + ', '.join(bad_urls))

    @pytest.mark.nondestructive
    @pytest.mark.xfail(reason="Issue 67 - test_filter_results_by_name CI fail")
    # https://github.com/mozilla/remo-tests/issues/67
    def test_filter_results_by_name(self, mozwebqa):
        # Verify name in search matches query results
        query = u'Reps'
        people_page = People(mozwebqa)
        people_page.go_to_people_page()
        people_page.filter_for(query)
        Assert.equal(u'Reps', people_page.people_name_text)

        # Check profile to verify search results where search does not match name
        query = u'moz_reps_user'
        people_page.go_to_people_page()
        people_page.filter_for(query)
        profile_page = people_page.click_to_open_profile()
        Assert.contains(query, profile_page.profile_text)
