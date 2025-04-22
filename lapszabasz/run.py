import lapszabasz.statistics as ls
import lapszabasz.step_by_step as lss
import lapszabasz.randomrec as lr

def run_stat_1(a, b):
    stat = ls.Statistics(10)
    stat.step_by_step_stat("vertical_bar")

def run_stat_2(a, b):
    data = lr.RandomRectangles.generate_random_size(10, 0, 0.5, 5)
    step = lss.StepByStepAlgorithms(data)

    step.interactive_figure()

if __name__=="__main__":
    ''''
    inp = input("Milyen Algoritmust szeretnél futtatni?\nA: Statisztika 1\nB: Statisztika 2")
    algos = {
        "A": run_stat_1,
        "B": run_stat_2
    }

    if inp in algos.keys:
        algos[inp]()
    else:
        print("Ilyen nincs")
    '''
    run_stat_2(0,0)
