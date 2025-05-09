import matplotlib.patches as patches
import matplotlib.pyplot as plt
import copy
import heapq
from ipywidgets import interact, widgets
from IPython.display import SVG, display
import svgwrite

import lapszabasz.sorting as ls


class StepByStepAlgorithms:
    def __init__(self, rectangles):
        self.sorting = ls.SortingByRectangles(rectangles)

        self.selection = {
            "vertical_bar": self.vertical_bar,
            "horizontal_bar": self.horizontal_bar,
            "mix": self.mix,
        }

    # Egy lépésben elvégzi a vágást szélesség szerint
    def step_width(self, sizes, pattern, table_number, i, rec):
        if i >= len(sizes):
            table_number += 1
            pattern.append([rec[0], rec[1], [0, 0], table_number])

            size_1 = [rec[0], 1 - rec[1], [0, rec[1]], table_number]
            size_2 = [1 - rec[0], 1, [rec[0], 0], table_number]

        else:
            pattern.append([rec[0], rec[1], sizes[i][2], sizes[i][3]])

            size_1 = [rec[0], sizes[i][1] - rec[1], [sizes[i][2][0], sizes[i][2][1] + rec[1]], sizes[i][3]]
            size_2 = [sizes[i][0] - rec[0], sizes[i][1], [sizes[i][2][0] + rec[0], sizes[i][2][1]], sizes[i][3]]

            del sizes[i]

        if size_1[1] != 0:
            sizes.append(size_1)
        if size_2[0] != 0:
            sizes.append(size_2)

        rate = max(size_1[0] * size_1[1], size_2[0] * size_2[1])

        return sizes, pattern, table_number, rate

    # Egy lépésben elvégzi a vágást magasság szerint
    def step_height(self, sizes, pattern, table_number, i, rec):
        if i >= len(sizes):
            table_number += 1
            pattern.append([rec[0], rec[1], [0, 0], table_number])

            size_1 = [1 - rec[0], rec[1], [rec[0], 0], table_number]
            size_2 = [1, 1 - rec[1], [0, rec[1]], table_number]

        else:
            pattern.append([rec[0], rec[1], sizes[i][2], sizes[i][3]])

            size_1 = [sizes[i][0] - rec[0], rec[1], [sizes[i][2][0] + rec[0], sizes[i][2][1]], sizes[i][3]]
            size_2 = [sizes[i][0], sizes[i][1] - rec[1], [sizes[i][2][0], sizes[i][2][1] + rec[1]], sizes[i][3]]

            del sizes[i]

        if size_1[0] != 0:
            sizes.append(size_1)
        if size_2[1] != 0:
            sizes.append(size_2)

        rate = max(size_1[0] * size_1[1], size_2[0] * size_2[1])

        return sizes, pattern, table_number, rate

    # Függőleges sávos szabástervet generáló step by step
    # - upload=1: a legkisebb területűre darabra helyezi le a szabandó téglalapot
    # - upload=2: a legelső táblára amire még ráfér helyezi le a téglalapot
    # - upload=21: a legelső táblán amire ráfér a legkisebb területű darabra helyezi le
    # - upload=3: a legkissebb szélességű darabra helyezi el a szabandó télalapot
    # - upload=0: nincs rendezés az üres darabok között
    def vertical_bar(self, upload_site, sorting_rectangles, c):
        sizes = [[1, 1, [0, 0], 1]]  # [szélesség, magasság, bal alsó csúcs koordinátája, tartalmazó tábla]
        table_number = 1
        pattern = []

        rectangle = self.sorting.sort_c_aspect_ratio(sorting_rectangles, 1, c)
        for rec in rectangle:
            sizes = self.sorting.step_setting(sizes, upload_site)

            i = 0
            while (i < len(sizes)) and ((sizes[i][0] < rec[0]) or (sizes[i][1] < rec[1])):
                i += 1

            sizes, pattern, table_number, rate = self.step_width(sizes, pattern, table_number, i, rec)

        areas = [s[0] * s[1] for s in sizes]
        top3 = heapq.nlargest(3, areas)
        max_remnant_area = top3 + [0] * (3 - len(top3))

        return pattern, table_number, max_remnant_area

    # Vízszintes sávos szabástervet generáló step by step
    # Beállítások ugyan az mint elöbb
    def horizontal_bar(self, upload_site, sorting_rectangles, c):
        sizes = [[1, 1, [0, 0], 1]]  # [szélesség, magasság, bal alsó csúcs koordinátája, tartalmazó tábla]
        table_number = 1
        pattern = []

        rectangle = self.sorting.sort_c_aspect_ratio(sorting_rectangles, 1, c)
        for rec in rectangle:
            sizes = self.sorting.step_setting(sizes, upload_site)

            i = 0
            while (i < len(sizes)) and ((sizes[i][0] < rec[0]) or (sizes[i][1] < rec[1])):
                i += 1

            sizes, pattern, table_number, rate = self.step_height(sizes, pattern, table_number, i, rec)

        areas = [s[0] * s[1] for s in sizes]
        top3 = heapq.nlargest(3, areas)
        max_remnant_area = top3 + [0] * (3 - len(top3))

        return pattern, table_number, max_remnant_area

    # Vegyes szabástervet generáló step by step
    def mix(self, upload_site, sorting_rectangles, c):
        sizes = [[1, 1, [0, 0], 1]]  # [szélesség, magasság, bal alsó csúcs koordinátája, tartalmazó tábla]
        table_number = 1
        pattern = []

        rectangle = self.sorting.sort_c_aspect_ratio(sorting_rectangles, 1, c)
        for rec in rectangle:
            sizes = self.sorting.step_setting(sizes, upload_site)

            i = 0
            sizes_len = len(sizes)
            while i < sizes_len and (sizes[i][0] < rec[0] or sizes[i][1] < rec[1]):
                i += 1

            sizes_copy = [s.copy() for s in sizes]
            pattern_copy = [p.copy() for p in pattern]

            sizes_1, pattern_1, table_number_1, rate_1 = self.step_width(sizes_copy, pattern_copy, table_number, i, rec)
            sizes_2, pattern_2, table_number_2, rate_2 = self.step_height(sizes, pattern, table_number, i, rec)

            if rate_1 >= rate_2:
                sizes = sizes_1
                pattern = pattern_1
                table_number = table_number_1
            else:
                sizes = sizes_2
                pattern = pattern_2
                table_number = table_number_2

        areas = [s[0] * s[1] for s in sizes]
        top3 = heapq.nlargest(3, areas)
        max_remnant_area = top3 + [0] * (3 - len(top3))

        return pattern, table_number, max_remnant_area

    # Vázlatosan ábrázolja step by step által létre hozott szabástervet
    def plot(self, algorithm, upload_site, sorting_rectangles, aspect_ratio):
        pattern, table_number, remnant = self.selection[algorithm](upload_site, sorting_rectangles, aspect_ratio)
        fig, ax = plt.subplots(figsize=(10, 5))
        pattern = sorted(pattern, key=lambda x: x[3])
        x = 0
        i = 1
        for rec in pattern:
            if rec[3] == i:
                rectangle = patches.Rectangle((x + rec[2][0], rec[2][1]), rec[0], rec[1], edgecolor='blue',
                                              facecolor='lightblue')
                ax.add_patch(rectangle)
            else:
                x += 1
                ax.axvline(x=x, color='black', linestyle='-', linewidth=2)
                rectangle = patches.Rectangle((x + rec[2][0], rec[2][1]), rec[0], rec[1], edgecolor='blue',
                                              facecolor='lightblue')
                ax.add_patch(rectangle)
            i = rec[3]

        ax.axvline(x=x + 1, color='black', linestyle='-', linewidth=2)

        ax.text(x + 1.5, 0.3, f'A felhasznált \n táblák száma: {table_number}', fontsize=12, ha='center', va='center')
        ax.text(x + 1.5, 0.7, f'Legnagyobb megmarad \n darab területe: {round(remnant[0], 2)}', fontsize=12,
                ha='center', va='center')

        ax.set_xlim(0, x + 2)
        ax.set_ylim(0, 1)

        ax.set_aspect('equal', adjustable='box')
        plt.show()

    def plot_svg(self, algorithm, upload_site, sorting_rectangles, aspect_ratio):
        pattern, table_number, remnant = self.selection[algorithm](upload_site, sorting_rectangles, aspect_ratio)

        u = 500
        pattern = sorted(pattern, key=lambda x: x[3])

        max_table_number = max(rec[3] for rec in pattern)

        for table_idx in range(1, max_table_number + 1):
            svg_filename = f"tabla_{table_idx}.svg"
            dwg = svgwrite.Drawing(svg_filename, size=(u, u))

            # Sraffozás mintázat
            pattern_fill = dwg.defs.add(
                dwg.pattern(id="sraffozas", size=(10, 10), patternUnits="userSpaceOnUse")
            )
            pattern_fill.add(dwg.line(start=(0, 0), end=(10, 10), stroke="black", stroke_width=0.5))

            # Háttér (sraffozott)
            dwg.add(dwg.rect(insert=(0, 0), size=(u, u),
                             fill="url(#sraffozas)", stroke="black", stroke_width=3))

            # Téglalapok berajzolása
            for rec in pattern:
                if rec[3] == table_idx:
                    width = rec[0] * u
                    height = rec[1] * u
                    x_pos = rec[2][0] * u
                    y_pos = rec[2][1] * u

                    dwg.add(dwg.rect(insert=(x_pos, y_pos),
                                     size=(width, height),
                                     fill="grey", stroke="black", stroke_width=1))

                    if rec[0] > 0.1 and rec[1] > 0.1:
                        text_position_1 = (x_pos + width / 2, y_pos + 15)
                        text_position_2 = (x_pos + 15, y_pos + height / 2)

                        dwg.add(dwg.text(round(rec[0], 2),
                                         insert=text_position_1,
                                         text_anchor="middle",
                                         font_size="12px"))

                        dwg.add(dwg.text(round(rec[1], 2),
                                         insert=text_position_2,
                                         text_anchor="middle",
                                         font_size="12px",
                                         transform=f"rotate(270, {text_position_2[0]}, {text_position_2[1]})"))

            dwg.save()
            display(SVG(svg_filename))

    # Vázlatosan ábrázolja vegyes step by step algortimus lépésenként
    def mix_step_plot(self, upload_site, sorting_rectangles):
        sizes = [[1, 1, [0, 0], 1]]  # [szélesség, magasság, bal alsó csúcs koordinátája, tartalmazó tábla]
        table_number = 1
        pattern = []

        rectangle = getattr(self.sorting, sorting_rectangles)(1)

        for rec in rectangle:
            sizes = self.sorting.step_setting(sizes, upload_site)

            i = 0
            while (i < len(sizes)) and ((sizes[i][0] < rec[0]) or (sizes[i][1] < rec[1])):
                i += 1

            sizes_copy = copy.deepcopy(sizes)
            pattern_copy = copy.deepcopy(pattern)

            sizes_1, pattern_1, table_number_1, rate_1 = self.step_width(sizes_copy, pattern_copy, table_number, i, rec)
            sizes_2, pattern_2, table_number_2, rate_2 = self.step_height(sizes, pattern, table_number, i, rec)

            if rate_1 >= rate_2:
                sizes = sizes_1
                pattern = pattern_1
                table_number = table_number_1

            else:
                sizes = sizes_2
                pattern = pattern_2
                table_number = table_number_2

            last = pattern[len(pattern) - 1]

            fig, ax = plt.subplots(figsize=(10, 5))
            pattern = sorted(pattern, key=lambda x: x[3])
            x = 0
            i = 1
            n = 0
            edgecolor = 'blue'
            facecolor = 'lightblue'

            for rec in pattern:
                if rec == last:
                    edgecolor = 'red'
                    facecolor = 'lightgreen'
                if rec[3] == i:
                    rectangle = patches.Rectangle((x + rec[2][0], rec[2][1]), rec[0], rec[1], edgecolor=edgecolor,
                                                  facecolor=facecolor)
                    ax.add_patch(rectangle)
                else:
                    x += 1
                    ax.axvline(x=x, color='black', linestyle='-', linewidth=2)
                    rectangle = patches.Rectangle((x + rec[2][0], rec[2][1]), rec[0], rec[1], edgecolor=edgecolor,
                                                  facecolor=facecolor)
                    ax.add_patch(rectangle)
                i = rec[3]
                edgecolor = 'blue'
                facecolor = 'lightblue'

            ax.axvline(x=x + 1, color='black', linestyle='-', linewidth=2)

            ax.set_xlim(0, x + 2)
            ax.set_ylim(0, 1)

            ax.set_aspect('equal', adjustable='box')
            plt.show()

    # Step by step algoritmushoz készít interaktav ábrát amin az összed beállítás megadható
    def interactive_figure(self):
        upload_site_algorthm = widgets.Dropdown(
            options=[
                ("Függőleges sávos (vertical_bar)", "vertical_bar"),
                ("Vízszintes sávos (horizontal_bar)", "horizontal_bar"),
                ("Kevert (mix)", "mix")
            ],
            description='Szabásterv típusa:'
        )

        upload_site_stay = widgets.Dropdown(
            options=[
                ("Legkisebb területű darabra helyezi le (1)", 1),
                ("Legelső táblára helyezi le (2)", 2),
                ("Legelső táblán a legkisebb területűre helyezi le (21)", 21),
                ("Legkisebb szélességű darabra (3)", 3),
                ("Nincs rendezés (0)", 0)
            ],
            description='Maradék beállítása:'
        )
        upload_site_rectangel = widgets.Dropdown(
            options=[
                ("Széllesség szerint (latitude)", "latitude"),
                ("Magasság szerint (height)", "height"),
                ("Terület szerint (area)", "area"),
                ("Oldal arány szerint: (aspect_ratio)", "aspect_ratio")
            ],
            description='Szabásjegyzék rendezése:'
        )
        aspect_ratio = widgets.FloatSlider(
            value=0.5,
            min=0,
            max=1,
            step=0.1,
            description='Oldalarány súlya (c):'
        )

        interact(
            self.plot,
            algorithm=upload_site_algorthm,
            upload_site=upload_site_stay,
            sorting_rectangles=upload_site_rectangel,
            aspect_ratio=aspect_ratio
        )
