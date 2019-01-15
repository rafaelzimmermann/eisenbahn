

def create_chars(lcd):
    degree_pattern = [6,9,9,6,0,0,0,0]
    n71_pattern = [29,5,9,9,9,0,0,0]
    u_pattern = [0,27,27,27,27,27,14,0]
    n08_pattern = [0,31,13,15,13,31,0,0]

    lcd.create_char(0, degree_pattern)
    lcd.create_char(1, n71_pattern)
    lcd.create_char(2, u_pattern)
    lcd.create_char(3, n08_pattern)
    return {
        "{DEGREE_SIGN}": '\x00',
        "U71": '\x01\x02',
        "708": '\x02\x03'
    }
