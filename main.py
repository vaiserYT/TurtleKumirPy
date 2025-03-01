import tkinter
import re
from turtle import RawTurtle
import turtle
import inspect


window = tkinter.Tk(screenName="Turtle")

canvas = tkinter.Canvas(master=window, width=800, height=900)
canvas.grid(padx=2, pady=2, row=0, column=1, rowspan=10, columnspan=10)

tr = RawTurtle(canvas, shape="turtle")

syntaxerror_l = tkinter.Label(window, font=("Arial", 16), fg="red")
syntaxerror_l.grid(padx=4, pady=4, row=10, column=0, sticky='nsew')

def show_error(error: str):
    syntaxerror_l.config(text=error)
    syntaxerror_l.update()

def run(commands: str):
    syntaxerror_l.config(text="")
    try:
        tr.reset()
        commands_list = [_.replace('\n', "") for _ in commands.split(";")]

        final_commands = []

        for _ in commands_list[0:-1]:
            if _.startswith('repeat'):
                times = int(_.split('(')[1].replace(')', ""))
                repeat_block = []
                for _ in commands_list[commands_list.index(_) + 1:]:
                    if _.startswith('endrepeat'):
                        break
                    repeat_block.append(_.replace('\n', ""))

                for _ in range(times):
                    final_commands.extend(repeat_block)

            else:
                if not _.startswith('endrepeat'):
                    final_commands.append(_.replace('\n', ""))

        for command in final_commands:
            eval(f'tr.{command}')
    except Exception as e:
        show_error(str(e))

entry = tkinter.Text(window, width=40, height=10, padx=10, pady=10, font=("Arial", 16), undo=True)
entry.grid(padx=4, pady=4, row=0, column=0, rowspan=9, sticky='nsew')

button = tkinter.Button(window, text="Run", command=lambda: run(entry.get("1.0", "end")), bg='gray', fg="green")
button.grid(padx=4, pady=4, row=9, column=0, sticky='nsew')

def undo_text(event=None):
    entry.edit_undo()

def delete_text(event=None):
    entry.delete("1.0", "end")

window.bind('<Control-z>', undo_text)
window.bind('<Control-x>', delete_text)
window.bind('<F5>', lambda event: run(entry.get("1.0", "end")))

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

def highlight_syntax(event=None):
    text = entry.get("1.0", "end-1c")

    entry.tag_remove("keyword", "1.0", "end")
    entry.tag_remove("number", "1.0", "end")

    keywords = [name for name, obj in inspect.getmembers(turtle, inspect.isfunction)]
    keywords.append("repeat")
    keywords.append("endrepeat")
    pattern_keywords = r'\b(' + '|'.join(keywords) + r')\b'
    pattern_numbers = r'\b\d+\b'

    for match in re.finditer(pattern_keywords, text):
        entry.tag_add("keyword", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")

    for match in re.finditer(pattern_numbers, text):
        entry.tag_add("number", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")

    entry.tag_config("keyword", foreground="green")
    entry.tag_config("number", foreground="red") 

entry.bind("<KeyRelease>", highlight_syntax)

window.mainloop()
