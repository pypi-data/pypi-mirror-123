#!/usr/bin/env python

# -*-coding:utf-8 -*-

import numpy as np
import numpy_financial as npf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


class Mortgage:
    """
    A class to represent a mortgage loan for purchasing a house. This is a base class that builds an amortization table for an n-year fixed interest rate loan. 
    The base class does not include extra principal payments.
    
    Attributes
    -----------
    __purchase_price (int): The full purchase price amount. Example: 200000 for a $200,000 purchase price.
    __down_payment_percent (float): Percent of purchase price paid as down payment. Example: 0.2 for a 20% down payment.
    __interest_rate (float): The loan interest rate. Example: 0.04125 for a 4.125% rate.
    __start_date (str): The starting date the loan begins, represented as '%Y-%m-%d'. Example: '2000-5-1' for a May 1, 2000 start date.
    __years (int): The length of the mortgage loan in years. Example: 30 for a 30 year loan.
    __num_yearly_payments (int, optional): Th[summary]e numprivate method to update from setterber of installment payments in a year. Typically, mortgages are paid monthly. Defaults to 12.
    __down_payment (int): The down payment paid at the start of the loan
    __loan_amount (int): The financed portion of the mortgage. Equals purchase_price - down_payment.
    __payment (float): The monthly principal + interest payment
    __payment_range (DatetimeIndex): Datetime index of payment periods from loan start date to loan payoff date.
    """
    
    def __init__(self, purchase_price, down_payment_percent, interest_rate, start_date, years, num_yearly_payments=12):
        """Initializes base mortgage class instance using input arguments

        Args:
            purchase_price (int): The full purchase price amount. Example: 200000 for a $200,000 purchase price.
            down_payment_percent (float): Percent of purchase price paid as down payment. Example: 0.2 for a 20% down payment.
            interest_rate (float): The loan interest rate. Example: 0.04125 for a 4.125% rate.
            start_date (str): The starting date the loan begins, represented as '%Y-%m-%d'. Example: '2000-5-1' for a May 1, 2000 start date.
            years (int): The length of the mortgage loan in years. Example: 30 for a 30 year loan.
            num_yearly_payments (int, optional): The number of installment payments in a year. Typically, mortgages are paid monthly. Defaults to 12.
        """
        # initialize instance variables
        self.__purchase_price = purchase_price
        self.__down_payment_percent = down_payment_percent
        self.__interest_rate = interest_rate
        self.__start_date = start_date
        self.__years = years
        self.__num_yearly_pmts = num_yearly_payments
        
    @property
    def __down_payment(self):
        return self.get_purchase_price() * self.get_down_payment_percent()
    
    @property
    def __loan_amount(self):
        return self.get_purchase_price() - self.get_down_payment()
    
    @property
    def __payment(self):
        return round(-1 * npf.pmt(self.__interest_rate/self.__num_yearly_pmts, self.__years*self.__num_yearly_pmts, self.__loan_amount), 2)
    
    def get_payment(self):
        """returns monthly principal + interest payment

        Returns:
            float: monthly payment
        """
        return self.__payment
    
    def get_purchase_price(self):
        """returns purchase price (loan amount + down payment)

        Returns:
            int: the purchase price
        """
        return self.__purchase_price
    
    def set_purchase_price(self, purchase_price):
        """method to set/change purchase price
        
        Changing the purchase price will recalculate the down payment, loan amount, and monthly payment attributes.
        
        Args:
            purchase_price (int): purchase price
        """
        self.__purchase_price = purchase_price
        
    def get_down_payment_percent(self):
        """returns down payment percent

        Returns:
            float: down payment percent
        """
        return self.__down_payment_percent
    
    def set_down_payment_percent(self, down_payment_percent):
        """Set/change the down payment percent
        
        Changing the down payment percent will recalculate the down payment, the loan amount, and the monthly payment attributes.
        
        Args:
            down_payment_percent (float): the down payment percent, as a float. Example: 0.0475 for a 4.75% rate.
        """
        self.__down_payment_percent = down_payment_percent
        
    def get_down_payment(self):
        """Returns down payment (purchase price * down payment percent)

        Returns:
            int: The down payment
        """
        return self.__down_payment
    
    def get_interest_rate(self):
        """Returns the interest rate

        Returns:
            float: interest rate as a float (0.04125 for 4.125%)
        """
        return self.__interest_rate
    
    def set_interest_rate(self, interest_rate):
        """Set/change the interest rate
        
        Changing the interest rate will recalculate the monthly payment attribute
        
        Args:
            interest_rate (float): interest rate, expressed as a float (0.04125 for 4.125%)
        """
        self.__interest_rate = interest_rate
    
    def get_years(self):
        """returns the number of years over which the mortgage is amortized

        Returns:
            int: number of years
        """
        return self.__years
    
    def set_years(self, years):
        """Set/change the number of years
        
        Changing the number of years will recalculate the monthly payment attribute

        Args:
            years ([type]): [description]
        """
        self.__years = years
    
    def get_num_yearly_pmts(self):
        """Returns the number of yearly payments

        Returns:
            int: number of yearly payments
        """
        return self.__num_yearly_pmts
    
    def set_num_yearly_pmts(self, num_yearly_pmts):
        """Set/change the number of yearly payments
        
        Changing the number of yearly payments will recalculate the monthly payment attribute

        Args:
            num_yearly_pmts ([type]): [description]
        """
        self.__num_yearly_pmts = num_yearly_pmts
    
    def get_start_date(self):
        """Returns the mortgage start date

        Returns:
            datetime.date: mortgage start date
        """
        return self.__start_date
    
    def set_start_date(self, start_date):
        """Set/change the mortgage start date
        
        The new start date attribute value is confirmed with a print statement returning the new start date.

        Args:
            start_date (str): The mortgage start date as a tuple '%Y-%m-%d'. ex: '2000-5-1' is May 1, 2000.
        """
        self.__start_date = start_date
    
    def get_loan_amount(self):
        """Return the loan amount (loan amount = purchase price - down payment)

        Returns:
            int: the loan amount (purchase price - down payment)
        """
        return self.__loan_amount
              
    @property
    def __payment_range(self):
        payment_range = pd.date_range(self.__start_date, periods=self.__years*self.__num_yearly_pmts, freq='MS')
        payment_range.name = 'Payment Date'
        return payment_range
    
    def get_payment_range(self):
        """Returns a DatetimeIndex of payment dates from loan start to finish.

        Returns:
            DatetimeIndex: Index of payment dates in Datetime format
        """
        return self.__payment_range
              
    def get_number_of_payments(self):
        """Returns the number of payment periods. This is equal to the number of years times the number of yearly payments.
        
        Example: A 30 year loan with monthly payments will have 360 payments.

        Returns:
            int: the number of payment periods
        """
        return self.__years * self.__num_yearly_pmts
              
    @property
    def __amortization_table(self):
        """Returns amortization table containing the loan payment schedule. The columns include:
        
        1) Payment Date
        2) Monthly payment
        3) Principal Paid at each payment
        4) Interest Paid at each payment
        5) Beginning Balance at each payment
        6) Ending Balance at each payment
        7) Cumulative Principal Paid at each payment
        8) Cumulative Interest Paid at each payment

        Returns:
            pandas.DataFrame: DataFrame containing the mortgage amortization table.
        """
        atable = pd.DataFrame(
            index=self.get_payment_range(),
            columns=['Payment', 'Principal Paid', 'Interest Paid', 'Beginning Balance', 'Ending Balance'],
            dtype=float
        )
        atable.reset_index(inplace=True)
        atable.index += 1
        atable.index.name = 'Period'
        atable['Payment'] = self.get_payment()
        atable['Principal Paid'] = -1 * npf.ppmt(self.__interest_rate/self.__num_yearly_pmts, atable.index, self.__years*self.__num_yearly_pmts, self.__loan_amount)
        atable['Interest Paid'] = -1 * npf.ipmt(self.__interest_rate/self.__num_yearly_pmts, atable.index, self.__years*self.__num_yearly_pmts, self.__loan_amount)
        atable.loc[1, 'Beginning Balance'] = self.__loan_amount
        atable.loc[1, 'Ending Balance'] = atable.loc[1, 'Beginning Balance'] - atable.loc[1, 'Principal Paid']
        for i in range(2, self.__years*self.__num_yearly_pmts + 1):
            atable.loc[i, 'Ending Balance'] = atable.loc[i - 1, 'Ending Balance'] - atable.loc[i, 'Principal Paid']
            atable.loc[i, 'Beginning Balance'] = atable.loc[i - 1, 'Ending Balance']
        atable.loc[atable.index.max(), 'Ending Balance'] = abs(atable.loc[atable.index.max(), 'Ending Balance'])
        atable['Cumulative Principal Paid'] = atable['Principal Paid'].cumsum()
        atable['Cumulative Interest Paid'] = atable['Interest Paid'].cumsum()
        return atable.round(2)
    
    def get_amortization_table(self):
        return self.__amortization_table
    
    @property
    def __payoff_date(self):
        return self.get_amortization_table().iloc[-1, 0].strftime('%m-%d-%Y')
    
    def get_payoff_date(self):
        """Returns mortgage payoff date. This is the date of the final loan payment.

        Returns:
            Datetime.date: Date of final payment
        """
        return self.__payoff_date
    
    def get_total_principal_paid(self):
        """Returns the total principal paid. This value should be equal to the loan amount.

        Returns:
            float: Total principal paid
        """
        atable = self.get_amortization_table()
        return round(atable['Cumulative Principal Paid'].iloc[-1], 2)
              
    def get_total_interest_paid(self):
        """Returns the total interest paid over the life of the loan.

        Returns:
            float: Total interest paid
        """
        atable = self.get_amortization_table()
        return round(atable['Cumulative Interest Paid'].iloc[-1], 2)
    
    def get_total_cost_of_loan(self):
        """Returns the total paid over the life of the loan and is equal to the total prinicipal plus the total interest.

        Returns:
            float: The total paid over the life of the loand
        """
        return round(self.get_total_principal_paid() + self.get_total_interest_paid(), 2)
    
    def summary_plots(self, figsize=(20,20)):
        """Returns 2x2 figure of summary plots

        Args:
            figsize (tuple, optional): Figure size (Width, Length). Defaults to (20,20).
        """
        atable = self.get_amortization_table()
        fig, axes = plt.subplots(nrows=2, ncols=2, sharex='col', figsize=figsize)
        # axes[0, 0]: cumulative plot
        ax = axes[0, 0]
        atable.plot('Payment Date', 'Cumulative Principal Paid', ax=ax)
        atable.plot('Payment Date', 'Cumulative Interest Paid', ax=ax)
        atable.plot('Payment Date', 'Ending Balance', ax=ax)
        ax.scatter(
            atable[atable['Cumulative Principal Paid'] > atable['Cumulative Interest Paid']].iloc[0, 0],
            atable[atable['Cumulative Principal Paid'] > atable['Cumulative Interest Paid']].iloc[0, -2],
            label=f"Cross-Over: \
            {atable[atable['Cumulative Principal Paid'] > atable['Cumulative Interest Paid']].iloc[0,0]: %Y-%m-%d}",
            color='black'
        )
        ytick = mtick.StrMethodFormatter('${x:,.0f}')
        ax.yaxis.set_major_formatter(ytick)
        ax.set_ylabel('Dollars')
        ax.set_ylim(0, atable['Cumulative Principal Paid'].max())
        ax.set_title('Cumulative Principal vs. Interest', fontsize=12, fontweight='bold')
        ax.legend(bbox_to_anchor=(1,1), loc='upper left', fontsize=8)
        # axes[0, 1]: Principal vs. Interest per period
        ax = axes[0, 1]
        atable.groupby(atable['Payment Date'].map(lambda x: x.year)).sum().loc[:, ['Interest Paid', 'Principal Paid']].plot.bar(stacked=True, ax=ax)
        ax.yaxis.set_major_formatter(ytick)
        ax.set_ylabel('Dollars')
        ax.set_title('Yearly principal versus interest paid', fontsize=12, fontweight='bold')
        ax.legend(bbox_to_anchor=(1,1), loc='upper left', fontsize=8)
        # axes[1, 0] : Debt to equity line plot
        ax = axes[1, 0]
        atable.plot('Payment Date', 'Ending Balance', ax=ax, label='Debt', color='red')
        atable.plot('Payment Date', 'Cumulative Principal Paid', ax=ax, label='Equity', color='green')
        ax.scatter(
            atable[atable['Cumulative Principal Paid'] > atable['Ending Balance']].iloc[0, 0],
            atable[atable['Cumulative Principal Paid'] > atable['Ending Balance']].iloc[0, -2],
            color='black',
            label=f"Cross-over: \
            {atable[atable['Cumulative Principal Paid'] > atable['Ending Balance']].iloc[0, 0]:%Y-%m-%d}"
        )
        ax.yaxis.set_major_formatter(ytick)
        ax.set_ylabel('Dollars')
        ax.set_ylim(0, atable['Cumulative Principal Paid'].max())
        ax.set_title('Debt vs. Equity', fontsize=12, fontweight='bold')
        ax.legend(bbox_to_anchor=(1,1), loc='upper left', fontsize=8)
        # axes[1, 1]: Debt to equity bar plot
        ax = axes[1, 1]
        year_end_debt = atable.groupby(atable['Payment Date'].map(lambda x: x.year)).min().loc[:, ['Payment Date', 'Ending Balance']]
        year_end_equity = atable.groupby(atable['Payment Date'].map(lambda x: x.year)).max().loc[:, ['Payment Date', 'Cumulative Principal Paid']]
        ax.bar(
            x=np.arange(year_end_debt['Payment Date'].size) - 0.2,
            height=year_end_debt['Ending Balance'],
            color='red',
            edgecolor='black',
            width=0.4,
            alpha=0.7,
            label='Debt'
        )
        ax.bar(
            x=np.arange(year_end_equity['Payment Date'].size) + 0.2,
            height=year_end_equity['Cumulative Principal Paid'],
            color='green',
            edgecolor='black',
            width=0.4,
            alpha=0.7,
            label='Equity'
        )
        ax.set_xticks(range(year_end_debt['Payment Date'].size))
        ax.set_xlim(-1, len(year_end_debt))
        ax.set_xticklabels(year_end_debt['Payment Date'].map(lambda x: x.year), rotation=45, fontsize=10)
        ax.yaxis.set_major_formatter(ytick)
        ax.set_ylabel('Dollars')
        ax.set_ylim(0, year_end_equity['Cumulative Principal Paid'].max())
        ax.set_title('Year-end Debt vs. Equity', fontsize=12, fontweight='bold')
        ax.legend(bbox_to_anchor=(1,1), loc='upper left', fontsize=8)
        plt.tight_layout(h_pad=2.2, rect=[0, 0.03, 1, 0.95])
        plt.show()
        return None    
    
    
