# cuffnote
A python library for simple mortgage calculations

## package modules

1. **cuffnote.mortgages.Mortgage**: The base class represents a plain vanilla mortgage
1. **cuffnote.mortgages.ExtraMonthlyPrincipal**: Inherits from the base class & allows modelling a mortgage with extra monthly principal payments. The start date of the extra payments does not have to be the same as the start date of the loan.
1. **cuffnote.mortgages.AnnualLumpPayment**: Inherits from both base class & ExtraMonthlyPrincipal. Allows modelling a mortgage with annual principal lump payments that occur only once a year.

## running unittests using coverage & unittest

Launch the unittests using coverage:

`$ coverage run -m unittest -v tests/test_* ; coverage html`