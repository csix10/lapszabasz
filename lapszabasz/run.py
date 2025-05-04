import lapszabasz.statistics as ls


def run_stat_1(n):
    inp = input("Milyen tipust szeretnél:\nA: Függőleges sávos\nB: Vízszintes sávos\nC: Kevert\n")
    stat = ls.Statistics(int(n))
    selection = {
        "A": lambda: stat.step_by_step_stat("vertical_bar"),
        "B": lambda: stat.step_by_step_stat("horizontal_bar"),
        "C": lambda: stat.step_by_step_stat("mix")
    }

    if inp in selection.keys():
        selection[inp]()
    else:
        print("Hibás választás. Csak A, B vagy C lehet.")


def run_stat_2(n):
    stat = ls.Statistics(int(n))
    stat.fit_stat()

def run_stat_3(n):
    stat = ls.Statistics(int(n))
    stat.vertical_bar()

def run_stat_4(n):
    stat = ls.Statistics(int(n))
    stat.all_types()

def run_stat_5(n):
    stat = ls.Statistics(int(n))
    stat.mix_c_testing()

if __name__=="__main__":
    inp_1 = input("Milyen tesztet szeretnél futtatni?\nA: Step by Step algortimus családon\nB: Fit algoritmus családon\nC: Függőleges sávos algoritmusokon\nD: Kevert és sávos összehasonlítás\nE: c test\n" )
    inp_2 =input("Mekkora mintán? \n")
    algos = {
        "A": run_stat_1,
        "B": run_stat_2,
        "C": run_stat_3,
        "D": run_stat_4,
        "E": run_stat_5
    }

    if inp_1 in algos.keys():
        algos[inp_1](inp_2)
    else:
        print("Ilyen nincs")