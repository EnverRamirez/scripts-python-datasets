import numpy as np
import numpy.ma as ma

# Sample data with NaN values
x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
y = np.array([2.1, 3.0, np.nan, 5.2, np.nan, 7.8, 8.9, 10.1])

# Create masked arrays
masked_y = ma.masked_invalid(y)
masked_x = ma.masked_where(ma.getmask(masked_y), x)

print(y, masked_y, x, masked_x)
# Perform linear regression on valid points only
slope, intercept = ma.polyfit(masked_x, masked_y, 1)

print(f"Trend line: y = {slope:.2f}x + {intercept:.2f}")
