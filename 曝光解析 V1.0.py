'''
This script performs calculations related to exposure settings for SSS Automotive CMOS Image Sensors. 
It includes functions to convert hexadecimal numbers to decimal, find the closest smaller even number, calculate various time intervals, 
and determine exposure settings based on input parameters.

The script begins by defining hexadecimal constants for various parameters such as line length, frame length, frame rate, etc. 
These constants are converted to decimal values using the `hex_to_decimal_U_X_Y` function.

The script then defines several utility functions:
- `hex_to_decimal_U_X_Y`: Converts a hexadecimal number to its decimal equivalent.
- `closest_smaller_even`: Finds the closest smaller even integer to a given number.
- `time_1C_s`: Calculates the time for one clock cycle.
- `time_1H_s`: Calculates the time for one line.
- `exp_time_s`: Calculates the exposure time in seconds.
- `exp_time_line`: Calculates the exposure time in lines.

In the `main` function, the exposure settings are computed based on the provided constants and parameters. 
These settings include clock time, line time, exposure time for different modes (SP1 and SP2), and are printed as output.

The script also contains two unit test section.

Author: Liubingtao@Gmail.com 
Date: 2024/04/25
Version: V1.0
'''


# user edit 

SHT_TIME_US = 2005 # in unit of us

# 5 FPS
LINE_LENGTH_OUT           = "0x8CA0  "
FRAME_LENGTH_OUT          = "0x960   "
ADDITIONAL_LINE_OUT       = "0x0     "
FRAME_RATE                = "0x50000 "
FRAME_RATE_BASE           = "0x50000 "
INTG_TIME_FINE_SP1H_OUT   = "0x370   " # For SP1 H
INTG_TIME_FINE_SP1LD_OUT  = "0x8A8   "
INTG_TIME_FINE_SP1LS_OUT  = "0x0     "
INTG_TIME_FINE_SP2_OUT    = "0x0     " # For SP2 
INTG_TIME_FINE_SP1ECN_OUT = "0x0     "
FME_SHTVAL_FINE_S2        = "0x0     "


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
    
    if abs (round(number) - number) < 0.0000001: # 59.999999999999 → 60
        integer_part = round(number)
    else:
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

def exp_time_s (exposure_time_LINES, one_line_time_S, toffset_CLOCKS, one_clock_time_US):
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
    clock_time_NS = clock_time_S * 1000000000

    line_time_S = time_1H_s(D_FRAME_RATE_BASE, D_FRAME_LENGTH_OUT)
    line_time_US = line_time_S * 1000000

    SP1_exp_time_line_value = exp_time_line(SHT_TIME_US, line_time_S, D_INTG_TIME_FINE_SP1H_OUT, clock_time_US) / (1000000 * 1000000)
    SP1_exp_time_line_even = closest_smaller_even(SP1_exp_time_line_value)

    SP1_exp_time_s_value = exp_time_s(SP1_exp_time_line_even, line_time_S, D_INTG_TIME_FINE_SP1H_OUT, clock_time_S)
    SP1_exp_time_ms_value = SP1_exp_time_s_value * 1000

    SP2_exp_time_line_value = exp_time_line(SHT_TIME_US, line_time_S, D_INTG_TIME_FINE_SP2_OUT, clock_time_US) / (1000000 * 1000000)
    SP2_exp_time_line_even = closest_smaller_even(SP2_exp_time_line_value)

    SP2_exp_time_s_value = exp_time_s(SP2_exp_time_line_even, line_time_S, D_INTG_TIME_FINE_SP2_OUT, clock_time_S)
    SP2_exp_time_ms_value = SP2_exp_time_s_value * 1000

    print(f"Exposure Settings are as follows：")
    print(f"1 clk time is {clock_time_NS} NS,")
    print(f"1 H time is {line_time_US} US,")
    print(f"For SP1 Line:")
    print(f"Line = {SP1_exp_time_line_value} / {SP1_exp_time_line_even} Line,") 
    print(f"Time = {SP1_exp_time_ms_value} MS")
    print(f"For SP2 Line:")
    print(f"Line = {SP2_exp_time_line_value} / {SP2_exp_time_line_even} Line,") 
    print(f"Time = {SP2_exp_time_ms_value} MS")

if __name__ == "__main__":
    main()
''' 
  
# Unit Test 001

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
# Unit Test 002

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