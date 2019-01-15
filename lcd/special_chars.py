

def create_chars(lcd):
    degree_pattern = [6,9,9,6,0,0,0,0]
    celsius_pattern = [14,27,24,24,24,27,14,0]
    u_pattern = [0,27,27,27,27,27,14,0]
    n0_pattern = [14,27,27,27,27,27,14,0]
    n1_pattern = [2,6,14,6,6,6,6,0]
    n7_pattern = [31,3,6,12,12,12,12,0]
    n8_pattern = [14,27,27,14,27,27,14,0]

    lcd.create_char(0, degree_pattern)
    lcd.create_char(1, celsius_pattern)
    lcd.create_char(2, u_pattern)
    lcd.create_char(3, n0_pattern)
    lcd.create_char(4, n1_pattern)
    lcd.create_char(5, n7_pattern)
    lcd.create_char(6, n8_pattern)
    return {
        "{CELSIUS_DEGREE}": '\x00\x01',
        "U71": '\x02\x05\x04',
        "708": '\x05\x03\x06'
    }
