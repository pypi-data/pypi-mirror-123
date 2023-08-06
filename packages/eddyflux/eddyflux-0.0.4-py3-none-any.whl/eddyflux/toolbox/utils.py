def unit2unit(val, choice):
    """
    Input:
    ------
    val:
        value of which the unit to be changed. 
    choice: int
        what unit change to what unit?
        g/kg -> kg/kg
    """
    if (choice == "g/kg -> kg/kg") or (choice == 1):
        val = val / 1000
    elif (choice == "g/m3 -> mg/m3") or (choice == 2):
        val = val * 1000
    else:
        raise(Exception("Must specify a correct choice"))
    return val