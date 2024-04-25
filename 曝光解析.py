'''
- V0.01 Initial realease 
- only works for SP1H Line
- has some minor issue (59.999999999 (60) will be rounded to 58)
'''

# user edit 
LINE_LENGTH_OUT           = "0x1194  "
FRAME_LENGTH_OUT          = "0x960   "
ADDITIONAL_LINE_OUT       = "0x960   "
FRAME_RATE                = "0x140000"
FRAME_RATE_BASE           = "0x280000"
INTG_TIME_FINE_SP1H_OUT   = "0x370   "
INTG_TIME_FINE_SP1LD_OUT  = "0x0     "
INTG_TIME_FINE_SP1LS_OUT  = "0x0     "
INTG_TIME_FINE_SP2_OUT    = "0x0     "
INTG_TIME_FINE_SP1ECN_OUT = "0x0     "
FME_SHTVAL_FINE_S2        = "0x0     "  
SHT_TIME_US = 10000 # in unit of us

def hex_to_decimal_U_X_Y(hex_num, int_num, frac_num):
    while True:
        # Calculate total number of bits
        total_bits = int_num + frac_num

        # Convert hexadecimal to decimal
        decimal_num = int(hex_num, 16)

        # Check if the hexadecimal number is within the valid range
        if decimal_num >= 2 ** total_bits:
            print("Error: Hexadecimal number is out of range.")
            hex_num = input("Enter a hexadecimal number within the valid range: ")
            continue

        # Convert hexadecimal to binary
        binary_num = bin(decimal_num)[2:].zfill(total_bits)

        # Ensure binary number has enough bits
        binary_num = binary_num.zfill(total_bits)

        # Extract integer and fractional parts
        integer_part = int(binary_num[:int_num], 2)
        if frac_num > 0:
            fractional_part = int(binary_num[int_num:], 2) / (2 ** frac_num)
        else:
            fractional_part = 0

        # Calculate decimal value
        decimal_result = integer_part + fractional_part

        return decimal_result
    
def closest_smaller_even(number):
    # float to int
    integer_part = int(number)
    # if float = 2n
    if integer_part % 2 == 0:
        return integer_part
    # if float = 2n+1
    return integer_part - 1

def time_1C_s (frame_rate, Vmax, Hmax):
    Clock_time = 1/ frame_rate / Vmax / Hmax
    return Clock_time

def time_1H_s (frame_rate, Vmax):
    Line_time = 1/ frame_rate / Vmax
    return Line_time

def exp_time_us (exposure_time_LINES, one_line_time_S, toffset_CLOCKS, one_clock_time_US):
    Exposure_time_US = exposure_time_LINES * ( one_line_time_S) + toffset_CLOCKS * one_clock_time_US
    return Exposure_time_US

def exp_time_line (exposure_time_US, one_line_time_S, toffset_CLOCKS, one_clock_time_US):
    Exposrue_time_LINE = (exposure_time_US - (toffset_CLOCKS * one_clock_time_US)) / (one_line_time_S / 1000000)
    return Exposrue_time_LINE


D_LINE_LENGTH_OUT = hex_to_decimal_U_X_Y(LINE_LENGTH_OUT, 16, 0)
D_FRAME_LENGTH_OUT = hex_to_decimal_U_X_Y(FRAME_LENGTH_OUT, 18, 0)
D_ADDITIONAL_LINE_OUT = hex_to_decimal_U_X_Y(ADDITIONAL_LINE_OUT, 18, 0)
D_FRAME_RATE = hex_to_decimal_U_X_Y(FRAME_RATE, 16, 16)
D_FRAME_RATE_BASE = hex_to_decimal_U_X_Y(FRAME_RATE_BASE, 16, 16)
D_INTG_TIME_FINE_SP1H_OUT = hex_to_decimal_U_X_Y(INTG_TIME_FINE_SP1H_OUT, 30, 0)
D_INTG_TIME_FINE_SP1LD_OUT = hex_to_decimal_U_X_Y(INTG_TIME_FINE_SP1LD_OUT, 30, 0)
D_INTG_TIME_FINE_SP1LS_OUT = hex_to_decimal_U_X_Y(INTG_TIME_FINE_SP1LS_OUT, 30, 0)
D_INTG_TIME_FINE_SP2_OUT = hex_to_decimal_U_X_Y(INTG_TIME_FINE_SP2_OUT, 30, 0)
D_INTG_TIME_FINE_SP1ECN_OUT = hex_to_decimal_U_X_Y(INTG_TIME_FINE_SP1ECN_OUT, 30, 0)
D_FME_SHTVAL_FINE_S2 = hex_to_decimal_U_X_Y(FME_SHTVAL_FINE_S2, 15, 0)

