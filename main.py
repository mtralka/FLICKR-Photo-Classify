import gspread
from oauth2client.service_account import ServiceAccountCredentials
import PySimpleGUI as sg
import webbrowser

"""""
FLICKR Photo Classify V1.0
Matthew Tralka 2020
GNU General Public License v3.0
"""""

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("CREDS.json", scope)
client = gspread.authorize(creds)

question_count = 1
reviewed, first = False, True
global_Theme = 'Dark Grey 3'


def startup():
    sg.theme(global_Theme)
    title = 'Startup: Photo Classify'

    layout = [
        [sg.Text('Reviewer: '), sg.InputText(key='-reviewer-', size=(10, 1))],
        [sg.Text('Google Sheet Name: ', tooltip='Enter exactly as defined in Google Sheets'),
         sg.InputText(key='-sheet_name-', size=(10, 1))],
        [sg.Text('Column Number of "Direct Link": '), sg.InputText(key='-dlink_column-', size=(10, 1))],
        [sg.Text('Column Number of "Title": '), sg.InputText(key='-title_column-', size=(10, 1))],
        [sg.Text('Starting Row: '), sg.InputText(key='-dlink_row-', size=(10, 1))],
        [sg.Ok(), sg.Exit()],

    ]

    window = sg.Window(title, layout)

    while True:

        event, values_startup = window.read()

        if event is None or event == 'Exit':
            quit()

        if event == 'Ok':
            window.close()
            return values_startup


