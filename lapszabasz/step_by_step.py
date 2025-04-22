import matplotlib.patches as patches
import matplotlib.pyplot as plt
import copy
from ipywidgets import interact, widgets

import lapszabasz.sorting as ls


class StepByStepAlgorithms:
  def __init__(self, rectangles):
    self.sorting = ls.SortingByRectangles(rectangles)

    self.selection = {
      "vertical_bar": self.vertical_bar,
      "horizontal_bar": self.horizontal_bar,
      "mix": self.mix,
    }

  def step_width(self, sizes, pattern, table_number): #i, rec
    if self.i >= len(sizes):
        table_number += 1
        pattern.append([self.rec[0], self.rec[1], [0,0], table_number])

        size_1 = [self.rec[0], 1-self.rec[1], [0, self.rec[1]], table_number]
        size_2 = [1-self.rec[0], 1, [self.rec[0], 0], table_number]

    else:
        pattern.append([self.rec[0], self.rec[1], sizes[self.i][2], sizes[self.i][3]])

        size_1 = [self.rec[0], sizes[self.i][1]-self.rec[1], [sizes[self.i][2][0], sizes[self.i][2][1]+self.rec[1]], sizes[self.i][3]]
        size_2 = [sizes[self.i][0]-self.rec[0], sizes[self.i][1], [sizes[self.i][2][0]+self.rec[0], sizes[self.i][2][1]], sizes[self.i][3]]

        del sizes[self.i]

    if size_1[1] != 0:
      sizes.append(size_1)
    if size_2[0] != 0:
      sizes.append(size_2)


    rate = max(size_1[0]*size_1[1], size_2[0]*size_2[1])

    return sizes, pattern, table_number, rate

  def step_height(self, sizes, pattern, table_number):
    if self.i >= len(sizes):
        table_number += 1
        pattern.append([self.rec[0], self.rec[1], [0,0], table_number])

        size_1 = [1-self.rec[0], self.rec[1], [self.rec[0], 0], table_number]
        size_2 = [1, 1-self.rec[1], [0, self.rec[1]], table_number]

    else:
        pattern.append([self.rec[0], self.rec[1], sizes[self.i][2], sizes[self.i][3]])

        size_1 = [sizes[self.i][0]-self.rec[0], self.rec[1], [sizes[self.i][2][0]+self.rec[0], sizes[self.i][2][1]], sizes[self.i][3]]
        size_2 = [sizes[self.i][0], sizes[self.i][1]-self.rec[1], [sizes[self.i][2][0], sizes[self.i][2][1]+self.rec[1]], sizes[self.i][3]]

        del sizes[self.i]

    if size_1[0] != 0:
      sizes.append(size_1)
    if size_2[1] != 0:
      sizes.append(size_2)

    rate = max(size_1[0]*size_1[1], size_2[0]*size_2[1])

    return sizes, pattern, table_number, rate

  #Ezt majd késöbb fogalmazom...:
  # - upload=1: a legkisebb területűre darabra helyezi le a szabandó téglalapot
  # - upload=2: a legelső táblára amire még ráfér helyezi le a téglalapot
  # - upload=21: a legelső táblán amire ráfér a legkisebb területű darabra helyezi le
  # - upload=3: a legkissebb szélességű darabra helyezi el a szabandó télalapot
  # - upload=0: nincs rendezés az üres darabok között
  def vertical_bar(self, upload_site, sorting_rectangles, c):
    sizes = [[1,1,[0,0],1]]      #[szélesség, magasság, bal alsó csúcs koordinátája, tartalmazó tábla]
    table_number = 1
    pattern = []

    rectangle = self.sorting.sort_c_aspect_ratio(sorting_rectangles,1,c)
    for rec in rectangle:
      self.rec = rec

      sizes = self.sorting.step_setting(sizes, upload_site)

      i = 0
      while (i < len(sizes)) and ((sizes[i][0] < rec[0]) or (sizes[i][1] < rec[1])):
        i += 1

      self.i = i

      sizes, pattern, table_number, rate = self.step_width(sizes, pattern, table_number)

    max_remnant = sorted(sizes, key=lambda x: x[0] * x[1], reverse=1)
    max_remnant_area = [[],[],[]]
    max_remnant_area[0] = max_remnant[0][0] * max_remnant[0][1]
    max_remnant_area[1] = max_remnant[1][0] * max_remnant[1][1]
    max_remnant_area[2] = max_remnant[2][0] * max_remnant[2][1]

    return pattern, table_number, max_remnant_area


  def horizontal_bar(self, upload_site, sorting_rectangles, c):
    sizes = [[1,1,[0,0],1]]      #[szélesség, magasság, bal alsó csúcs koordinátája, tartalmazó tábla]
    table_number = 1
    pattern = []

    rectangle = self.sorting.sort_c_aspect_ratio(sorting_rectangles,1,c)
    for rec in rectangle:
      self.rec = rec

      sizes = self.sorting.step_setting(sizes, upload_site)

      i = 0
      while (i < len(sizes)) and ((sizes[i][0] < rec[0]) or (sizes[i][1] < rec[1])):
        i += 1
      self.i = i

      sizes, pattern, table_number, rate = self.step_height(sizes, pattern, table_number)

    max_remnant = sorted(sizes, key=lambda x: x[0] * x[1], reverse=1)
    max_remnant_area = [[],[],[]]
    max_remnant_area[0] = max_remnant[0][0] * max_remnant[0][1]
    max_remnant_area[1] = max_remnant[1][0] * max_remnant[1][1]
    max_remnant_area[2] = max_remnant[2][0] * max_remnant[2][1]

    return pattern, table_number, max_remnant_area

  def mix(self, upload_site, sorting_rectangles, c):
    sizes = [[1,1,[0,0],1]]      #[szélesség, magasság, bal alsó csúcs koordinátája, tartalmazó tábla]
    table_number = 1
    pattern = []

    #rectangle = getattr(self.sorting, sorting_rectangles)(1)
    rectangle = self.sorting.sort_c_aspect_ratio(sorting_rectangles, 1, c)
    for rec in rectangle:
      self.rec = rec
      sizes = self.sorting.step_setting(sizes, upload_site)

      i = 0
      while (i < len(sizes)) and ((sizes[i][0] < rec[0]) or (sizes[i][1] < rec[1])):
        i += 1
      self.i = i

      # sizes[(sizes[i][0] < rec[0]) or (sizes[i][1] < rec[1])].argmin()

      sizes_copy = copy.deepcopy(sizes)
      pattern_copy = copy.deepcopy(pattern)

      sizes_1, pattern_1, table_number_1, rate_1 = self.step_width(sizes_copy, pattern_copy, table_number)
      sizes_2, pattern_2, table_number_2, rate_2 = self.step_height(sizes, pattern, table_number)

      if rate_1 >= rate_2:
        sizes = sizes_1
        pattern = pattern_1
        table_number = table_number_1

      else:
        sizes = sizes_2
        pattern = pattern_2
        table_number = table_number_2

    max_remnant = sorted(sizes, key=lambda x: x[0] * x[1], reverse=1)
    max_remnant_area = [[],[],[]]
    max_remnant_area[0] = max_remnant[0][0] * max_remnant[0][1]
    max_remnant_area[1] = max_remnant[1][0] * max_remnant[1][1]
    max_remnant_area[2] = max_remnant[2][0] * max_remnant[2][1]

    return pattern, table_number, max_remnant_area

  #Ábrázolja step by step által létre hozott táblákat
  def plot(self, algorithm, upload_site, sorting_rectangles, aspect_ratio):
    #pattern, table_number, remnant = getattr(self, algorithm)(upload_site, sorting_rectangles, aspect_ratio)
    pattern, table_number, remnant = self.selection[algorithm](upload_site, sorting_rectangles, aspect_ratio)
    fig, ax = plt.subplots(figsize=(10, 5))
    pattern = sorted(pattern, key=lambda x: x[3])
    x = 0
    i = 1
    for rec in pattern:
      if rec[3] == i:
          rectangle = patches.Rectangle((x + rec[2][0], rec[2][1]), rec[0], rec[1], edgecolor='blue', facecolor='lightblue')
          ax.add_patch(rectangle)
      else:
          x += 1
          ax.axvline(x=x, color='black', linestyle='-', linewidth=2)
          rectangle = patches.Rectangle((x + rec[2][0], rec[2][1]), rec[0], rec[1], edgecolor='blue', facecolor='lightblue')
          ax.add_patch(rectangle)
      i = rec[3]

    ax.axvline(x=x+1, color='black', linestyle='-', linewidth=2)

    ax.text(x+1.5, 0.3, f'A felhasznált \n táblák száma: {table_number}', fontsize=12, ha='center', va='center')
    ax.text(x+1.5, 0.7, f'Legnagyobb megmarad \n darab területe: {round(remnant[0],2)}', fontsize=12, ha='center', va='center')

    ax.set_xlim(0, x + 2)
    ax.set_ylim(0, 1)

    ax.set_aspect('equal', adjustable='box')
    plt.show()

  def mix_step_plot(self, upload_site, sorting_rectangles):
    sizes = [[1,1,[0,0],1]]      #[szélesség, magasság, bal alsó csúcs koordinátája, tartalmazó tábla]
    table_number = 1
    pattern = []

    rectangle = getattr(self.sorting, sorting_rectangles)(1)

    for rec in rectangle:
      self.rec = rec
      sizes = self.sorting.step_setting(sizes, upload_site)

      i = 0
      while (i < len(sizes)) and ((sizes[i][0] < rec[0]) or (sizes[i][1] < rec[1])):
        i += 1
      self.i = i

      sizes_copy = copy.deepcopy(sizes)
      pattern_copy = copy.deepcopy(pattern)

      sizes_1, pattern_1, table_number_1, rate_1 = self.step_width(sizes_copy, pattern_copy, table_number)
      sizes_2, pattern_2, table_number_2, rate_2 = self.step_height(sizes, pattern, table_number)

      if rate_1 >= rate_2:
        sizes = sizes_1
        pattern = pattern_1
        table_number = table_number_1

      else:
        sizes = sizes_2
        pattern = pattern_2
        table_number = table_number_2

      last = pattern[len(pattern)-1]

      fig, ax = plt.subplots(figsize=(10, 5))
      pattern = sorted(pattern, key=lambda x: x[3])
      x = 0
      i = 1
      n = 0
      edgecolor='blue'
      facecolor='lightblue'

      for rec in pattern:
        if rec == last:
            edgecolor='red'
            facecolor='lightgreen'
        if rec[3] == i:
            rectangle = patches.Rectangle((x + rec[2][0], rec[2][1]), rec[0], rec[1], edgecolor=edgecolor, facecolor=facecolor)
            ax.add_patch(rectangle)
        else:
            x += 1
            ax.axvline(x=x, color='black', linestyle='-', linewidth=2)
            rectangle = patches.Rectangle((x + rec[2][0], rec[2][1]), rec[0], rec[1], edgecolor=edgecolor, facecolor=facecolor)
            ax.add_patch(rectangle)
        i = rec[3]
        edgecolor='blue'
        facecolor='lightblue'

      ax.axvline(x=x+1, color='black', linestyle='-', linewidth=2)

      ax.set_xlim(0, x + 2)
      ax.set_ylim(0, 1)

      ax.set_aspect('equal', adjustable='box')
      plt.show()

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
        ("Magasság szerint (height)","height"),
        ("Terület szerint (area)", "area"),
        ("Oldal arány szerint: (aspect_ratio)", "aspect_ratio")
      ],
      description='Szabásjegyzék rendezése:'
    )

    interact(
      self.plot,
      algorithm=upload_site_algorthm,
      upload_site=upload_site_stay,
      sorting_rectangles= upload_site_rectangel,
      aspect_ratio=(0, 1, 0.1)
    )