def main():
    clock_time_S = time_1C_s(D_FRAME_RATE_BASE, D_LINE_LENGTH_OUT, D_FRAME_LENGTH_OUT)
    clock_time_US = clock_time_S * 1000000
    line_time_S = time_1H_s(D_FRAME_RATE_BASE, D_FRAME_LENGTH_OUT)

    exp_time_line_value = exp_time_line(SHT_TIME_US, line_time_S, D_INTG_TIME_FINE_SP1H_OUT, clock_time_US) / (1000000 * 1000000)
    exp_time_line_even = closest_smaller_even(exp_time_line_value)

    exp_time_us_value = exp_time_us(exp_time_line_even, line_time_S, D_INTG_TIME_FINE_SP1H_OUT, clock_time_S)

    print(f"1 clk time is {clock_time_S} S,")
    print(f"1 H time is {line_time_S} S,")
    print(f"Line = {exp_time_line_value} / {exp_time_line_even} Line,") 
    print(f"time = {exp_time_us_value} S")
    
if __name__ == "__main__":
    main()

'''    
# Unit Test
def main():
    
    print(f"LINE_LENGTH_OUT           = {D_ADDITIONAL_LINE_OUT}")
    print(f"FRAME_LENGTH_OUT          = {D_LINE_LENGTH_OUT}")           
    print(f"ADDITIONAL_LINE_OUT       = {D_FRAME_LENGTH_OUT}")                
    print(f"FRAME_RATE                = {D_FRAME_RATE}")                
    print(f"FRAME_RATE_BASE           = {D_FRAME_RATE_BASE}")           
    print(f"INTG_TIME_FINE_SP1H_OUT   = {D_INTG_TIME_FINE_SP1H_OUT}")   
    print(f"INTG_TIME_FINE_SP1LD_OUT  = {D_INTG_TIME_FINE_SP1LD_OUT}")  
    print(f"INTG_TIME_FINE_SP1LS_OUT  = {D_INTG_TIME_FINE_SP1LS_OUT}")  
    print(f"INTG_TIME_FINE_SP2_OUT    = {D_INTG_TIME_FINE_SP2_OUT}")    
    print(f"INTG_TIME_FINE_SP1ECN_OUT = {D_INTG_TIME_FINE_SP1ECN_OUT}") 
    print(f"FME_SHTVAL_FINE_S2        = {D_FME_SHTVAL_FINE_S2}") 

    
if __name__ == "__main__":
    main()
'''

'''    
# Unit Test
def main():
    clock_time_S = time_1C_s(30, 2400, 6000)
    clock_time_US = clock_time_S * 1000000
    line_time_S = time_1H_s(30, 2400)

    exp_time_line_value = exp_time_line(10000, line_time_S, 880, clock_time_US) / (1000000 * 1000000)
    exp_time_line_even = closest_smaller_even(exp_time_line_value)

    exp_time_us_value = exp_time_us(exp_time_line_even, line_time_S, 880, clock_time_S)

    print(f"1 clk time is {clock_time_S} S,")
    print(f"1 H time is {line_time_S} S,")
    print(f"Line = {exp_time_line_value} / {exp_time_line_even} Line,") 
    print(f"time = {exp_time_us_value} S")
    
if __name__ == "__main__":
    main()
'''
