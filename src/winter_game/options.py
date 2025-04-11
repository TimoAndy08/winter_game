def options(position, option_placement, save_file, event):
    if event.button == 1:
        if option_placement == "load_save":
            if 100 <= position <= 150:
                return ("change", "save_selection")
            elif 200 <= position <= 250:
                return ("change", "save_creation")
        elif option_placement.split("_")[0] == "save" and len(save_file) > 0:
            if 200 <= position <= 250:
                if option_placement == "save_creation":
                    return ("create", "main_game")
                elif option_placement == "save_selection":
                    return ("load", "main_game")
        elif option_placement.split("_")[0] == "options":
            if option_placement == "options_game":
                if 0 <= position <= 50:
                    option_placement = "main_game"
                elif 100 <= position <= 150:
                    return ("save", "main_menu")
            elif option_placement == "options_main":
                if 0 <= position <= 50:
                    return ("change", "main_menu")
            if 200 <= position <= 250:
                return ("control", "controls_options")
        elif option_placement == "main_menu":
            if 0 <= position <= 50:
                return ("change", "load_save")
            elif 100 <= position <= 150:
                return ("change", "options_main")
            elif 200 <= position <= 250:
                return ("exit", "exit")
        elif option_placement == "controls_options":
            if 0 <= position <= 50:
                if len(save_file) == 0:
                    return ("change", "options_main")
                else:
                    return ("change", "options_game")
    elif option_placement == "controls_options":
        return ("adjust", -(event.button == 6) + (event.button == 7))
    return ("change", option_placement)