

def create_chars(lcd):
    degree_pattern = [6,9,9,6,0,0,0,0]
    celsius_pattern = [14,27,24,24,24,27,14,0]
    n71_pattern = [31,2,26,22,22,22,31,31]
    u_pattern = [31,21,21,21,21,17,31,31]
    n18_pattern = [31,8,10,8,10,8,31,31]

    lcd.create_char(0, degree_pattern)
    lcd.create_char(1, celsius_pattern)
    lcd.create_char(2, u_pattern)
    lcd.create_char(3, n71_pattern)
    lcd.create_char(4, n18_pattern)
    return {
        "{CELSIUS_DEGREE}": '\x00\x01',
        "U71": '\x02\x03',
        "708": '\x03\x04'
    }
