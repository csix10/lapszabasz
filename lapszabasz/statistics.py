import numpy as np
from collections import Counter
from tabulate import tabulate

import lapszabasz.random as lr
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

  def evaluative_descriptive(self, stat, names):
    counter = Counter(stat)
    result = list(map(list, counter.items()))
    result_sorted = sorted(result, key=lambda x: x[1], reverse=True)
    i = 0
    result_sorted_text=[]

    for row in result_sorted:
      i+=1
      result_sorted_text.append([i, names[int(row[0])], row[1], row[1]/self.sample_number*100])

    headers = ["Sorszám", "Algoritmus beállítása", "DB", "%"]
    print(tabulate(result_sorted_text, headers=headers, tablefmt="grid"))

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
          #pattern, table, remnant_area = getattr(step_by_step, algorithm)(sett_2, sett_1, 0)
          sample[i,x] = np.array([x, table, -remnant_area[0], -remnant_area[1], -remnant_area[2]])
          x += 1
          names.append(sett_1 +"_"+ str(sett_2))

      sorted_sample[i] = sample[i][np.lexsort((sample[i,:, 4], sample[i,:, 3], sample[i,:, 2], sample[i,:, 1]))]
      if np.array_equal(sorted_sample[i,0,1:],sorted_sample[i,1,1:]) == False:
        stat.append(sorted_sample[i,0,0])

    self.evaluative_descriptive(stat, names)

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
        sett= sett + "_lanes"
        pattern, table, remnant_area  = getattr(fit, sett)()
        sample[i,x] = np.array([x, table, -remnant_area[0], -remnant_area[1], -remnant_area[2]])
        x += 1
        names.append(sett)

      sorted_sample[i] = sample[i][np.lexsort((sample[i,:, 4], sample[i,:, 3], sample[i,:, 2], sample[i,:, 1]))]
      if np.array_equal(sorted_sample[i,0,1:],sorted_sample[i,1,1:]) == False:
        stat.append(sorted_sample[i,0,0])

    self.evaluative_descriptive(stat, names)

  def fit(self):
    sorted_sample = np.zeros((self.sample_number, 3, 5))
    sample = np.zeros((self.sample_number, 3, 5))
    stat = []
    names = []
    for i in range(0, self.sample_number):
      if i%100 == 0:
        print(i)
      rectangles = lr.RandomRectangles.generate_random_size(100, 0, 0.5, 10)
      fit = lf.FitAlgorithms(rectangles)
      x = 0

      for sett in self.setting_fit:
        pattern, table, remnant_area = fit_selection(fit)[sett]()
        #sett= sett + "_lanes"
        #pattern, table, remnant_area  = getattr(fit, sett)()
        sample[i,x] = np.array([x, table, -remnant_area[0], -remnant_area[1], -remnant_area[2]])
        x += 1
        names.append(sett)

      sorted_sample[i] = sample[i][np.lexsort((sample[i,:, 4], sample[i,:, 3], sample[i,:, 2], sample[i,:, 1]))]
      if np.array_equal(sorted_sample[i,0,1:],sorted_sample[i,1,1:]) == False:
        stat.append(sorted_sample[i,0,0])

    self.evaluative_descriptive(stat, names)