from gui.components import Button


def cursor_handler(game, *, buttons: list[Button]):
    if not game.cursor:
        return

    if len(buttons):
        any_hover = False
        any_click = False

        for button in buttons:
            if button.hovered:
                any_hover = True
            if button.clicked:
                any_click = True

        if any_click:
            game.cursor.set_state("click")
        elif any_hover:
            game.cursor.set_state("hover")
        else:
            game.cursor.set_state("normal")
