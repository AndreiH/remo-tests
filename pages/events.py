#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base import Base
from pages.create_event import CreateEvent
from pages.event_detail import EventDetail


class Events(Base):

    _page_title = 'Mozilla Reps - Events'
    _advanced_options_button_locator = (By.ID, 'adv-search-icon-events')
    _advanced_search_form_locator = (By.ID, 'searchform')
    _create_event_button_locator = (By.ID, 'events-create-button')
    _event_deleted_message_locator = (By.CSS_SELECTOR, '.success')
    _events_filter_locator = (By.ID, 'searchfield')
    _events_location_locator = (By.CSS_SELECTOR, 'div.events-table-location')
    _events_location_links_locator = (By.CSS_SELECTOR, 'div.events-table-location a')
    _events_map_locator = (By.ID, 'map')
    _events_timeline_button_locator = (By.ID, 'events-timeline-button')
    _events_timeline_locator = (By.ID, 'event-timeline')
    _events_table_locator = (By.ID, 'events-table-body')
    _events_result_locator = (By.CSS_SELECTOR, '#events-table-body .event-item')
    _events_owner_locator = (By.CSS_SELECTOR, 'div.events-table-owner a')
    _events_icalendar_export_button_locator = (By.ID, 'icalendar-export-button')
    _filter_for_event_locator = (By.CSS_SELECTOR, 'div.events-table-name.hide-for-small a')

    def __init__(self, testsetup):
        Base.__init__(self, testsetup)
        # Wait for the page to be populated
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: len(s.find_elements(*self._events_map_locator)))

    @property
    def is_event_deleted_message_visible(self):
        return self.is_element_visible(*self._event_deleted_message_locator)

    @property
    def is_events_map_visible(self):
        return self.is_element_visible(*self._events_map_locator)

    @property
    def is_events_timeline_visible(self):
        return self.is_element_visible(*self._events_timeline_locator)

    @property
    def is_events_table_visible(self):
        return self.is_element_visible(*self._events_table_locator)

    @property
    def is_event_profile_result_visible(self):
        return self.is_element_visible(*self._events_result_locator)

    @property
    def is_events_icalendar_export_button_visible(self):
        return self.is_element_visible(*self._events_icalendar_export_button_locator)

    @property
    def is_advanced_search_form_visible(self):
        return self.is_element_visible(*self._advanced_search_form_locator)

    @property
    def event_profile_location_text(self):
        return self.selenium.find_element(*self._events_location_locator).text

    @property
    def event_profile_owner_text(self):
        return self.selenium.find_element(*self._events_owner_locator).text

    @property
    def event_owners(self):
        return [event.text for event in self.selenium.find_elements(*self._events_owner_locator)]

    def select_random_event_owner(self):
        return random.choice(self.event_owners)

    @property
    def events_icalendar_export_button_url(self):
        return self.selenium.find_element(*self._events_icalendar_export_button_locator).get_attribute('href')

    @property
    def event_items_count(self):
        return self.selenium.find_elements(*self._events_result_locator)

    @property
    def event_locations(self):
        return self.get_locations()

    def get_locations(self):
        return self.selenium.find_elements(*self._events_location_links_locator)

    def select_random_event_location(self):
        return self.event_locations[random.randint(0, len(self.event_locations) - 1)].text

    def filter_for(self, search_term):
        element = self.selenium.find_element(*self._events_filter_locator)
        element.send_keys(search_term)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: not s.find_element_by_id('canvasLoader').is_displayed())

    def click_advanced_options(self):
        self.selenium.find_element(*self._advanced_options_button_locator).click()

    def click_create_event_button(self):
        self.selenium.find_element(*self._create_event_button_locator).click()
        return CreateEvent(self.testsetup)

    def click_filtered_event(self):
        self.selenium.find_element(*self._filter_for_event_locator).click()
        return EventDetail(self.testsetup)

    def click_timeline(self):
        self.selenium.find_element(*self._events_timeline_button_locator).click()
