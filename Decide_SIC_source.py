# =============================================================================
# DECIDE SIC SOURCE BASED ON TIME PERIODS
# OSI450a period 1982-1990
# SICCI_HR_SIC period 1991 - 2002 (jun) + 2011-2012
# OSI458 period 2002 (jul) - 2023, except 2011 () - 2012 ()
def identify_product_ID(y, m, d):
    print(m)
    if y>=1982 and y<=1991:
        Product_IDs = 'OSI450a'
    elif y>=1992 and y<=2001:
        Product_IDs = 'SICCI_HR_SIC'
    elif (y>=2003 and y<=2010) or (y>=2013 and y<2021):
        Product_IDs = 'OSI458'
    elif y>=2021:
        Product_IDs = 'OSI458_TU'

    elif y==2002:
        if m<=5:
            Product_IDs = 'SICCI_HR_SIC'
        # start from the 1st of june 06
        else:
            Product_IDs = 'OSI458'
    elif y==2011:
        if m>=10 and d>=5:
            Product_IDs = 'SICCI_HR_SIC'
        else:
            Product_IDs = 'OSI458'
    elif y==2012:
        if m<=7 and d<=23:
            Product_IDs = 'SICCI_HR_SIC'
        else:
            Product_IDs = 'OSI458'
    
    return Product_IDs

# =============================================================================
