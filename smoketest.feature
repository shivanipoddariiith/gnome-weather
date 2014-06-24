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

  @select_all_cities
  Scenario: Back to world weather
    * Add random city
    * Add random city
    * Press "<Ctrl>a"
    * Delete selected cities
    Then no cities displayed

  @escape_win_selection
  Scenario: Back to world weather
    * Press new to add city
    * Press "Escape"
    Then no cities displayed

  #@refresh_weather
  #Scenario: Back to world weather
  #  * Add random city
  #  * Select Added city
  #  * Refresh forecast for selected city
  #  Then loading page is visible
