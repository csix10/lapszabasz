def run_stat_1(a, b):
    pass

def run_stat_2(a, b):
    pass

if __name__=="__main__":
    inp = input("Milyen Algoritmust szeretnél futtatni?\nA: Statisztika 1\nB: Statisztika 2")
    algos = {
        "A": run_stat_1,
        "B": run_stat_2
    }

    if inp in algos.keys:
        algos[inp]()
    else:
        print("Ilyen nincs")
