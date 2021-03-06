#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import Base


class EventDetail(Base):

    _button = (By.ID, 'event-attend-button')
    _edit_event_button_locator = (By.CSS_SELECTOR, 'div.hide-for-small:nth-child(2) > a:nth-child(3)')
    _event_description_locator = (By.CSS_SELECTOR, '.profile-item:nth-child(2)')
    _event_name_locator = (By.CSS_SELECTOR, '.event-single-title')
    _event_saved_message_locator = (By.CSS_SELECTOR, '.success')

    @property
    def description(self):
        return self.selenium.find_element(*self._event_description_locator).text

    @property
    def is_event_saved_message_visible(self):
        return self.is_element_visible(*self._event_saved_message_locator)

    @property
    def name(self):
        return self.selenium.find_element(*self._event_name_locator).text

    def click_edit_event_button(self):
        self.selenium.find_element(*self._edit_event_button_locator).click()
        from pages.edit_event import EditEvent
        return EditEvent(self.testsetup)
