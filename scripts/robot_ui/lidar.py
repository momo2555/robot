from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import pyglet as pyg


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./lidar_assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

pyg.font.add_file("./lidar_assets/Montserrat-ExtraBold.ttf")


window = Tk()

window.geometry("800x480")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 480,
    width = 800,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    400,
    300,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    379.0,
    407.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    606.0,
    407.0,
    image=image_image_3
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Côté violet sélectioné."),
    relief="flat"
)
button_1.place(
    x=382.15985107421875,
    y=407.0758056640625,
    width=78.22955322265625,
    height=33.310638427734375
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Côté jaune sélectioné."),
    relief="flat"
)
button_2.place(
    x=298.88323974609375,
    y=407.0758056640625,
    width=78.22955322265625,
    height=33.310638427734375
)

canvas.create_text(
    312,
    372,
    anchor="nw",
    text="Côté du plateau",
    fill="#000000",
    font=("Montserrat ExtraBold", 16 * -1)
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    121.0,
    248.0,
    image=image_image_4
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Calibration du LIDAR lançée."),
    relief="flat"
)
button_3.place(
    x=527.0107421875,
    y=370.2322998046875,
    width=158.47796630859375,
    height=73.68719482421875
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    121.0,
    119.0,
    image=image_image_5
)

canvas.create_text(
    98,
    234,
    anchor="nw",
    text="100",
    fill="#FFFFFF",
    font=("Montserrat ExtraBold", 20 * -1)
)

canvas.create_text(
    145,
    234,
    anchor="nw",
    text="S",
    fill="#FFFFFF",
    font=("Montserrat ExtraBold", 20 * -1)
)

canvas.create_text(
    95,
    194,
    anchor="nw",
    text="TIMER",
    fill="#FFFFFF",
    font=("Montserrat ExtraBold", 20 * -1)
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    485.0,
    182.0,
    image=image_image_6
)

canvas.create_text(
    145.0,
    104,
    anchor="nw",
    text="0",
    fill="#FFFFFF",
    font=("Montserrat ExtraBold", 20 * -1)
)

canvas.create_text(
    95.0,
    62.0,
    anchor="nw",
    text="SCORE",
    fill="#FFFFFF",
    font=("Montserrat ExtraBold", 20 * -1)
)
window.resizable(False, False)
window.mainloop()
