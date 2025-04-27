import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
from collections import Counter

import lapszabasz.randomrec as lr
import lapszabasz.fit as lf
import lapszabasz.step_by_step as lss


def step_by_step_selection(step_by_step):
  selection = {
      "vertical_bar": step_by_step.vertical_bar,
      "horizontal_bar": step_by_step.horizontal_bar,
      "mix": step_by_step.mix
  }
  return selection

def fit_selection(fit):
  selection = {
      "NFD": fit.NFD_lanes,
      "FFD": fit.FFD_lanes,
      "BFD": fit.BFD_lanes
  }
  return selection

class Statistics:
  def __init__(self, sample_number):
    self.sample_number = sample_number
    self.setting_sorting_rec = ("latitude", "height", "area", "aspect_ratio")
    self.setting_sorting_rem = (1, 2, 21, 3)
    self.setting_fit = ("NFD", "FFD", "BFD")

  #Kiértékeli a statisztikai eredményeket és előkészíti a táblázat ábrázolását
  def evaluative_descriptive(self, stat, names):
    vocabulary = {
      "latitude_1": "SbS: Szab. jegy.: Szélesség, Maradék: Terület",
      "latitude_2": "SbS: Szab. jegy.: Szélesség, Maradék: Tábla",
      "latitude_21": "SbS: Szab. jegy.: Szélesség, Maradék: Tábla és terület",
      "latitude_3": "SbS: Szab. jegy.: Szélesség, Maradék: Szélesség",
      "height_1": "SbS: Szab. jegy.: Magasság, Maradék: Terület",
      "height_2": "SbS: Szab. jegy.: Magasság, Maradék: Tábla",
      "height_21": "SbS: Szab. jegy.: Magasság, Maradék: Tábla és terület",
      "height_3": "SbS: Szab. jegy.: Magasság, Maradék: Szélesség",
      "area_1": "SbS: Szab. jegy.: Terület, Maradék: Terület",
      "area_2": "SbS: Szab. jegy.: Terület, Maradék: Tábla",
      "area_21": "SbS: Szab. jegy.: Terület, Maradék: Tábla és terület",
      "area_3": "SbS: Szab. jegy.: Terület, Maradék: Szélesség",
      "aspect_ratio_1": "SbS: Szab. jegy.: Old. arány, Maradék: Terület",
      "aspect_ratio_2": "SbS: Szab. jegy.: Old. arány, Maradék: Tábla",
      "aspect_ratio_21": "SbS: Szab. jegy.: Old. arány, Maradék: Tábla és terület",
      "aspect_ratio_3": "SbS: Szab. jegy.: Old. arány, Maradék: Szélesség",
      "NFD": "NFDL",
      "FFD": "FFDL",
      "BFD": "BFDL"
    }

    counter = Counter(stat)
    result = list(map(list, counter.items()))
    result_sorted = sorted(result, key=lambda x: x[1], reverse=True)

    i = 0
    result_sorted_text=[]

    for row in result_sorted:
      i+=1
      result_sorted_text.append([
        i,
        vocabulary[names[int(row[0])]],
        row[1],
        round(row[1]/self.sample_number*100, 3)])

    return result_sorted_text

  #Létrehoz egy terminálos táblázatot
  def table_generator_tab(self, stat, names):
    result_sorted_text = self.evaluative_descriptive(stat, names)

    headers = ["Sorszám", "Algoritmus beállítása", "DB", "%"]
    print(tabulate(result_sorted_text, headers=headers, tablefmt="grid"))

  #Létrehoz egy táblázatot képként
  def table_generator_plt(self, stat, names):
    result_sorted_text = self.evaluative_descriptive(stat, names)

    headers = ["Sorszám", "Algoritmus beállítása", "DB", "%"]
    column_widths = [0.1, 0.7, 0.1, 0.1]

    fig, ax = plt.subplots(figsize=(10, 0.5 * len(result_sorted_text) + 1))  # dinamikus méret
    ax.axis('off')  # elrejti a tengelyeket

    table = ax.table(
      cellText=result_sorted_text,
      colLabels=headers,
      cellLoc='center',
      loc='center',
      colWidths=column_widths
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)  # méretarány a cellák között

    plt.title("Algoritmus statisztika", fontsize=14, pad=20)
    plt.show()

  #Step by Step algoritmusok különboző beállításait teszteli
  def step_by_step_stat(self, algorithm):
    sorted_sample = np.zeros((self.sample_number, 16, 5))
    sample = np.zeros((self.sample_number, 16, 5))
    stat = []
    names = []
    for i in range(0, self.sample_number):
      rectangles = lr.RandomRectangles.generate_random_size(40, 0, 0.5, 10)
      step_by_step = lss.StepByStepAlgorithms(rectangles)
      x = 0
      for sett_1 in self.setting_sorting_rec:
        for sett_2 in self.setting_sorting_rem:
          pattern, table, remnant_area = step_by_step_selection(step_by_step)[algorithm](sett_2, sett_1, 0)
          sample[i,x] = np.array([x, table, -remnant_area[0], -remnant_area[1], -remnant_area[2]])
          x += 1
          names.append(sett_1 +"_"+ str(sett_2))

      sorted_sample[i] = sample[i][np.lexsort((sample[i,:, 4], sample[i,:, 3], sample[i,:, 2], sample[i,:, 1]))]
      if np.array_equal(sorted_sample[i,0,1:],sorted_sample[i,1,1:]) == False:
        stat.append(sorted_sample[i,0,0])

      if i % 100 == 0:
        print(f"{i}. mintát értékelte ki!")

    self.table_generator_tab(stat, names)
    self.table_generator_plt(stat, names)

  #Függőleges sávos szab. tervet adó algoritmusokat teszteli
  def vertical_bar(self):
    sorted_sample = np.zeros((self.sample_number, 19, 5))
    sample = np.zeros((self.sample_number, 19, 5))
    stat = []
    names = []
    for i in range(0, self.sample_number):
      rectangles = lr.RandomRectangles.generate_random_size(40, 0, 0.5, 10)
      fit = lf.FitAlgorithms(rectangles)
      step_by_step = lss.StepByStepAlgorithms(rectangles)
      x = 0
      for sett_1 in self.setting_sorting_rec:
        for sett_2 in self.setting_sorting_rem:
          pattern, table, remnant_area = step_by_step.vertical_bar(sett_2, sett_1, 0)
          sample[i,x] = np.array([x, table, -remnant_area[0], -remnant_area[1], -remnant_area[2]])
          x += 1
          names.append(sett_1 +"_"+ str(sett_2))

      for sett in self.setting_fit:
        pattern, table, remnant_area = fit_selection(fit)[sett]()
        sample[i,x] = np.array([x, table, -remnant_area[0], -remnant_area[1], -remnant_area[2]])
        x += 1
        names.append(sett)

      sorted_sample[i] = sample[i][np.lexsort((sample[i,:, 4], sample[i,:, 3], sample[i,:, 2], sample[i,:, 1]))]
      if np.array_equal(sorted_sample[i,0,1:],sorted_sample[i,1,1:]) == False:
        stat.append(sorted_sample[i,0,0])

      if i % 100 == 0:
        print(f"{i}. mintát értékelte ki!")

    self.table_generator_tab(stat, names)
    self.table_generator_plt(stat, names)

  #Fit algoritmusokat teszteli
  def fit_stat(self):
    sorted_sample = np.zeros((self.sample_number, 3, 5))
    sample = np.zeros((self.sample_number, 3, 5))
    stat = []
    names = []
    for i in range(0, self.sample_number):
      rectangles = lr.RandomRectangles.generate_random_size(100, 0, 0.5, 10)
      fit = lf.FitAlgorithms(rectangles)
      x = 0

      for sett in self.setting_fit:
        pattern, table, remnant_area = fit_selection(fit)[sett]()
        sample[i,x] = np.array([x, table, -remnant_area[0], -remnant_area[1], -remnant_area[2]])
        x += 1
        names.append(sett)

      sorted_sample[i] = sample[i][np.lexsort((sample[i,:, 4], sample[i,:, 3], sample[i,:, 2], sample[i,:, 1]))]
      if np.array_equal(sorted_sample[i,0,1:],sorted_sample[i,1,1:]) == False:
        stat.append(sorted_sample[i,0,0])

      if i % 100 == 0:
        print(f"{i}. mintát értékelte ki!")

    self.table_generator_tab(stat, names)
    self.table_generator_plt(stat, names)