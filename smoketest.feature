Feature: Smoke tests

  Background:
    * Make sure that gnome-weather is running

  @add_new_cities
  Scenario: Add new cities
    * Add random city
    * Select added city
    * Show forecast details
    Then forecast for today is shown
    * Hide forecast details
    Then forecast for today is hidden

  @remove_cities
  Scenario: Remove cities
    * Add random city
    * Remove last added city
    Then no cities displayed

  @back_to_world_weather
  Scenario: Back to world weather
    * Add random city
    * Select added city
    * Return to World Weather
    Then a list of cities is displayed