def main():
    global count

    big_font = 13
    small_font = 10
    font = 'Times New Roman'
    standard_col_size = (300, 70)
    input_col_size = (300, 85)
    standard_pad = (0, 0)
    sg.theme(global_Theme)
    title = 'Photo Classify'

    user_ID_plant = [

        [sg.Text('Does User ID Plants?', key='-is_user_ID-', visible=True, justification='left')],
        [sg.Button('Yes', key='-user_ID_yes-', visible=True),
         sg.Button('No', key='-user_ID_no-', visible=True)],

    ]
    user_ID_correct = [

        [sg.Text('Is User ID correct?', key='-is_user_ID_correct-', visible=True)],
        [sg.Button('Yes', key='-user_ID_correct_yes-', visible=True),
         sg.Button('No', key='-user_ID_correct_no-', visible=True),
         sg.Button('IDK', key='-user_ID_correct_idk-', visible=True)],

    ]
    user_ID_species = [

        [sg.Text('User Identified Species / Genus : ', visible=True)],
        [sg.InputText(enable_events=True, key='-user_plant_species-', size=(20, 1))],
        [sg.Button('Submit', key='-user_plant_species_done-')],

    ]
    individual_plant_visible = [
        [sg.Text('Are Individual Plants Visible?', visible=True)],
        [sg.Button('Yes', key='-individual_plant_visible_yes-', visible=True),
         sg.Button('No', key='-individual_plant_visible_no-', visible=True),
         sg.Button('IDK', key='-individual_plant_visible_idk-', visible=True)],

    ]
    plant_ID = [

        [sg.Text('Plant Species / Genus : ', visible=True)],
        [sg.InputText(enable_events=True, key='-plant_species-')],
        [sg.Button('Done', key='-plant_species_done-')],

    ]
    flowers_visible = [

        [sg.Text('Are Flowers Visible?', key='-plant-flowers-visible-', visible=True)],
        [sg.Button('Yes', key='-flower_visible_yes-', visible=True),
         sg.Button('No', key='-flower_visible_no-', visible=True),
         sg.Button('IDK', key='-flower_visible_idk-', visible=True)],

    ]
    flower_species = [

        [sg.Text('Flower Species / Genus : ', visible=True)],
        [sg.InputText(enable_events=True, key='-flower_species-')],
        [sg.Button('Submit', key='-flower_species_done-')],

    ]
    flowers_list = [

        [sg.Text('Are Flowers Black, Red, or Red List Species?', key='-flowers_on_list-', visible=True)],
        [sg.Button('Black', key='-flowers_on_list_black-', visible=True),
         sg.Button('Watch', key='-flowers_on_list_watch-', visible=True),
         sg.Button('Red', key='-flowers_on_list_red-', visible=True),
         sg.Button('No', key='-flowers_on_list_no-', visible=True),
         sg.Button('IDK', key='-flowers_on_list_idk-', visible=True)],
    ]
    plant_list_awareness = [

        [sg.Text('Were Users aware of these categories?', key='-flower_list_awareness-', visible=True)],
        [sg.Button('Yes', key='-flowers_on_list_awareness_yes-', visible=True),
         sg.Button('No', key='-flowers_on_list_awareness_no-', visible=True),
         sg.Button('IDK', key='-flowers_on_list_awareness_idk-', visible=True)],

    ]
    plant_tags = [

        [sg.Text('What Plant Tags are Used? : ', visible=True)],
        [sg.InputText(enable_events=True, key='-plant_tags-', focus=False, size=(20, 1))],
        [sg.Button('Submit', key='-plant_tags_done-')],

    ]
    plant_col = [

        [sg.Col(user_ID_plant, key='-plantsub1-', visible=True, pad=standard_pad, size=standard_col_size)],
        [sg.Col(user_ID_correct, key='-plantsub2-', visible=False, pad=standard_pad, size=standard_col_size)],
        [sg.Col(user_ID_species, key='-plantsub3-', visible=False, pad=standard_pad, size=input_col_size)],
        [sg.Col(individual_plant_visible, key='-plantsub4-', visible=False, pad=standard_pad, size=standard_col_size)],
        [sg.Col(plant_ID, key='-plantsub5-', visible=False, pad=standard_pad, size=input_col_size)],
        [sg.Col(flowers_visible, key='-plantsub6-', visible=False, pad=(0, 0), size=standard_col_size)],
        [sg.Col(flower_species, key='-plantsub7-', visible=False, pad=(0, 0), size=input_col_size)],
        [sg.Col(flowers_list, key='-plantsub8-', visible=False, pad=standard_pad, size=standard_col_size)],
        [sg.Col(plant_list_awareness, key='-plantsub9-', visible=False, pad=standard_pad, size=standard_col_size)],
        [sg.Col(plant_tags, key='-plantsub10-', visible=False, pad=standard_pad, size=input_col_size)],
    ]

    # """""""""
    # Landscape
    # """""""""
    landscape = [
        [sg.Text('Which Landscape is Visible?', visible=True)],
        [sg.Button('Sub-alpine forest', key='-subalpine-', visible=True)],
        [sg.Button('Alpine meadow', key='-alpine_meadow-', visible=True)],
        [sg.Button('Alpine scrub with low shrubs', tooltip='Rhododendron, Vaccinium, Juniperus', key='-alpine_scrub-',
                   visible=True)],
        [sg.Button('Other', key='-landscape_other-', visible=True)],

    ]

    landscape_other = [
        [sg.Text('Other, please clarify')],
        [sg.InputText(key='-land_other_input-', size=(20, 1), enable_events=True)],
        [sg.Button('Submit', key='-land_other_done-')],
    ]

    user_id_land = [
        [sg.Text('How does the user ID the landscape?', visible=True)],
        [sg.Button('Correctly', key='-landscape_ID_correct-', visible=True),
         sg.Button('Incorrectly', key='-landscape_ID_incorrect-', visible=True)],
        [sg.Button('No ID', key='-landscape_ID_no-', visible=True),
         sg.Button('Other', key='-landscape_ID_other-', visible=True)],

    ]

    user_ID_land_other = [
        [sg.Text('Other, please clarify')],
        [sg.InputText(key='-land_ID_input-', size=(20, 1), enable_events=True)],
        [sg.Button('Submit', key='-land_ID_done-')],

    ]

    landscape_col = [

        [sg.Col(landscape, key='-landsub1-', visible=True, pad=standard_pad, size=(300, 150))],
        [sg.Col(landscape_other, visible=False, key='-landsub2-', pad=standard_pad, size=input_col_size)],
        [sg.Col(user_id_land, key='-landsub3-', pad=standard_pad, visible=False, size=(300, 100))],
        [sg.Col(user_ID_land_other, visible=False, key='-landsub4-', pad=standard_pad, size=input_col_size)],

    ]

    # """""""""
    # Main Col and GUI
    # """""""""
    main_subjects = (
        'people', 'pets', 'livestock', 'wildlife', 'plant', 'landscape', 'water', 'recreation', 'building',
        'infrastructure',
        'subject_other_bool')

    main_languages = (
        'English', 'Italian', 'German', 'French', 'Other'
    )

    col_schema = (
        "Reviewer", "Main Subject", 'Languages', "Does User ID Plant", "Is ID Correct", "User Defined Plant Species",
        "Are Individual Plant Species Visible?", "Plant Species / Genus", "Are Flowers Visible?",
        "Flower Species / Genus", "Black / Watch / Red List?", "Were Users Aware?", "What Tags are Used?",
        "Which Landscape is Visible?", "How does the user ID the landscape?")

    subject_col = [
        [sg.Text('Title: ', font=(font, big_font), justification='left', size=(5, 1)),
         sg.Text('', font=(font, big_font), size=(20, 1), key='-photo_title-', justification='left'), sg.Exit(pad=(2, 2))],
        [sg.Text('Photo Subject:', font=(font, big_font), justification='center')],
        [sg.Checkbox('People', default=False, font=(font, small_font), key='-people-')],
        [sg.Checkbox('Pets', default=False, font=(font, small_font), key='-pets-')],
        [sg.Checkbox('Livestock (e.g. cows, sheep)', default=False, font=(font, small_font), key='-livestock-')],
        [sg.Checkbox('Wildlife', default=False, font=(font, small_font), key='-wildlife-')],

        [sg.Checkbox('Plant(s)', default=False, font=(font, small_font), key='-plant-', enable_events=True)],
        [sg.Checkbox('Natural Landscape', tooltip="mountains, meadows, forests", default=False, font=(font, small_font),
                     key='-landscape-', enable_events=True)],

        [sg.Checkbox('Water Feature', tooltip='g. stream, lake, river', default=False, font=(font, small_font),
                     key='-water-')],
        [sg.Checkbox('Recreational', tooltip='hiking, biking, fishing', default=False, font=(font, small_font),
                     key='-recreation-')],
        [sg.Checkbox('Building(s)', default=False, font=(font, small_font), key='-building-')],
        [sg.Checkbox('Infrastructure', default=False, font=(font, small_font), key='-infrastructure-')],
        [sg.Checkbox('Other', default=False, font=(font, small_font), key='-subject_other_bool-'),
         sg.InputText(size=(11, 1), key='-subject_other-')],
        [sg.Text()],
        [sg.Text('Post Language: ', font=(font, big_font), justification='center')],
        [sg.Checkbox('English', default=False, font=(font, small_font), key='-English-'),
         sg.Checkbox('Italian', default=False, font=(font, small_font), key='-Italian-')],
        [sg.Checkbox('German', default=False, font=(font, small_font), key='-German-'),
         sg.Checkbox('French', default=False, font=(font, small_font), key='-French-')],
        [sg.Checkbox('Other: ', default=False, font=(font, small_font), key='-language_other_bool-'),
         sg.InputText('', size=(10, 1), key='-language_other-')],

        [sg.Text('----------')],
        [sg.Text('Go to Row: ', font=(font, small_font)), sg.InputText(key='-go_to_page_number-', size=(4, 1)),
         sg.Button('Go', key='-go_to_page-')],
    ]

    main_col = [

        [sg.Col(subject_col, justification='left', element_justification='Left', pad=(0, 0)),
         sg.Col(plant_col, visible=False, key='-plantcol-', scrollable=False, element_justification='left',
                justification='right'),
         sg.Col(landscape_col, visible=False, key='-landcol-', element_justification='left',
                justification='right')],

    ]
    bottom_buttons = [
        [sg.Button('', button_color=(sg.theme_background_color(), sg.theme_background_color()),
                   image_filename='arrow-bar-left-red.png', image_subsample=8, border_width=0, key='-previous-'),
         sg.Button('', button_color=(sg.theme_background_color(), sg.theme_background_color()),
                   image_filename='arrow-bar-right-green.png', image_subsample=8, border_width=0, key='-next-')],

    ]

    layout = [
        [sg.Col(main_col, justification='left', element_justification='center', pad=standard_pad)],
        [sg.Col(bottom_buttons, justification='left', pad=((80, 10), (0, 0)))]

    ]

    window = sg.Window(title, layout, resizable=True, keep_on_top=True, no_titlebar=True, grab_anywhere=True)

    def submit_changes():

        subjects, languages = '', ''
        try:
            # Subject Submit
            for x in range(0, len(main_subjects) - 1):
                if bool(values[f'-{main_subjects[x]}-']):
                    subjects += ', ' + str(main_subjects[x])

            if bool(values['-subject_other_bool-']):
                subjects += ', ' + values['-subject_other-']
            if len(subjects) > 2:
                subjects = subjects[1:]
            write_response(bool_message=None, header='Main Subject', message=subjects)

            # Language Submit
            for x in range(0, len(main_languages) - 1):
                if bool(values[f'-{main_languages[x]}-']):
                    languages += ', ' + str(main_languages[x])

            if bool(values['-language_other_bool-']):
                languages += ', ' + values['-language_other-']
            if len(languages) > 2:
                languages = languages[1:]
            write_response(bool_message=None, header='Languages', message=languages)


        except:
            print('Submit Changes Error')

    def clear_plants():
        clear_col(col='plant', max_sub=10)
        window['-plant_tags-'].update('')
        window['-flower_species-'].update('')
        window['-user_plant_species-'].update('')

    def clear_landscape():
        clear_col(col='land', max_sub=4)
        window['-land_other_input-'].update('')
        window['-land_ID_input-'].update('')

    def clear_selection():
        for x in range(0, len(main_subjects) - 1):
            window[f'-{main_subjects[x]}-'].update(False)

        window['-subject_other_bool-'].update(False)
        window['-subject_other-'].update('')
        for x in range(0, len(main_languages) - 1):
            window[f'-{main_languages[x]}-'].update(False)

        window['-language_other_bool-'].update(False)
        window['-language_other-'].update('')
        window['-go_to_page_number-'].update('')

        clear_plants()
        clear_landscape()

    def image_change(next):
        global count, reviewed, title_col

        if next:
            count += 1
            image_link = sheet.cell(count, int(values_startup['-dlink_column-'])).value
        else:
            count -= 1
            image_link = sheet.cell(count, int(values_startup['-dlink_column-'])).value

        existing = sheet.cell(count, int(col_schema.index('Reviewer') + int(starting_col) + 1)).value

        # Read and Update Title
        window.Read(timeout=2)
        window['-photo_title-'].update(sheet.cell(count, title_col).value)

        if len(str(existing)) > 0:
            reviewed = True
        else:
            reviewed = False

        try:
            webbrowser.open(image_link, new=0)
            write_response(bool_message=None, header='Reviewer', message=values_startup['-reviewer-'])
        except:
            sg.ErrorElement('Error')
            image_change(next=True)

    def clear_col(col, max_sub):
        global question_count

        window[f'-{col}col-'].update(visible=False)

        for x in range(1, max_sub + 1):
            sg.Col.hide_row(window[f'-{col}sub{x}-'])
            window[f'-{col}sub{max_sub + 1 - x}-'].update(visible=False)

        question_count = 1

    def question_response(col, skip):
        global question_count

        if col == 'plant' and skip <= 10:
            question_count += skip

            window[f'-{col}sub{question_count}-'].update(visible=True)
            sg.Col.unhide_row(window[f'-{col}sub{question_count}-'])

        elif col == 'land' and skip <= 4:
            question_count += skip

            window[f'-{col}sub{question_count}-'].update(visible=True)
            sg.Col.unhide_row(window[f'-{col}sub{question_count}-'])

    def write_response(message, header, bool_message):
        global reviewed, count

        existing_message = str(sheet.cell(count, int(col_schema.index(header)) + int(starting_col) + 1).value)

        if bool_message:
            message = 'Yes'
        elif type(message) == str:
            pass
        else:
            message = 'No'

        if reviewed:
            message = existing_message + ' | ' + message

        sheet.update_cell(count, int(col_schema.index(header)) + int(starting_col) + 1, message)

    # First Run
    image_change(next=False)
    first_click = True

    while True:
        global question_count, count
        event, values = window.read()

        if event is None or event == 'Exit':
            break

        # """""""""
        # Plants
        # """""""""
        if event == '-plant-':
            if first_click:
                window['-plantcol-'].update(visible=True)
                question_response(col='plant', skip=0)
                first_click = False
            else:
                clear_plants()
                first_click = True

        if event == '-user_ID_yes-':
            question_count = 1
            write_response(bool_message=True, header='Does User ID Plant', message=None)
            question_response(col='plant', skip=1)
        elif event == '-user_ID_no-':
            question_count = 1
            write_response(bool_message=False, header='Does User ID Plant', message=None)
            question_response(col='plant', skip=3)

        if event == '-user_ID_correct_yes-':
            question_count = 2
            write_response(bool_message=True, header='Is ID Correct', message=None)
            question_response(col='plant', skip=1)
        elif event == '-user_ID_correct_no-':
            question_count = 2
            write_response(bool_message=False, header='Is ID Correct', message=None)
            question_response(col='plant', skip=2)
        elif event == '-user_ID_correct_idk-':
            question_count = 2
            write_response(bool_message=False, header='Is ID Correct', message='IDK')
            question_response(col='plant', skip=1)

        if event == '-user_plant_species_done-':
            question_count = 3
            write_response(bool_message=False, header='User Defined Plant Species',
                           message=str(values['-user_plant_species-']))
            question_response(col='plant', skip=1)

        if event == '-individual_plant_visible_yes-':
            question_count = 4
            question_response(col='plant', skip=1)
            write_response(bool_message=True, header='Are Individual Plant Species Visible?', message=None)
        elif event == '-individual_plant_visible_no-':
            question_count = 4
            question_response(col='plant', skip=2)
            write_response(bool_message=False, header='Are Individual Plant Species Visible?', message=None)
        elif event == '-individual_plant_visible_idk-':
            question_count = 4
            question_response(col='plant', skip=2)
            write_response(bool_message=None, header='Are Individual Plant Species Visible?', message='IDK')

        if event == '-plant_species_done-':
            question_count = 5
            question_response(col='plant', skip=1)
            write_response(bool_message=False, header='Plant Species / Genus', message=str(values['-plant_species-']))

        if event == '-flower_visible_yes-':
            question_count = 6
            question_response(col='plant', skip=1)
            write_response(bool_message=True, header='Are Flowers Visible?', message=None)
        elif event == '-flower_visible_no-':
            question_response(col='plant', skip=4)
            write_response(bool_message=False, header='Are Flowers Visible?', message=None)
            question_count = 6
        elif event == '-flower_visible_idk-':
            question_count = 6
            question_response(col='plant', skip=4)
            write_response(bool_message=None, header='Are Flowers Visible?', message='IDK')

        if event == '-flower_species_done-':
            question_count = 7
            question_response(col='plant', skip=1)
            write_response(bool_message=False, header='Flower Species / Genus', message=str(values['-flower_species-']))

        if event == '-flowers_on_list_black-':
            question_count = 8
            question_response(col='plant', skip=1)
            write_response(bool_message=None, header='Black / Watch / Red List?', message='Black')
        elif event == '-flowers_on_list_watch-':
            question_count = 8
            question_response(col='plant', skip=1)
            write_response(bool_message=None, header='Black / Watch / Red List?', message='Watch')
        elif event == '-flowers_on_list_red-':
            question_count = 8
            question_response(col='plant', skip=1)
            write_response(bool_message=None, header='Black / Watch / Red List?', message='Red')
        elif event == '-flowers_on_list_no-':
            question_count = 8
            question_response(col='plant', skip=1)
            write_response(bool_message=False, header='Black / Watch / Red List?', message='No')
        elif event == 'flowers_on_list_idk-':
            question_count = 8
            question_response(col='plant', skip=1)
            write_response(bool_message=True, header='Black / Watch / Red List?', message='IDK')

        if event == '-flowers_on_list_awareness_yes-':
            question_count = 9
            question_response(col='plant', skip=1)
            write_response(bool_message=True, header='Were Users Aware?', message='')
        elif event == '-flowers_on_list_awareness_no-':
            question_count = 9
            question_response(col='plant', skip=1)
            write_response(bool_message=False, header='Were Users Aware?', message='No')
        elif event == '-flowers_on_list_awareness_idk-':
            question_count = 9
            question_response(col='plant', skip=1)
            write_response(bool_message=None, header='Were Users Aware?', message='IDK')

        if event == '-plant_tags_done-':
            question_count = 10
            write_response(bool_message=False, header='What Tags are Used?', message=str(values['-plant_tags-']))
            window['-plantcol-'].update(visible=False)
            first_click = True

        # """""""""
        # Landscape
        # """""""""
        if event == '-landscape-':
            if first_click:
                window['-plantcol-'].update(visible=False)
                window['-landcol-'].update(visible=True)
                question_response(col='land', skip=0)
                first_click = False
            else:
                clear_landscape()
                first_click = True

        if event == '-subalpine-':
            question_count = 1
            question_response(col='land', skip=2)
            write_response(bool_message=False, header='Which Landscape is Visible?', message='Subalpine Forest')
        elif event == '-alpine_meadow-':
            question_count = 1
            question_response(col='land', skip=2)
            write_response(bool_message=False, header='Which Landscape is Visible?', message='Alpine Meadow')
        elif event == '-alpine_scrub-':
            question_count = 1
            question_response(col='land', skip=2)
            write_response(bool_message=False, header='Which Landscape is Visible?', message='Alpine Scrub')
        elif event == '-landscape_other-':
            question_count = 1
            question_response(col='land', skip=1)

        if event == '-land_other_done-':
            question_count = 2
            question_response(col='land', skip=1)
            write_response(bool_message=False, header='Which Landscape is Visible?',
                           message=values['-land_other_input-'])

        if event == '-landscape_ID_correct-':
            question_count = 3
            write_response(bool_message=False, header='How does the user ID the landscape?', message='Correctly')
            window['-landcol-'].update(visible=False)
            first_click = True
        elif event == '-landscape_ID_incorrect-':
            question_count = 3
            write_response(bool_message=False, header='How does the user ID the landscape?', message='Incorrectly')
            window['-landcol-'].update(visible=False)
            first_click = True
        elif event == '-landscape_ID_no-':
            question_count = 3
            write_response(bool_message=False, header='How does the user ID the landscape?', message='No ID')
            window['-landcol-'].update(visible=False)
            first_click = True
        elif event == '-landscape_ID_other-':
            question_count = 3
            question_response(col='land', skip=1)

        if event == '-land_ID_done-':
            question_count = 4
            write_response(bool_message=False, header='How does the user ID the landscape?',
                           message=values['-land_ID_input-'])
            window['-landcol-'].update(visible=False)
            first_click = True

        # """""""""
        # Buttons
        # """""""""
        if event == '-previous-':
            first_click = True
            submit_changes()
            clear_selection()
            image_change(next=False)

        if event == '-next-':
            first_click = True
            submit_changes()
            clear_selection()
            image_change(next=True)

        if event == '-go_to_page-':
            count = int(values['-go_to_page_number-']) - 1
            clear_selection()
            image_change(next=True)


values_startup = startup()
sheet = client.open(values_startup['-sheet_name-']).sheet1

count = int(values_startup['-dlink_row-'])
count += 1

starting_row = int(values_startup['-dlink_row-']) + 1
starting_col = values_startup['-dlink_column-']
title_col = values_startup['-title_column-']

main()
