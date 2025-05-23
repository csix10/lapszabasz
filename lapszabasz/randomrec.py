import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import svgwrite
from IPython.display import SVG, display

class RandomRectangles:
    #Letrehoz random teglalapok egy np listajat ugy hogy:
    # - size_number darab kulonbozo meretu teglalap legyen
    # - szelessegi es magassagi merete min_size es max_size kozotti racionalis szam
    # - maximum max_count darab azonos meretu teglalap lehet
    def generate_random_size(size_number: int, min_size, max_size, max_count):
        sizes = np.random.uniform(min_size, max_size, size=(size_number, 2))
        counts = np.random.randint(0, max_count + 1, size=size_number)

        expanded_sizes = np.repeat(sizes, counts, axis=0)
        return expanded_sizes

    #Abrazolja teglalapok egy halmazat egyszeruen
    def plot_rectangles(rectangles):
        fig, ax = plt.subplots(figsize=(10, 5))

        i=0
        for rect in list(rectangles):
            width, height = rect
            rectangle = patches.Rectangle((i, 0), width, height, edgecolor='blue', facecolor='lightblue')
            ax.add_patch(rectangle)
            i = i+width+0.1

        ax.set_xlim(0, i + 1)
        ax.set_ylim(0, 1)

        ax.set_aspect('equal', adjustable='box')
        plt.show()

    #Abrazolja teglalapok egy halmazat svg-ben
    def plot_rectangles_svg(rectangles):
        filename = "teglalapok.svg"
        u=500
        dwg = svgwrite.Drawing(filename, size=(20*u, u))

        i=0
        for rect in list(rectangles):
            width, height = rect
            width = width*u
            height = height*u
            dwg.add(dwg.rect(insert=(i, 0), size=(width, height), fill="grey",  stroke="black"))

            if rect[0]>0.1:
              text_position_1 = (i+width/2, 15)

              dwg.add(dwg.text(round(width/u,2), insert=text_position_1, text_anchor="middle"))

            if rect[1]>0.1:
              text_position_2 = (i + 15, height/2)

              dwg.add(dwg.text(round(height/u,2), insert=text_position_2, text_anchor="middle", transform=f"rotate(270, {text_position_2[0]}, {text_position_2[1]})"))

            i = i+width+0.1*u

        dwg.save()
        display(SVG(filename))