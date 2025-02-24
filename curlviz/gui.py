try:
    import tkinter as tk
except ImportError:
    import sys
    print("[ERROR] Tk is not available in your environment.", file=sys.stderr)
    sys.exit(1)

import skia
from PIL import Image, ImageTk

import curlviz


def main():
    config = curlviz.Config()
    config.ppm = 100
    drawer = curlviz.drawer.Drawer(config)

    window = tk.Tk()
    window.title("CURLVIZ")
    window.minsize(*drawer.canvas_size())

    sheet = curlviz.Sheet()

    surface = skia.Surface(*drawer.canvas_size())
    with surface as canvas:
        drawer.draw(canvas, sheet)
    image = ImageTk.PhotoImage(Image.fromarray(surface.toarray()))

    canvas = tk.Canvas(window, bg="black", width=image.width(), heigh=image.height())
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, image=image, anchor=tk.NW)

    window.mainloop()


if __name__ == "__main__":
    main()