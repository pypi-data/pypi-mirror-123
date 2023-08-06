import tkinter as tk
import tkinter.font as tk_font
from tkinter import ttk
from tkinter import colorchooser
import threading
import re


class VariableTweaker:
    def __init__(self):
        self.create_requests = []
        self.window = None

    def add_slider(self, name, value, min_value, max_value, step):
        type_error = 'must be int or float, not'
        if not isinstance(name, str):
            raise TypeError(f'name must be str, not {name.__class__.__name__}')
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError(f'value {type_error} {value.__class__.__name__}')
        if not isinstance(min_value, int) and not isinstance(min_value, float):
            raise TypeError(f'min_value {type_error} {min_value.__class__.__name__}')
        if not isinstance(max_value, int) and not isinstance(max_value, float):
            raise TypeError(f'max_value {type_error} {max_value.__class__.__name__}')
        if not isinstance(step, int) and not isinstance(step, float):
            raise TypeError(f'step {type_error} {step.__class__.__name__}')
        if min_value >= max_value:
            raise ValueError(f'min_value is not less than max_value: {min_value} < {max_value} not holds')
        if not (min_value <= value <= max_value):
            raise ValueError(
                f'value must be between min and max values: {min_value} <= {value} <= {max_value} not holds')

        self.create_requests.append(('slider', (name, value, min_value, max_value, step)))

    def add_text(self, name, value):
        if not isinstance(name, str):
            raise TypeError(f'name must be str, not {name.__class__.__name__}')
        if not isinstance(value, str):
            raise TypeError(f'value must be str, not {value.__class__.__name__}')
        self.create_requests.append(('text', (name, value)))

    def add_dropdown(self, name, value, options):
        if not isinstance(name, str):
            raise TypeError(f'name must be str, not {name.__class__.__name__}')
        if not isinstance(options, list) and not isinstance(options, tuple):
            raise TypeError(f'options must be list or tuple, not {options.__class__.__name__}')
        self.create_requests.append(('dropdown', (name, value, options)))

    def add_boolean(self, name, value):
        if not isinstance(name, str):
            raise TypeError(f'name must be str, not {name.__class__.__name__}')
        if not isinstance(value, bool):
            raise TypeError(f'value must be bool, not {name.__class__.__name__}')
        self.create_requests.append(('boolean', (name, value)))

    def add_color(self, name, value):
        if not isinstance(name, str):
            raise TypeError(f'name must be str, not {name.__class__.__name__}')
        if isinstance(value, str):
            if not re.match('#[1234567890abcdefABCDEF]{6}', value):
                raise ValueError('value must be in #XXXXXX format')
        else:
            try:
                r, g, b = value
                if not isinstance(r, int) or not isinstance(g, int) or not isinstance(b, int):
                    raise TypeError('r, g and b must be integers')
                if not (0 <= r <= 255, 0 <= g <= 255, 0 <= b <= 255):
                    raise ValueError('r, g, and b must be in range of [0, 255]')
            except ValueError:
                raise ValueError('value must be (r, g, b) or #XXXXXX color format')
        self.create_requests.append(('color', (name, value)))

    def __init_gui_thread__(self, window_name, font_size, widget_font_size):

        if widget_font_size is None:
            widget_font_size = int(font_size * 0.75)

        for request_name, parameters in self.create_requests:
            setattr(self, parameters[0], parameters[1])

        self.window = tk.Tk()
        self.window.title(window_name)
        label_font = tk_font.Font(family='Helvetica', size=font_size, weight='bold')
        widget_font = tk_font.Font(family='Helvetica', size=widget_font_size)
        variables = []
        for request_name, parameters in self.create_requests:
            frame = tk.Frame(self.window, bd=4, relief=tk.FLAT)
            label = tk.Label(frame, text=parameters[0] + ': ', font=label_font)
            label.pack(side='left', fill='x', padx=5, pady=5)
            if request_name == 'slider':
                name, value, min_value, max_value, step = parameters
                scl = tk.Scale(frame, from_=min_value, to=max_value, resolution=step, font=widget_font,
                               orient=tk.HORIZONTAL, command=lambda scale_value: setattr(self, name, scale_value))
                scl.set(value)
                scl.pack(expand=True, fill='x')
                variables.append((request_name, name, scl))
            elif request_name == 'text':
                name, value = parameters
                entry = tk.Entry(frame, font=widget_font, justify='center')

                def callback():
                    self.window.after(10, lambda: setattr(self, name, entry.get()))

                    return True

                entry.configure(validate='key', validatecommand=callback)
                entry.insert(0, value)
                entry.pack(expand=True, fill='x')
                variables.append((request_name, name, entry))
            elif request_name == 'dropdown':
                name, value, options = parameters
                variable = tk.Variable(value=value, name=name)
                option_menu = tk.OptionMenu(frame, variable, *options,
                                            command=lambda scale_value: setattr(self, name, scale_value))
                option_menu.config(font=widget_font)
                frame.nametowidget(option_menu.menuname).config(font=widget_font)
                option_menu.pack(expand=True, fill='x')
                variables.append((request_name, name, option_menu))
            elif request_name == 'boolean':
                name, value = parameters
                var = tk.BooleanVar(value=value)
                checkbutton = tk.Checkbutton(frame, text=('True' if value else 'False'),
                                             variable=var, font=widget_font, indicatoron=False)

                def callback():
                    setattr(self, name, var.get())
                    checkbutton.config(text=('True' if var.get() else 'False'))

                checkbutton.configure(command=callback)
                checkbutton.pack(expand=True, fill='both')
                variables.append((request_name, name, checkbutton))
            elif request_name == 'color':
                name, value = parameters
                color = Color(value)
                def color_callback():
                    color.set(colorchooser.askcolor(color=color.color_code, title='Choose Color')[0])
                    button.config(bg=color.color_code, activebackground=color.__highlight_color__())

                button = tk.Button(frame, bg=color.color_code, activebackground=color.__highlight_color__(),
                                   command=color_callback)
                button.pack(expand=True, fill='both')

            frame.pack(expand=True, fill='x', padx=3, pady=3)
            ttk.Separator(self.window, orient='horizontal').pack(fill='x')

        self.window.mainloop()

    def init_gui(self, window_name='Variable Tweaker', font_size=16, widget_font_size=None):
        threading.Thread(target=self.__init_gui_thread__, daemon=True,
                         args=(window_name, font_size, widget_font_size)).start()


class Color:
    def __init__(self, value):
        self.r, self.g, self.b, self.color_code = 0, 0, 0, '#000000'
        self.set(value)

    def set(self, value=(0, 0, 0)):
        if isinstance(value, str):
            value = value.replace('#', '')
            a = int(value, 16)
            self.b = a & 0xff
            self.g = (a >> 8) & 0xff
            self.r = (a >> 16) & 0xff
            self.color_code = '#' + value
        elif isinstance(value, tuple):
            self.r, self.g, self.b = value
            self.color_code = '#{:06x}'.format((self.r << 16) | (self.g << 8) | self.b)

    def __highlight_color__(self):
        return '#{:06x}'.format((min(self.r + 20, 255) << 16) | ((min(self.g + 20, 255) << 8) | min(self.b + 20, 255)))
