#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import Base
from pages.page import Page


class Profile(Base):

    _page_title = 'Mozilla Reps - Profile of webqabrowserid'

    _page_source_locator = (By.ID, 'wrapper')
    _user_avatar_locator = (By.ID, 'profiles-view-avatar')
    _edit_profile_button_locator = (By.CSS_SELECTOR, '.small.button')

    def __init__(self, testsetup):
        Base.__init__(self, testsetup)
        self.wait_for_element_visible(*self._user_avatar_locator)

    @property
    def profile_text(self):
        return self.selenium.find_element(*self._page_source_locator).text

    def click_edit_profile(self):
        self.selenium.find_element(*self._edit_profile_button_locator).click()
        return EditProfile(self.testsetup)


class EditProfile(Base):

    _profile_fields_locator = (By.CSS_SELECTOR, '#name-gender')
    _save_profile_button_locator = (By.ID, 'save-profile-button')

    @property
    def profile_fields(self):
        return [self.ProfileSection(self.testsetup, web_element)
                for web_element in self.selenium.find_elements(*self._profile_fields_locator)]

    def click_save_profile(self):
        self.selenium.find_element(*self._save_profile_button_locator).click()
        return Profile(self.testsetup)

    class ProfileSection(Page):

        _input_field_locator = (By.CSS_SELECTOR, ' input')

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def field_value(self):
            try:
                return self._root_element.find_element(*self._input_field_locator).get_attribute('value')
            except Exception.NoSuchAttributeException:
                return " "

        def type_value(self, value):
            if value != '':
                self._root_element.find_element(*self._input_field_locator).send_keys(value)

        def clear_field(self):
            self._root_element.find_element(*self._input_field_locator).clear()
