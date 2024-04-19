## Introduction

This Python script provides a utility for converting hexadecimal numbers to decimal values, and performing exposure time calculations for imaging applications. It includes functions to convert hexadecimal numbers to decimal format and to calculate exposure times based on various parameters such as frame rate, maximum value, and clock time.

## Requirements

- Python 3.x

## Usage

1. **hex_to_decimal_U_X_Y(hex_num, int_num, frac_num):**
   - Converts a hexadecimal number to a decimal value in the U X.Y format.
   - Parameters:
     - `hex_num`: The hexadecimal number to convert (as a string).
     - `int_num`: The number of bits for the integer part.
     - `frac_num`: The number of bits for the fractional part.
   - Returns:
     - The decimal representation of the hexadecimal number.
2. **closest_smaller_even(number)**
   - This function takes a floating-point number as input and returns the closest smaller even integer.
   - Parameters:
     - `number`: The input floating-point number.
   - Returns
     - The closest smaller even integer to the input number.

3. **time_1C_s(frame_rate, Vmax, Hmax):**
   - Calculates the clock time for a given frame rate, maximum value, and horizontal maximum value.
   - Parameters:
     - `frame_rate`: Frame rate of the imaging system.
     - `Vmax`: Vertical Maximum Lines.
     - `Hmax`: Horizontal Maximum Pixels.
   - Returns:
     - one clock time.

3. **time_1H_s(frame_rate, Vmax):**
   - Calculates the line time for a given frame rate and maximum value.
   - Parameters:
     - `frame_rate`: Frame rate of the imaging system.
     - `Vmax`: Vertical Maximum Lines.
   - Returns:
     - One line time.

4. **exp_time_us(exposure_time_LINES, one_line_time_S, toffset_CLOCKS, one_clock_time_US):**
   - Calculates the exposure time in microseconds.
   - Parameters:
     - `exposure_time_LINES`: Exposure time (in lines).
     - `one_line_time_S`: Time for one line (in seconds).
     - `toffset_CLOCKS`: Offset clocks (in clocks).
     - `one_clock_time_US`: Time for one clock (in microseconds).
   - Returns:
     - The exposure time in microseconds.

5. **exp_time_line(exposure_time_US, one_line_time_S, toffset_CLOCKS, one_clock_time_US):**
   - Calculates the exposure time in lines.
   - Parameters:
     - `exposure_time_US`: Exposure time (in microseconds).
     - `one_line_time_S`: Time for one line (in seconds).
     - `toffset_CLOCKS`: Offset clocks(in clocks).
     - `one_clock_time_US`: Time for one clock (in microseconds).
   - Returns:
     - The exposure time in lines.
