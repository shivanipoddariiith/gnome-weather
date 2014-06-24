# -*- coding: UTF-8 -*-
from behave import step

from dogtail.tree import root
from behave_common_steps import *
from random import sample
from behave_common_steps import limit_execution_time_to


CITIES = [
    { 'partial': 'Brno',
      'full':    'Brno, Czech Republic'},
    { 'partial': 'Minsk',
      'full':    'Minsk (Loshitsa / Minsk International), Belarus'},
    { 'partial': 'New York',
      'full':    'Albany, New York, United States'},
]

@step(u'Press new to add city')
def press_new_to_add_city(context):
    context.app.instance.button("New").click()

@step(u'Add random city')
def add_random_city(context):
    # Choose a random city out of the list
    context.random_city = sample(CITIES, 1)[0]

    # Remember a number of icons
    icons_num = len(context.app.instance.child(roleName='layered pane').\
        findChildren(lambda x: x.roleName == 'icon'))

    context.app.instance.button("New").click()

    dialog = context.app.instance.dialog("New Location")
    # Probably a bug: textfield should be labelled
    #dialog.childLabelled('Search for a city:').typeText(context.random_city)

    textentry = dialog.textentry('')
    textentry.grabFocus()
    textentry.typeText(context.random_city['partial'])
    # Wait for autocompletion
    sleep(0.1)
    textentry.keyCombo("<Down>")
    textentry.keyCombo("<Enter>")

    assert textentry.text == context.random_city['full'],\
        "Incorrect full city name, expected '%s'" % context.random_city['full']
    dialog.button('Add').click()

    # A new icon should be added
    new_icons_num = len(context.app.instance.child(roleName='layered pane').\
        findChildren(lambda x: x.roleName == 'icon'))

    assert new_icons_num == icons_num + 1,\
        "Incorrect icon number, expected '%s' but was '%s'" % (icons_num+1, new_icons_num)


@step(u'Select added city')
def select_added_city(context):
    # As gnome-weather is poorly introspected we should choose the last icon
    pane = context.app.instance.child(roleName='layered pane')
    pane.findChildren(lambda x: x.roleName == 'icon')[-1].click()

    wait_for_loading_screen_to_disappear(context)

    # Pane becomes hidden
    assert context.app.instance.child('World Weather').showing, "World Weather button is hidden"
    assert not context.app.instance.child('New').showing, "New button is not hidden"


@limit_execution_time_to(30)
def wait_for_loading_screen_to_disappear(context):
    spinner = context.app.instance.child('Spinner')
    while(spinner.showing):
        sleep(0.5)

    sleep(0.5)


@step(u'{action:w} forecast details')
def forecast_details(context, action):
    if action not in ['Show', 'Hide']:
        raise RuntimeError("Incorrect action: %s" % action)

    context.app.instance.child(roleName='push button').click()
    # FIXME: check that forecast is displayed/hidden

@then(u'forecast for today is {state:w}')
def forecast_for_today(context, state):
    if state not in ['shown', 'hidden']:
        raise RuntimeError("Incorrect state: %s" % state)

    boolean_state = state == 'shown'
    label = context.app.instance.child("Forecast for Today")
    assert label.showing == boolean_state

@step(u'Refresh forecast for selected city')
def refresh_forecast(context):
    context.app.instance.child(roleName='layered pane').button("Refresh").click()

@then(u'loading page is visible')
def loading_page_visible(context):
    pane = context.app.instance.child(roleName='layered pane')
    assert pane.label('Loading...')

@step(u'Remove last added city')
def remove_last_added_city(context):
    pane = context.app.instance.child(roleName='layered pane')
    # Right-click the icon
    pane.findChildren(lambda x: x.roleName == 'icon')[-1].click(button=3)
    context.app.instance.button("Delete").click()
    context.app.instance.button("Done").click() 

@step(u'Delete selected cities')
def delete_selected_cities(context):
    context.app.instance.button("Delete").click()
    context.app.instance.button("Done").click() 

@then(u'no cities displayed')
def no_cities_displayed(context):
    pane = context.app.instance.child(roleName='layered pane')
    actual = len(pane.findChildren(lambda x: x.roleName == 'icon'))

    assert actual == 0, "%s cities displayed, though none expected" % actual


@step(u'Return to World Weather')
def return_to_world_weather(context):
    context.app.instance.button("World Weather").click()
    # Give it some time to display the list
    sleep(0.1)


@then(u'a list of cities is displayed')
def list_of_cities_is_displayed(context):
    pane = context.app.instance.child(roleName='layered pane')
    cities_container = pane.child(roleName='icon').parent

    assert cities_container.showing, "Cities list is not visible"

    
