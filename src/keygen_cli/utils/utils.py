import click
from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout


# MARK: Selection dialog
def create_selection_dialog(title, options, allow_abort=True, allow_no_selection=False):
    if not options:
        click.echo("No options available for selection.")
        return None

    kb = KeyBindings()
    selected_index = [0]
    scroll_offset = [0]
    terminal_height = 20  # Default height, will be updated dynamically

    @kb.add("up")
    def _(event):
        nonlocal selected_index, scroll_offset
        if selected_index[0] > 0:
            selected_index[0] -= 1
            if selected_index[0] < scroll_offset[0]:
                scroll_offset[0] = selected_index[0]

    @kb.add("down")
    def _(event):
        nonlocal selected_index, scroll_offset, terminal_height
        if selected_index[0] < len(options) - 1:
            selected_index[0] += 1
            max_visible_items = terminal_height - 3  # Adjust for title and abort message
            if selected_index[0] >= scroll_offset[0] + max_visible_items:
                scroll_offset[0] = selected_index[0] - max_visible_items + 1

    @kb.add("enter")
    def _(event):
        event.app.exit(result=options[selected_index[0]])

    @kb.add("c-c")
    @kb.add("q")
    def _(event):
        event.app.exit(result=None)

    def get_formatted_options():
        nonlocal terminal_height, scroll_offset
        max_visible_items = terminal_height - 3  # Adjust for title and abort message
        visible_options = options[scroll_offset[0] : scroll_offset[0] + max_visible_items]

        formatted_options = []
        for i, option in enumerate(visible_options, start=scroll_offset[0]):
            if i == selected_index[0]:
                formatted_options.append(f"<ansired>▸</ansired> {option[1]}")
            else:
                formatted_options.append(f"  {option[1]}")

        if len(options) > max_visible_items:
            formatted_options.append(
                f"  (Showing {scroll_offset[0] + 1}-{min(scroll_offset[0] + max_visible_items,
                                                         len(options))} of {len(options)})"
            )

        if allow_abort:
            formatted_options.append("  (Press 'q' to abort)")

        return HTML("\n".join(formatted_options))

    layout = Layout(
        HSplit(
            [
                Window(height=1, content=FormattedTextControl(title)),
                Window(content=FormattedTextControl(get_formatted_options))
            ]
        )
    )

    app = Application(
        layout=layout,
        key_bindings=kb,
        full_screen=True
    )

    # Determine terminal height dynamically
    try:
        terminal_height = app.output.get_size().rows
    except Exception:
        terminal_height = 20  # Fallback to default

    result = app.run()
    if result is None and allow_abort:
        click.echo("Aborted by user.")
        exit(1)
    return result[0] if result else None
