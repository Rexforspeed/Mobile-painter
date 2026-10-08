import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.core.window import Window

Window.size = (400, 700)

class DrawingCanvas(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_x = 200
        self.current_y = 400
        self.brush_color = (1, 0, 0, 1)
        self.brush_width = 3
        with self.canvas:
            Color(1, 1, 1, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def move_brush(self, dx, dy):
        old_x, old_y = self.current_x, self.current_y
        self.current_x += dx
        self.current_y += dy
        self.current_x = max(self.x, min(self.current_x, self.right))
        self.current_y = max(self.y, min(self.current_y, self.top))
        with self.canvas:
            Color(*self.brush_color)
            Line(points=[old_x, old_y, self.current_x, self.current_y], width=self.brush_width)

    def clear_canvas(self):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.current_x = 200
        self.current_y = 400

class MobilePainterApp(App):
    def build(self):
        self.title = "Mobile Painter"
        self.main_layout = BoxLayout(orientation='vertical')
        self.painter = DrawingCanvas()
        self.main_layout.add_widget(self.painter)
        self.control_panel = BoxLayout(orientation='vertical', size_hint_y=0.45, padding=5, spacing=5)
        self.status_label = Label(text="Brush Width: 3 | Mode: Ink", size_hint_y=0.2, color=(0,0,0,1), bold=True)
        self.control_panel.add_widget(self.status_label)
        btn_grid = GridLayout(cols=3, spacing=5)
        btn_clear = Button(text="Clear")
        btn_clear.bind(on_press=lambda x: self.painter.clear_canvas())
        btn_up = Button(text="▲ Up")
        btn_up.bind(on_press=lambda x: self.painter.move_brush(0, 30))
        btn_width = Button(text="Size +")
        btn_width.bind(on_press=self.increase_size)
        btn_left = Button(text="◀ Left")
        btn_left.bind(on_press=lambda x: self.painter.move_brush(-30, 0))
        self.btn_eraser = Button(text="Eraser")
        self.btn_eraser.bind(on_press=self.toggle_eraser)
        btn_right = Button(text="Right ▶")
        btn_right.bind(on_press=lambda x: self.painter.move_brush(30, 0))
        btn_hide = Button(text="Hide HUD")
        btn_hide.bind(on_press=self.hide_controls)
        btn_down = Button(text="▼ Down")
        btn_down.bind(on_press=lambda x: self.painter.move_brush(0, -30))
        btn_size_down = Button(text="Size -")
        btn_size_down.bind(on_press=self.decrease_size)
        btn_grid.add_widget(btn_clear); btn_grid.add_widget(btn_up); btn_grid.add_widget(btn_width)
        btn_grid.add_widget(btn_left); btn_grid.add_widget(self.btn_eraser); btn_grid.add_widget(btn_right)
        btn_grid.add_widget(btn_hide); btn_grid.add_widget(btn_down); btn_grid.add_widget(btn_size_down)
        self.control_panel.add_widget(btn_grid)
        color_row = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=2)
        colors = {"Red": (1, 0, 0, 1), "Blue": (0, 0, 1, 1), "Green": (0, 1, 0, 1), "Orange": (1, 0.5, 0, 1), "Purple": (0.5, 0, 0.5, 1), "Black": (0, 0, 0, 1)}
        for c_name, c_rgba in colors.items():
            c_btn = Button(background_color=c_rgba, background_normal='')
            c_btn.bind(on_press=lambda x, rgba=c_rgba: self.select_color(rgba))
            color_row.add_widget(c_btn)
        self.control_panel.add_widget(color_row)
        self.main_layout.add_widget(self.control_panel)
        self.reveal_btn = Button(text="Show Controls Menu", size_hint_y=0.1, pos_hint={'top': 1}, background_color=(0.2, 0.6, 1, 0.8))
        self.reveal_btn.bind(on_press=self.show_controls)
        return self.main_layout

    def select_color(self, rgba):
        self.painter.brush_color = rgba
        self.status_label.text = f"Brush Width: {self.painter.brush_width} | Mode: Ink"

    def toggle_eraser(self, instance):
        if self.painter.brush_color != (1, 1, 1, 1):
            self.painter.brush_color = (1, 1, 1, 1)
            self.status_label.text = f"Brush Width: {self.painter.brush_width} | Mode: Eraser 🧽"
        else:
            self.painter.brush_color = (1, 0, 0, 1)
            self.status_label.text = f"Brush Width: {self.painter.brush_width} | Mode: Ink"

    def increase_size(self, instance):
        if self.painter.brush_width < 20:
            self.painter.brush_width += 1
            self.update_status_text()

    def decrease_size(self, instance):
        if self.painter.brush_width > 1:
            self.painter.brush_width -= 1
            self.update_status_text()

    def update_status_text(self):
        mode = "Eraser 🧽" if self.painter.brush_color == (1, 1, 1, 1) else "Ink"
        self.status_label.text = f"Brush Width: {self.painter.brush_width} | Mode: {mode}"

    def hide_controls(self, instance):
        self.main_layout.remove_widget(self.control_panel)
        self.main_layout.add_widget(self.reveal_btn)

    def show_controls(self, instance):
        self.main_layout.remove_widget(self.reveal_btn)
        self.main_layout.add_widget(self.control_panel)

if __name__ == '__main__':
    MobilePainterApp().run()
