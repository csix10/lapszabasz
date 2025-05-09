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


vocabulary_1 = {
    "latitude": "SbS: Szab. jegy.: Szélesség",
    "height": "SbS: Szab. jegy.: Magasság",
    "area": "SbS: Szab. jegy.: Terület",
    "aspect_ratio": "SbS: Szab. jegy.: Old. arány",
    "NFD": "NFDL",
    "FFD": "FFDL",
    "BFD": "BFDL"
}
vocabulary_2 = {
    1: "Maradék: Terület",
    2: "Maradék: Tábla",
    21: "Maradék: Tábla és terület",
    3: "Maradék: Szélesség"
}


class Statistics:
    def __init__(self, sample_number):
        self.sample_number = sample_number
        self.setting_sorting_rec = ("latitude", "height", "area", "aspect_ratio")
        self.setting_sorting_rem = (1, 2, 21, 3)
        self.setting_fit = ("NFD", "FFD", "BFD")

    # Kiértékeli a statisztikai eredményeket és előkészíti a táblázat ábrázolását
    def evaluative_descriptive(self, stat, names):
        counter = Counter(stat)
        result = list(map(list, counter.items()))
        result_sorted = sorted(result, key=lambda x: x[1], reverse=True)

        i = 0
        result_sorted_text = []

        for row in result_sorted:
            i += 1
            result_sorted_text.append([
                i,
                names[int(row[0])],
                row[1],
                round(row[1] / self.sample_number * 100, 3)])

        return result_sorted_text

    # Létrehoz egy terminálos táblázatot
    def table_generator_tab(self, stat, names):
        result_sorted_text = self.evaluative_descriptive(stat, names)

        headers = ["Sorszám", "Algoritmus beállítása", "DB", "%"]
        print(tabulate(result_sorted_text, headers=headers, tablefmt="grid"))

    # Létrehoz egy táblázatot képként
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

    # Step by Step algoritmusok különboző beállításait teszteli
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
                    sample[i, x] = np.array([x, table, -remnant_area[0], -remnant_area[1], -remnant_area[2]])
                    x += 1
                    names.append(vocabulary_1[sett_1] + ", " + vocabulary_2[sett_2])

            sorted_sample[i] = sample[i][
                np.lexsort((sample[i, :, 4], sample[i, :, 3], sample[i, :, 2], sample[i, :, 1]))]

            if not np.array_equal(sorted_sample[i, 0, 1:], sorted_sample[i, 1, 1:]):
                stat.append(sorted_sample[i, 0, 0])

            if i % 100 == 0:
                print(f"{i}. mintát értékelte ki!")

        self.table_generator_tab(stat, names)
        self.table_generator_plt(stat, names)

    # Függőleges sávos szab. tervet adó algoritmusokat teszteli
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
                    sample[i, x] = np.array([x, table, -remnant_area[0], -remnant_area[1], -remnant_area[2]])
                    x += 1
                    names.append(vocabulary_1[sett_1] + ", " + vocabulary_2[sett_2])

            for sett in self.setting_fit:
                pattern, table, remnant_area = fit_selection(fit)[sett]()
                sample[i, x] = np.array([x, table, -remnant_area[0], -remnant_area[1], -remnant_area[2]])
                x += 1
                names.append(vocabulary_1[sett])

            sorted_sample[i] = sample[i][
                np.lexsort((sample[i, :, 4], sample[i, :, 3], sample[i, :, 2], sample[i, :, 1]))]

            if not np.array_equal(sorted_sample[i, 0, 1:], sorted_sample[i, 1, 1:]):
                stat.append(sorted_sample[i, 0, 0])

            if i % 100 == 0:
                print(f"{i}. mintát értékelte ki!")
        print(names)
        self.table_generator_tab(stat, names)
        self.table_generator_plt(stat, names)

    # Fit algoritmusokat teszteli
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
                sample[i, x] = np.array([x, table, -remnant_area[0], -remnant_area[1], -remnant_area[2]])
                x += 1
                names.append(vocabulary_1[sett])

            sorted_sample[i] = sample[i][
                np.lexsort((sample[i, :, 4], sample[i, :, 3], sample[i, :, 2], sample[i, :, 1]))]
            if not np.array_equal(sorted_sample[i, 0, 1:], sorted_sample[i, 1, 1:]):
                stat.append(sorted_sample[i, 0, 0])

            if i % 100 == 0:
                print(f"{i}. mintát értékelte ki!")

        self.table_generator_tab(stat, names)
        self.table_generator_plt(stat, names)

    def all_types(self):
        sorted_sample = np.zeros((self.sample_number, 10, 5))
        sample = np.zeros((self.sample_number, 10, 5))
        stat = []
        names = []
        verstepsett = (("latitude", 1), ("latitude", 21), ("latitude", 2))
        fitsett = ("BFD", "FFD")
        mixstepsett = (("latitude", 1), ("area", 1), ("height", 3), ("height", 1), ("area", 3))

        for i in range(0, self.sample_number):
            rectangles = lr.RandomRectangles.generate_random_size(50, 0, 0.5, 10)
            fit = lf.FitAlgorithms(rectangles)
            step_by_step = lss.StepByStepAlgorithms(rectangles)
            x = 0

            for vestset in verstepsett:
                pattern_1, table_1, remnant_area_1 = step_by_step.vertical_bar(vestset[1], vestset[0], 0)
                sample[i, x] = np.array([x, table_1, -remnant_area_1[0], -remnant_area_1[1], -remnant_area_1[2]])
                x += 1
                names.append("Függőleges sávos: " + vocabulary_1[vestset[0]] + ", " + vocabulary_2[vestset[1]])

            for fsett in fitsett:
                pattern_2, table_2, remnant_area_2 = fit_selection(fit)[fsett]()
                sample[i, x] = np.array([x, table_2, -remnant_area_2[0], -remnant_area_2[1], -remnant_area_2[2]])
                x += 1
                names.append("Függőleges sávos: " + vocabulary_1[fsett])

            for mistset in mixstepsett:
                pattern_3, table_3, remnant_area_3 = step_by_step.mix(mistset[1], mistset[0], 0)
                sample[i, x] = np.array([x, table_3, -remnant_area_3[0], -remnant_area_3[1], -remnant_area_3[2]])
                x += 1
                names.append("Kevert: " + vocabulary_1[mistset[0]] + ", " + vocabulary_2[mistset[1]])

            sorted_sample[i] = sample[i][
                np.lexsort((sample[i, :, 4], sample[i, :, 3], sample[i, :, 2], sample[i, :, 1]))]

            if not np.array_equal(sorted_sample[i, 0, 1:], sorted_sample[i, 1, 1:]):
                stat.append(sorted_sample[i, 0, 0])

            if i % 100 == 0:
                print(f"{i}. mintát értékelte ki!")

        self.table_generator_tab(stat, names)
        self.table_generator_plt(stat, names)

    def mix_c_testing(self):
        sorted_sample = np.zeros((self.sample_number, 160, 5))
        sample = np.zeros((self.sample_number, 160, 5))
        stat = []
        names = []
        for i in range(0, self.sample_number):
            rectangles = lr.RandomRectangles.generate_random_size(40, 0, 0.5, 10)
            step_by_step = lss.StepByStepAlgorithms(rectangles)
            x = 0
            for sett_1 in self.setting_sorting_rec:
                for sett_2 in self.setting_sorting_rem:
                    for c_1 in range(10):
                        c = c_1 * 0.1
                        pattern, table, remnant_area = step_by_step.mix(sett_2, sett_1, c)
                        sample[i, x] = np.array([x, table, -remnant_area[0], -remnant_area[1], -remnant_area[2]])
                        x += 1
                        names.append(vocabulary_1[sett_1] + " " + vocabulary_2[sett_2] + " c: " + str(round(c, 2)))

            sorted_sample[i] = sample[i][
                np.lexsort((sample[i, :, 4], sample[i, :, 3], sample[i, :, 2], sample[i, :, 1]))]

            if not np.array_equal(sorted_sample[i, 0, 1:], sorted_sample[i, 1, 1:]):
                stat.append(sorted_sample[i, 0, 0])

            if i % 100 == 0:
                print(f"{i}. mintát értékelte ki!")

        self.table_generator_tab(stat, names)
        self.table_generator_plt(stat, names)
