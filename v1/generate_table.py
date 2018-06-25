from math import ceil
from math import floor

def linspace(lo, hi, steps):
    """Return a list of int numbers where minimum and maximum is first and
    last number and all steps are evenly distributes between them.
    [lo, N+1, N+2,... , hi]
    """
    lo = floor(lo)
    hi = ceil(hi)
    if (steps-1) > (hi-lo):
        raise ValueError('To many steps for range')
    return [floor(lo + (hi-lo)/(steps-1)*i) for i in range(steps)]

def get_limits():
    """These numbers are taken directly from fit calculator frontend.
    """
    INCH_TO_CM = 2.54
    limits_inches = {
        "inseam":(20,44),
        "trunk": (15, 35),
        "forearm": (6, 20),
        "arm": (13, 40),
        "thigh": (13, 40),
        "lower_leg": (12, 35),
        "sternal_notch": (30, 85),
        "height": (50, 95),
    }
    limits_cm = {
        key:(int(value[0] * INCH_TO_CM)+2, int(value[1] * INCH_TO_CM)-2)
        for (key, value) in limits_inches.items()
    }
    return limits_cm

def create_table(step):
    """Return a table of all possible fit combinations from min to max with
    given step.
    """
    limits = get_limits()
    table = []
    for a in linspace(*limits['inseam'], step):
        for b in linspace(*limits['trunk'], step):
            for c in linspace(*limits['forearm'], step):
                for d in linspace(*limits['arm'], step):
                    for e in linspace(*limits['thigh'], step):
                        for f in linspace(*limits['lower_leg'], step):
                            for g in linspace(*limits['sternal_notch'], step):
                                for h in linspace(*limits['height'], step):
                                    current_row = (a,b,c,d,e,f,g,h)
                                    table.append(current_row)
    return table

def calculate_table_size(steps):
    return steps**8

def test_linspace():
    print('All folowing should be True:')
    print(linspace(10,50,5) == [10, 20, 30, 40, 50])
    print(linspace(10,100,50)[0] == 10)
    print(linspace(3, 99, 80)[-1] == 99)
    print(linspace(1,10,10)[5] == 6)
    print(linspace(33.3, 66.6, 5)[0] == 33)
    print(linspace(33.3, 66.6, 5)[-1] == 67)
    print(linspace(20*2.54, 44*2.54, 2) == [50, 112])
    print(linspace(50*2.54,95*2.54,3)[-1] == 242)
    print('All done!')

def test_create_table():
    print('All folowing should be True:')
    limits = get_limits()
    for steps in range(2,7):
        size = calculate_table_size(steps)
        table = create_table(steps)
        print(
            (size == len(table)),
            (table[0][0] == limits['inseam'][0]),
            (table[0][7] == limits['height'][0]),
            (table[-1][0] == limits['inseam'][1]),
            (table[-1][7] == limits['height'][1]),
        )
    print('All done!')


if __name__ == '__main__':
    test_linspace()
    test_create_table()
