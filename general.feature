Feature: General actions

  @start_via_command
  Scenario: Start via command
    * Start Weather via command
    Then gnome-weather should start

  @start_via_menu
  Scenario: Start via menu
    * Start Weather via menu
    Then gnome-weather should start

  @quit_via_shortcut
  Scenario: Ctrl-Q to quit application
    * Start Weather via command
    * Press "<Ctrl>q"
    Then gnome-weather shouldn't be running anymore

  @close_via_gnome_panel
  Scenario: Close via menu
    * Start Weather via menu
    * Click "Quit" in GApplication menu
    Then Weather shouldn't be running anymore
