def render_menu(WINDOW, MENU_FONT, menu_placement, save_file_name, control_names, control_adjusted, controls):
    if menu_placement == "load_save":
        WINDOW.blit(MENU_FONT.render("Load save?", False, (19, 17, 18)), (0, 0))
        WINDOW.blit(MENU_FONT.render("Yes", False, (19, 17, 18)), (0, 100))
        WINDOW.blit(MENU_FONT.render("No", False, (19, 17, 18)), (0, 200))
    elif menu_placement.split("_")[0] == "save":
        if menu_placement == "save_creation":
            WINDOW.blit(MENU_FONT.render("Name your new save?", False, (19, 17, 18)), (0, 0))
        if menu_placement == "save_selection":
            WINDOW.blit(MENU_FONT.render("Which save to load?", False, (19, 17, 18)), (0, 0))
        WINDOW.blit(MENU_FONT.render(save_file_name, False, (19, 17, 18)), (0, 100))
        WINDOW.blit(MENU_FONT.render("Proceed", False, (19, 17, 18)), (0, 200))
    elif menu_placement.split("_")[0] == "options":
        if menu_placement == "options_game":
            WINDOW.blit(MENU_FONT.render("Return to game", False, (19, 17, 18)), (0, 0))
            WINDOW.blit(MENU_FONT.render("Save and Quit", False, (19, 17, 18)), (0, 100))
        elif menu_placement == "options_main":
            WINDOW.blit(MENU_FONT.render("Back to menu", False, (19, 17, 18)), (0, 0))
        WINDOW.blit(MENU_FONT.render("Controls options", False, (19, 17, 18)), (0, 200))
    elif menu_placement == "main_menu":
        WINDOW.blit(MENU_FONT.render("Play", False, (19, 17, 18)), (0, 0))
        WINDOW.blit(MENU_FONT.render("Options", False, (19, 17, 18)), (0, 100))
        WINDOW.blit(MENU_FONT.render("Quit Game", False, (19, 17, 18)), (0, 200))
    elif menu_placement == "controls_options":
        WINDOW.blit(MENU_FONT.render("Proceed", False, (19, 17, 18)), (0, 0))
        WINDOW.blit(MENU_FONT.render(f"{control_names[control_adjusted]}: {chr(controls[control_adjusted])}", False, (19, 17, 18)), (0, 100))