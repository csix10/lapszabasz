import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import svgwrite
from IPython.display import SVG, display
from ipywidgets import interact, widgets

import lapszabasz.sorting as ls


class FitAlgorithms:
    def __init__(self, rectangles):
        self.sorting = ls.SortingByRectangles(rectangles)

    # Sávokba rendezi téglalapok egy halmazát Next Fit Decreasing szerint.
    # (Addig rakja az elemeket a sorok következő sávba, amig lehet.
    # Ha egy elem már nem fér az adott sávba, akkor új sávot nyit)
    def NFD(self):
        sort_rec = self.sorting.latitude(1)
        lanes = []
        lane = []
        szum = 0
        remnant = []

        for rec in sort_rec:
            szum = szum + rec[1]
            if szum < 1:
                lane.append(rec)
            else:
                remnant.append((1 - szum + rec[1]) * lane[0][0])
                szum = rec[1]
                lanes.append(lane)
                lane = [rec]
        lanes.append(lane)
        return lanes, remnant

    # Táblákba rendezi sávok egy halmazát Next Fit Decreasing szerint.
    def NFD_lanes(self):
        lanes, remnant = self.NFD()
        tables = []
        table = []
        szum = 0

        for lane in lanes:
            szum = szum + lane[0][0]
            if szum < 1:
                table.append(lane)
            else:
                remnant.append(1 - szum + lane[0][0])
                szum = lane[0][0]
                tables.append(table)
                table = [lane]
        tables.append(table)
        remnant.append(1 - szum)

        max_remnant = sorted(remnant, reverse=True)[:3]

        return tables, len(tables), max_remnant

    # Sávokba rendezi téglalapok egy halmazát First Fit Decreasing szerint.
    # (Következőt mindig az első olyan sávba helyezi, amelybe belefér.)
    def FFD(self):
        sort_rec = self.sorting.latitude(1)
        lanes = []
        sizes = []

        for rec in sort_rec:
            i = 0
            while (i < len(sizes)) and ((sizes[i][0] < rec[0]) or (sizes[i][1] + rec[1] > 1)):
                i += 1
            if i >= len(sizes):
                lanes.append([rec])
                sizes.append([rec[0], rec[1]])
            else:
                lanes[i].append(rec)
                sizes[i][1] = sizes[i][1] + rec[1]

        sizes = np.array(sizes)
        remnant = sizes[:, 0] * (1 - sizes[:, 1])

        return lanes, remnant

    # Táblákba rendezi sávok egy halmazát First Fit Decreasing szerint.
    def FFD_lanes(self):
        lanes, remnant = self.FFD()
        sizes = []
        tables = []

        for lane in lanes:
            i = 0
            while (i < len(sizes)) and (sizes[i] + lane[0][0] > 1):
                i += 1
            if i >= len(sizes):
                tables.append([lane])
                sizes.append(lane[0][0])
            else:
                tables[i].append(lane)
                sizes[i] += lane[0][0]

        sizes = np.array(sizes)
        remnant = np.concatenate((remnant, 1 - sizes))
        max_remnant = sorted(remnant, reverse=True)[:3]

        return tables, len(tables), max_remnant

    def BFD(self):
        sort_rec = self.sorting.latitude(1)
        lanes = []
        sizes = []

        for rec in sort_rec:
            i = 0

            sorted_indices = sorted(range(len(sizes)), key=lambda i: sizes[i][1], reverse=True)
            sizes = [sizes[i] for i in sorted_indices]
            lanes = [lanes[i] for i in sorted_indices]

            while (i < len(sizes)) and ((sizes[i][0] < rec[0]) or (sizes[i][1] + rec[1] > 1)):
                i += 1
            if i >= len(sizes):
                lanes.append([rec])
                sizes.append([rec[0], rec[1]])
            else:
                lanes[i].append(rec)
                sizes[i][1] += rec[1]

        sizes = np.array(sizes)
        remnant = sizes[:, 0] * (1 - sizes[:, 1])

        return lanes, remnant

    def BFD_lanes(self):
        lanes, remnant = self.BFD()
        lanes = sorted(lanes, key=lambda x: x[0][0], reverse=True)
        sizes = []
        tables = []

        for lane in lanes:
            i = 0

            sorted_indices = sorted(range(len(sizes)), key=lambda i: sizes[i], reverse=True)
            sizes = [sizes[i] for i in sorted_indices]
            tables = [tables[i] for i in sorted_indices]

            while (i < len(sizes)) and (sizes[i] + lane[0][0] > 1):
                i += 1
            if i >= len(sizes):
                tables.append([lane])
                sizes.append(lane[0][0])
            else:
                tables[i].append(lane)
                sizes[i] += lane[0][0]

        sizes = np.array(sizes)
        remnant = np.concatenate((remnant, 1 - sizes))
        max_remnant = sorted(remnant, reverse=True)[:3]

        return tables, len(tables), max_remnant

    # Ábrázolja a Fit algoritmusok tábláit
    def plot(self, algorithm):
        algorithm = algorithm + "_lanes"
        tables, tables_number, remnant = getattr(self, algorithm)()

        fig, ax = plt.subplots(figsize=(10, 5))
        x = 0
        y = 0
        i = 0
        for table in tables:
            x = i
            for lane in table:
                for rec in lane:
                    width, height = rec
                    rectangle = patches.Rectangle((x, y), width, height, edgecolor='blue', facecolor='lightblue')
                    ax.add_patch(rectangle)
                    y = y + rec[1]
                y = 0
                x = x + lane[0][0]
            i = i + 1
            ax.axvline(x=i, color='black', linestyle='-', linewidth=2)
        ax.axvline(x=i, color='black', linestyle='-', linewidth=2)

        ax.text(x + 0.5, 0.3, f'A felhasznált \n táblák száma: {tables_number}', fontsize=12, ha='center', va='center')
        ax.text(x + 0.5, 0.7, f'Legnagyobb megmarad \n darab területe: {round(remnant[0], 2)}', fontsize=12,
                ha='center', va='center')

        ax.set_xlim(0, x + 1)
        ax.set_ylim(0, 1)

        ax.set_aspect('equal', adjustable='box')
        plt.show()

    # Ábrázolja a Fit algoritmusok tábláit
    def plot_svg(self, algorithm):
        algorithm = algorithm + "_lanes"
        tables, tables_number, remnant = getattr(self, algorithm)()
        u = 500

        x = 0
        y = 0
        i = 0
        for table in tables:
            x = 0
            svg_filename = f"fitt_terv_{i + 1}.svg"
            dwg = svgwrite.Drawing(svg_filename, size=(u, u))

            # Sraffozás mintázat létrehozása
            pattern = dwg.defs.add(dwg.pattern(id="sraffozas", size=(10, 10), patternUnits="userSpaceOnUse"))
            pattern.add(dwg.line(start=(0, 0), end=(10, 10), stroke="black", stroke_width=0.5))

            dwg.add(dwg.rect(insert=(0, 0), size=(u, u), fill="url(#sraffozas)", stroke="black", stroke_width=3))

            for lane in table:
                for rec in lane:
                    width, height = rec
                    width = width * u
                    height = height * u

                    dwg.add(dwg.rect(insert=(x, y), size=(width, height), fill="grey", stroke="black"))
                    if rec[0] > 0.1 and rec[1] > 0.1:
                        text_position_1 = (x + width / 2, y + 15)
                        text_position_2 = (x + 15, y + height / 2)

                        dwg.add(dwg.text(round(rec[0], 2), insert=text_position_1, text_anchor="middle"))
                        dwg.add(dwg.text(round(rec[1], 2), insert=text_position_2, text_anchor="middle",
                                         transform=f"rotate(270, {text_position_2[0]}, {text_position_2[1]})"))
                    y = y + height
                y = 0
                x = x + lane[0][0] * u
            i = i + 1

            # SVG mentése
            dwg.save()

            # SVG megjelenítése Colabban
            display(SVG(svg_filename))

    def interactive_figure(self):

        upload_site_dropdown = widgets.Dropdown(
            options=[
                ("NFDL: Next Fit Decreasing Lane", "NFD"),
                ("FFDL: First Fit Decreasing Lane", "FFD"),
                ("BFDL: Best Fit Decreasing Lane", "BFD"),
            ],
            description='Algoritmus: '
        )

        interact(
            self.plot,
            algorithm=upload_site_dropdown,
        )
