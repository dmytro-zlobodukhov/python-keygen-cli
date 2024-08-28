import click
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.formatted_text import HTML


# MARK: Selection dialog
def create_selection_dialog(title, options, allow_abort=True, allow_no_selection=False):
    if not options:
        click.echo("No options available for selection.")
        return None

    kb = KeyBindings()
    selected_index = [0]

    @kb.add('up')
    def _(event):
        selected_index[0] = (selected_index[0] - 1) % len(options)

    @kb.add('down')
    def _(event):
        selected_index[0] = (selected_index[0] + 1) % len(options)

    @kb.add('enter')
    def _(event):
        event.app.exit(result=options[selected_index[0]])

    @kb.add('c-c')
    @kb.add('q')
    def _(event):
        event.app.exit(result=None)

    def get_formatted_options():
        formatted_options = []
        for i, option in enumerate(options):
            if i == selected_index[0]:
                formatted_options.append(f"<ansired>▸</ansired> {option[1]}")
            else:
                formatted_options.append(f"  {option[1]}")
        
        if allow_abort:
            formatted_options.append("  (Press 'q' to abort)")
        
        return HTML('\n'.join(formatted_options))

    layout = Layout(
        HSplit([
            Window(height=1, content=FormattedTextControl(title)),
            Window(content=FormattedTextControl(get_formatted_options))
        ])
    )

    app = Application(
        layout=layout,
        key_bindings=kb,
        full_screen=True
    )

    result = app.run()
    if result is None and allow_abort:
        click.echo("Aborted by user.")
        exit(1)
    return result[0] if result else None