class ExtraMonthlyPrincipal(Mortgage):
    """Subclass of Mortgage. Enables adding extra monthly principal payments to model 
    the effects of paying down principal at a quicker rate.

    Args:
        Mortgage (object): An instance of the base Mortgage class
    """
    
    def __init__(self, mortgage, extra_principal, extra_principal_start_date=None):
        """Initialize & inherit class attributes

        Args:
            mortgage (cuffnote.mortgages.Mortgage): An instance of the base Mortgage class
            extra_principal (int): The amount of extra monthly principal payment
            extra_principal_start_date (str, optional): Optional parameter to adjust starting date of extra payments. Defaults to None. Ex: '2022-1-1' for January 1, 2022.
        """
        Mortgage.__init__(
            self,
            mortgage.get_purchase_price(),
            mortgage.get_down_payment_percent(),
            mortgage.get_interest_rate(),
            mortgage.get_start_date(),
            mortgage.get_years(),
            mortgage.get_num_yearly_pmts()
        )
        self.__extra_principal = float(extra_principal)
        if extra_principal_start_date is None:
            extra_principal_start_date = super().get_start_date()
        self.__extra_principal_start_date = extra_principal_start_date
        
    def get_extra_principal(self):
        """Returns extra monthly principal attribute value

        Returns:
            float: The extra monthly principal attribute instance value
        """
        return self.__extra_principal
    
    def set_extra_principal(self, extra_principal):
        """Set or change the extra monthly principal attribute value

        Args:
            extra_principal (int): Value of extra monthly principal payment
        """
        self.__extra_principal = float(extra_principal)
    
    def get_extra_principal_start_date(self):
        """Returns the starting date of when extra monthly principal payments begin.

        Returns:
            str: String representation of extra monthly principal starting date
        """
        return self.__extra_principal_start_date
    
    def set_extra_principal_start_date(self, start_date):
        """Set the extra monthly principal payment starting date.
        
        If not set when class is initialized, the attribute value defaults to the 
        loan start date

        Args:
            start_date (str): Date to start paying extra monthly principal. Ex: '2022-1-1' for Jan. 1, 2022
        """
        self.__extra_principal_start_date = start_date
        
    @property
    def __amortization_table(self):
        atable = pd.DataFrame(
            index=self.get_payment_range(),
            columns=['Payment', 'Principal Paid', 'Interest Paid', 'Extra Principal', 'Beginning Balance', 'Ending Balance', 'Cumulative Principal Paid', 'Cumulative Interest Paid'],
            dtype=float
        )
        atable.reset_index(inplace=True)
        atable.index += 1
        atable.index.name = 'Period'
        atable['Payment'] = self.get_payment()
        atable[['Principal Paid', 'Interest Paid', 'Extra Principal', 'Beginning Balance', 'Cumulative Principal Paid', 'Cumulative Interest Paid']] = 0
        atable['Ending Balance'] = np.nan
        atable.loc[1, 'Principal Paid'] = -1 * npf.ppmt(self.get_interest_rate()/self.get_num_yearly_pmts(), atable.index, self.get_years()*self.get_num_yearly_pmts(), self.get_loan_amount())[0]
        atable.loc[1, 'Interest Paid'] = -1 * npf.ipmt(self.get_interest_rate()/self.get_num_yearly_pmts(), atable.index, self.get_years()*self.get_num_yearly_pmts(), self.get_loan_amount())[0]
        atable['Extra Principal'] = self.get_extra_principal()
        atable.loc[atable['Payment Date'] < self.get_extra_principal_start_date(), 'Extra Principal'] = float(0)
        atable.loc[1, 'Beginning Balance'] = self.get_loan_amount()
        atable.loc[1, 'Ending Balance'] = atable.loc[1, 'Beginning Balance'] - atable.loc[1, 'Principal Paid'] - atable.loc[1, 'Extra Principal']
        for i in range(2, self.get_years()*self.get_num_yearly_pmts() + 1):
            if round(atable.loc[i - 1, 'Ending Balance'], 2) > 0 and self.get_payment() >= atable.loc[i - 1, 'Ending Balance']:
                atable.loc[i, 'Payment'] = atable.loc[i - 1, 'Ending Balance'] * (1 + self.get_interest_rate() / self.get_num_yearly_pmts())
                atable.loc[i, 'Interest Paid'] = self.get_interest_rate() / self.get_num_yearly_pmts() * atable.loc[i - 1, 'Ending Balance']
                atable.loc[i, 'Principal Paid'] = atable.loc[i, 'Payment'] - atable.loc[i, 'Interest Paid']
                atable.loc[i, 'Ending Balance'] = atable.loc[i - 1, 'Ending Balance'] - atable.loc[i, 'Principal Paid']
                atable.loc[i, 'Beginning Balance'] = atable.loc[i - 1, 'Ending Balance']
                atable.loc[i, 'Extra Principal'] = 0.0
                if atable.loc[i, 'Ending Balance'].round(2) == 0:
                    break
            else:
                atable.loc[i, 'Interest Paid'] = self.get_interest_rate() / self.get_num_yearly_pmts() * atable.loc[i - 1, 'Ending Balance']
                atable.loc[i, 'Principal Paid'] = atable.loc[i, 'Payment'] - atable.loc[i, 'Interest Paid']
                atable.loc[i, 'Ending Balance'] = atable.loc[i - 1, 'Ending Balance'] - atable.loc[i, 'Principal Paid'] - atable.loc[i, 'Extra Principal']
                atable.loc[i, 'Beginning Balance'] = atable.loc[i - 1, 'Ending Balance']
        atable = atable[atable['Ending Balance'].round(2) >= 0.0]
        atable.loc[atable.index.max(), 'Ending Balance'] = abs(atable.loc[atable.index.max(), 'Ending Balance'])
        per_month_principal_paid = atable['Principal Paid'] + atable['Extra Principal']
        atable['Cumulative Principal Paid'] = per_month_principal_paid.cumsum()
        atable['Cumulative Interest Paid'] = atable['Interest Paid'].cumsum()
        return atable.round(2)
    
    def get_amortization_table(self):
        """Returns the amortization table

        Returns:
            pandas.DataFrame: Amortization table reflecting additional extra monthly principal
        """
        return self.__amortization_table
    
    @property
    def __periods_saved(self):
        return len(super().get_amortization_table().index) - len(self.get_amortization_table().index)
    
    def get_periods_saved(self):
        """Returns the difference in number of payment periods as a result of paying 
        extra monthly principal
        
        This is equal to the length of the mortgage minus the length of the mortgage with extra monthly principal.

        Returns:
            int: number of payment periods saved by paying additional principal monthly
        """
        return self.__periods_saved
    
    def get_time_saved(self):
        return f"{self.get_periods_saved() // self.get_num_yearly_pmts()} years, {self.get_periods_saved() % self.get_num_yearly_pmts()} months"


