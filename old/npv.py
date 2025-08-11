import numpy_financial as npf

cash_flows = [-11000, 700, 1450, 1450, 1450, 1450, 1700, 1700, 1700, 1700, 1700]
irr = npf.irr(cash_flows)
print(f"IRR = {irr * 100:.2f}%")
