import typer


string_to_print = "Hello, dog.\nWho's a good boy? Is it you?\nYes. Yes it is."
time_dictionary = {
    '.': 1.,
    ',': .5,
    ';': .7,
    ':': .8,
    '?': 1.,
    '!': 1.,
    ' ': .1,
}

typer.typer(string_to_print, time_dictionary)