class AnnualLumpPayment(ExtraMonthlyPrincipal, Mortgage):
    """Class that inherits from both an ExtraMonthlyPrincipal instance or a Mortgage instance

    Args:
        ExtraMonthlyPrincipal (object): instance of ExtraMonthlyPrincipal class
        Mortgage (object): instance of Mortgage base class
    """
    
    def __init__(self, mortgage, annual_payment, annual_payment_month):
        """initializes instance of AnnualLumpPayment class. Enables modeling yearly one-time additional principal payments.

        Args:
            mortgage (object): An instance of either Mortgage or ExtraMonthlyPrincipal classes
            annual_payment (int): The amount of the annual additional principal payment
            annual_payment_month (int): The calendary month as an int in which the annual payment should occur. Example: 3 represents March
        """
        if not isinstance(mortgage, ExtraMonthlyPrincipal):
            # use ExtraMonthlyPrincipal constructor with extra principal set to 0
            ExtraMonthlyPrincipal.__init__(
                self,
                mortgage,
                extra_principal=0,
                extra_principal_start_date=None
            )
        else:
            ExtraMonthlyPrincipal.__init__(
                self,
                mortgage,
                mortgage.get_extra_principal(),
                mortgage.get_extra_principal_start_date()
            )
        self.__annual_payment = annual_payment
        self.__annual_payment_month = annual_payment_month
        
    def get_annual_payment(self):
        """returns annual payment amount

        Returns:
            int: annual payment amount
        """
        return self.__annual_payment
    
    def set_annual_payment(self, annual_payment):
        """Set the annual payent amount. Doing so will update the amortization table.

        Args:
            annual_payment (int): New value of annual additional principal payment
        """
        self.__annual_payment = annual_payment
        
    def get_annual_payment_month(self):
        """Returns the month in which the annual payment occurs

        Returns:
            int: Integer representation of the calendar month when the annual payment occurs
        """
        return self.__annual_payment_month
    
    def set_annual_payment_month(self, month):
        """Set the annual payment month. Doing so will update the amortization table.

        Args:
            month (int): Integer representation of the calendar month when the annual payment occurs. Ex: 3 represents March
        """
        self.__annual_payment_month = month
        
    @property
    def __amortization_table(self):
        atable = pd.DataFrame(
            index=self.get_payment_range(),
            columns=['Payment', 'Principal Paid', 'Interest Paid', 'Extra Principal', 'Beginning Balance', 'Ending Balance', 'Cumulative Principal Paid', 'Cumulative Interest Paid'],
            dtype=float
        )
        atable.reset_index(inplace=True)
        atable.index += 1
        atable.index.name = 'Period'
        atable['Payment'] = self.get_payment()
        atable[['Principal Paid', 'Interest Paid', 'Extra Principal', 'Beginning Balance', 'Cumulative Principal Paid', 'Cumulative Interest Paid']] = 0
        atable['Ending Balance'] = np.nan
        atable.loc[1, 'Principal Paid'] = -1 * npf.ppmt(self.get_interest_rate()/self.get_num_yearly_pmts(), atable.index, self.get_years()*self.get_num_yearly_pmts(), self.get_loan_amount())[0]
        atable.loc[1, 'Interest Paid'] = -1 * npf.ipmt(self.get_interest_rate()/self.get_num_yearly_pmts(), atable.index, self.get_years()*self.get_num_yearly_pmts(), self.get_loan_amount())[0]
        atable['Extra Principal'] = self.get_extra_principal()
        atable.loc[atable['Payment Date'] < self.get_extra_principal_start_date(), 'Extra Principal'] = float(0)
        atable.loc[atable['Payment Date'].dt.month == self.get_annual_payment_month(), 'Extra Principal'] += self.get_annual_payment()
        atable.loc[1, 'Beginning Balance'] = self.get_loan_amount()
        atable.loc[1, 'Ending Balance'] = atable.loc[1, 'Beginning Balance'] - atable.loc[1, 'Principal Paid'] - atable.loc[1, 'Extra Principal']
        for i in range(2, self.get_years()*self.get_num_yearly_pmts() + 1):
            if atable.loc[i - 1, 'Ending Balance'].round(2) < atable.loc[i, 'Extra Principal']:
                atable.loc[i, 'Extra Principal'] -= self.get_annual_payment()
            if round(atable.loc[i - 1, 'Ending Balance'], 2) > 0 and self.get_payment() >= atable.loc[i - 1, 'Ending Balance']:
                atable.loc[i, 'Payment'] = atable.loc[i - 1, 'Ending Balance'] * (1 + self.get_interest_rate() / self.get_num_yearly_pmts())
                atable.loc[i, 'Interest Paid'] = self.get_interest_rate() / self.get_num_yearly_pmts() * atable.loc[i - 1, 'Ending Balance']
                atable.loc[i, 'Principal Paid'] = atable.loc[i, 'Payment'] - atable.loc[i, 'Interest Paid']
                atable.loc[i, 'Ending Balance'] = atable.loc[i - 1, 'Ending Balance'] - atable.loc[i, 'Principal Paid']
                atable.loc[i, 'Beginning Balance'] = atable.loc[i - 1, 'Ending Balance']
                atable.loc[i, 'Extra Principal'] = 0.0
                if atable.loc[i, 'Ending Balance'].round(2) == 0:
                    break
            else:
                atable.loc[i, 'Interest Paid'] = self.get_interest_rate() / self.get_num_yearly_pmts() * atable.loc[i - 1, 'Ending Balance']
                atable.loc[i, 'Principal Paid'] = atable.loc[i, 'Payment'] - atable.loc[i, 'Interest Paid']
                atable.loc[i, 'Ending Balance'] = atable.loc[i - 1, 'Ending Balance'] - atable.loc[i, 'Principal Paid'] - atable.loc[i, 'Extra Principal']
                atable.loc[i, 'Beginning Balance'] = atable.loc[i - 1, 'Ending Balance']
        atable = atable[atable['Ending Balance'].round(2) >= 0.0]
        atable.loc[atable.index.max(), 'Ending Balance'] = abs(atable.loc[atable.index.max(), 'Ending Balance'])
        per_month_principal_paid = atable['Principal Paid'] + atable['Extra Principal']
        atable['Cumulative Principal Paid'] = per_month_principal_paid.cumsum()
        atable['Cumulative Interest Paid'] = atable['Interest Paid'].cumsum()
        return atable.round(2)
    
    def get_amortization_table(self):
        """returns the amortization table

        Returns:
            pandas.DataFrame: Pandas DataFrame containing the amortization table
        """
        return self.__amortization_table
