#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import time
import pytest
import random
import string
from copy import deepcopy
from unittestzero import Assert

from pages.home import Home
from pages.profile import Profile


class TestProfilePage:

    def test_edit_profile_fields(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()

        profile_page = home_page.header.click_profile()
        user_edit_page = profile_page.click_edit_profile()
        Assert.true(user_edit_page.is_the_current_page)

        # save initial values to restore them after the test is finished
        fields_no = len(user_edit_page.profile_fields)
        initial_value = [None] * fields_no
        random_name = "test%s" % random.choice(string.lowercase)

        # enter new values
        for i in range(0, fields_no):
            initial_value[i] = deepcopy(user_edit_page.profile_fields[i].field_value)
            user_edit_page.profile_fields[i].clear_field()
            user_edit_page.profile_fields[i].type_value(random_name)

        user_edit_page.click_save_profile()
        Assert.true(profile_page.update_message)

        # go back and restore initial values
        profile_page.click_edit_profile()
        for i in range(0, fields_no):
            user_edit_page.profile_fields[i].clear_field()
            user_edit_page.profile_fields[i].type_value(initial_value[i])

        user_edit_page.click_save_profile()
