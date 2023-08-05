"""
While a grid availability time series contains at each interval information of the charging stations available, 
such as the maximum power rating allocated to them, a grid electricity demand time series is the one that indicates 
the actual consumption of electricity from the grid to charge the battery of a vehicle according to its driving needs 
and grid availability. There are different options available to create a grid electricity demand time series. For example, 
"Immediate-Full capacity" is an option that informs the energy drawn from the grid at a maximum power rating of a respective 
charging station until the battery is fully charged or "Immediate-Balanced" option that creates a time series taking into account 
the duration of a vehicle is connected to a charging station and the energy required to get the battery fully charged, allowing to 
charge the battery at a lower capacity than the maximum capacity available.

For more details see the article and cite:

.. code-block:: python

    @article{Gaete-Morales_2021,
    author={Gaete-Morales, Carlos and Kramer, Hendrik and Schill, Wolf-Peter and Zerrahn, Alexander},
    title={An open tool for creating battery-electric vehicle time series from empirical data, emobpy},
    journal={Scientific Data}, year={2021}, month={Jun}, day={11}, volume={8}, number={1}, pages={152},
    issn={2052-4463}, doi={10.1038/s41597-021-00932-9}, url={https://doi.org/10.1038/s41597-021-00932-9}}

See also the examples in the documentation https://diw-evu.gitlab.io/emobpy/emobpy

"""

import pandas as pd
import numpy as np
import uuid
import os
import pickle
import gzip
from numba import jit
from .tools import check_for_new_function_name


def represents_int(s):
    """
    Check if argument is an int value.

    Args:
        s (any type): Value to check.

    Returns:
        bool: True if the argument is an int value.
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


@jit(nopython=True)
def is_between(t, time_range):
    """
    Checks if given value is between given time_range.

    Args:
        t (float): Value to check. 
        time_range (list): Time range list. E.g. [1,100].

    Returns:
        bool: Value if t is between time_range.
    """
    if time_range[1] < time_range[0]:
        return t >= time_range[0] or t <= time_range[1]
    return time_range[0] <= t <= time_range[1]


def add_column_datetime(df, totalrows, reference_date, t):
    """
    Useful to convert the time series from hours index to datetime index.

    Args:
        df (pd.DataFrame): Table on which datetime column should be added.
        totalrows (int): Number of rows on which datetime column should be added.
        reference_date (str): Starting date for adding. E.g. '01/01/2020'.
        t (float): Float frequency, will be changed to string.

    Returns:
        pd.DataFrame: Table with added datetime column.
    """
    fr = {1: 'H', 0.5: '30min', 0.25: '15min', 0.125: '450s'}
    freq = fr[t]
    start_date = pd.to_datetime(reference_date)
    drange = pd.date_range(start_date, periods=totalrows, freq=freq)
    df = pd.DataFrame(df.values, columns=df.columns, index=drange)
    df = df.rename_axis('date').copy()
    return df


class Charging:
    """
    Args:
        self.__init__(input)
            input: string. File name of the input profile (not the path).
            The input should be in this case a grid availability profile name.

            Methods in the following order:

            - self.loadScenario(DataBase)
            - self.setSubScenario(option)
            - self.run()
            - self.save_profile(folder, description=' ')
    """

    def __init__(self, inpt):
        self.kind = 'charging'
        self.input = inpt
        self.change_battery_cap = False  # in case the battery capacity has been changed and then it differs from
        # availability profile
        self.pointmissing = False  # in case of sub scenario A2BatpPoint is selected
        self.success = False

    def __getattr__(self, item):
        check_for_new_function_name(item)
        # if the return value is not callable, we get TypeError:

    def load_scenario(self, database):
        """
        Loads scenario data from given database into object.

        Args:
            database (DataBase()): E.g. manager = DataBase(). "manager" is a class instance that contains the profiles.

        Raises:
            ValueError: Raised if charging profile can not be found in the database.
        """
        if database.db[self.input]:
            if database.db[self.input]['kind'] == 'availability':
                self.profile = database.db[self.input]['profile'].copy()
                self.capacity_charging_point = database.db[self.input]['chargingdata']['capacity_charging_point']
                self.points = list(self.capacity_charging_point.keys())
                self.states = list(set(self.profile.loc[:, 'state']))
                self.battery_capacity = database.db[self.input]['battery_capacity']
                self.charging_eff = database.db[self.input]['charging_eff']
                self.soc_init = database.db[self.input]['soc_init']
                self.soc_min = database.db[self.input]['soc_min']
                self.t = database.db[self.input]['t']
                self.totalrows = database.db[self.input]['totalrows']
                self.refdate = database.db[self.input]['refdate']
            else:
                raise ValueError(
                    'The charging availability profile {} can not be found in the database'.format(self.input))
        else:
            raise ValueError('The charging availability profile {} can not be found in the database'.format(self.input))

    def set_sub_scenario(self, option):
        """
        Sets sub scenario in self.option.

        Args:
            option (str): 'immediate',  'balanced' or  'from_22_to_6_at_home'.
        """
        self.option = option

    def run(self):
        """
        No input required.
        Once it finishes the following attributes can be called.

        Attributes:

        - kind
        - input
        - change_battery_cap
        - pointmissing
        - success
        - option
        - profile
        - timeseries
        - name
        """
        self.name = self.input + '_' + self.option + '_' + uuid.uuid4().hex[0:5]
        # print(self.name, '    ->    ', self.input)
        if self.option == 'immediate':
            self.point = 'driving'
            try:
                self.pointcode = self.states.index(self.point)
            except ValueError:
                self.pointmissing = True
                self.success = False
                print('"{}" is not in "{}". Availability profile: {}'.format(self.point, ' - '.join(self.states), self.input))
                self._clean()
                return None
            self.numpy_array3 = self.profile[['state']].values.T
            self.arraystringstate = self.numpy_array3[0]
            self.arraycodestate = np.array([self.states.index(s) for s in self.arraystringstate])
            self.numpy_array2 = self.profile[['consumption', 'charging_cap']].values.T
            self.results = self._immediate(self.pointcode, self.charging_eff, self.battery_capacity, self.soc_init,
                                           self.arraycodestate, *self.numpy_array2, self.t)
            self.profile.loc[:, 'actual_soc'] = self.results[0]
            self.profile.loc[:, 'charge_battery'] = self.results[1]
            self.profile.loc[:, 'charge_grid'] = self.results[2]
        elif self.option == 'balanced':
            self.point = 'driving'
            try:
                self.pointcode = self.states.index(self.point)
            except ValueError:
                self.pointmissing = True
                self.success = False
                print('"{}" is not in "{}". Availability profile: {}'.format(self.point, ' - '.join(self.states), self.input))
                self._clean()
                return None
            self.numpy_array3 = self.profile[['state', 'consumption', 'charging_cap']].values.T
            self.arraystringstate = self.numpy_array3[0]
            self.arraycodestate = np.array([self.states.index(s) for s in self.arraystringstate])
            self.arrayconsumption = self.numpy_array3[1].astype(np.float64)
            self.arraychargingcap = self.numpy_array3[2].astype(np.float64)
            self.results = self._balanced(self.pointcode, self.charging_eff, self.battery_capacity, self.soc_init,
                                            self.arraycodestate, self.arrayconsumption, self.arraychargingcap, self.t)
            self.profile.loc[:, 'actual_soc'] = self.results[0]
            self.profile.loc[:, 'charge_battery'] = self.results[1]
            self.profile.loc[:, 'charge_grid'] = self.results[2]
        elif set(['from', 'to', 'at']).issubset(self.option.split('_')):  # eg. 'from_22_to_6_at_home'
            self.op_list = [int(s) if represents_int(s) else s for s in self.option.split('_')]
            self.from_ = self.op_list[1]
            self.to_ = self.op_list[3]
            self.point = self.op_list[5]

            self.numpy_array4 = self.profile[['state', 'consumption', 'charging_cap', 'hh']].values.T
            self.arraystringstate = self.numpy_array4[0]
            self.arraycodestate = np.array([self.states.index(s) for s in self.arraystringstate])
            try:
                self.drivingcode = self.states.index('driving')
                if self.point == 'any':
                    self.pointcode = -1
                else:
                    self.pointcode = self.states.index(self.point)
            except ValueError:
                self.pointmissing = True
                self.success = False
                print('Charging point "{}" is not in "{}". Availability profile: {}'.format(self.point,
                                                                                            ' - '.join(self.states),
                                                                                            self.input))
                self._clean()
                return None
            self.arrayconsumption = self.numpy_array4[1].astype(np.float64)
            self.arraychargingcap = self.numpy_array4[2].astype(np.float64)
            self.hh = self.numpy_array4[3].astype(np.float64)
            self.results = self._A2BatPoint(self.from_,
                                            self.to_,
                                            self.pointcode,
                                            self.drivingcode,
                                            self.charging_eff,
                                            self.battery_capacity,
                                            self.soc_init,
                                            self.arraycodestate,
                                            self.arrayconsumption,
                                            self.arraychargingcap,
                                            self.hh,
                                            self.t)
            self.profile.loc[:, 'actual_soc'] = self.results[0]
            self.profile.loc[:, 'charge_battery'] = self.results[1]
            self.profile.loc[:, 'charge_grid'] = self.results[2]
            self.profile.loc[:, 'omit'] = self.results[3]
        else:
            raise ValueError('Select a valid option')
        self._check_success()
        self.timeseries = add_column_datetime(self.profile.copy(), self.totalrows, self.refdate, self.t)
        self.timeseries = self.timeseries[["hh","state","distance","consumption","charging_point","charging_cap","actual_soc","charge_battery","charge_grid"]]
        if not self.success:
            self.name += '_FAIL'
        self._clean()
        print('Profile done: ' + self.name)
        return None

    @staticmethod
    @jit(nopython=True)
    def _immediate(driving_code, charging_eff, battery_capacity, soc_init, state, consumption, charging_cap, t):
        """
        #TODO DOCSTRING

        Args:
            driving_code ([type]): [description]
            charging_eff ([type]): [description]
            battery_capacity ([type]): [description]
            soc_init ([type]): [description]
            state ([type]): [description]
            consumption ([type]): [description]
            charging_cap ([type]): [description]
            t ([type]): [description]

        Returns:
            [type]: [description]
        """
        soc = np.empty(consumption.shape)
        battery = np.empty(consumption.shape)
        grid = np.empty(consumption.shape)
        rows = soc.shape[0]
        for i in range(rows):
            if i == 0:
                zero = soc_init
                current_soc = zero - consumption[i] / battery_capacity + charging_cap[
                    i] * t * charging_eff / battery_capacity
                if current_soc > 1:
                    soc[i] = 1
                    battery[i] = (charging_cap[i] * t * charging_eff - (current_soc - 1) * battery_capacity) / t
                    grid[i] = (charging_cap[i] * t - (current_soc - 1) * battery_capacity / charging_eff) / t
                else:
                    soc[i] = current_soc
                    battery[i] = (charging_cap[i] * t * charging_eff) / t
                    grid[i] = (charging_cap[i] * t) / t
            else:
                zero = soc[i - 1]
                if state[i] == driving_code:
                    if zero == 1:
                        current_soc = zero - consumption[i] / battery_capacity
                        soc[i] = current_soc
                        battery[i] = 0
                        grid[i] = 0
                    else:
                        current_soc = zero - consumption[i] / battery_capacity + charging_cap[
                            i] * t * charging_eff / battery_capacity
                        if current_soc > 1:
                            soc[i] = 1
                            battery[i] = (charging_cap[i] * t * charging_eff - (current_soc - 1) * battery_capacity) / t
                            grid[i] = (charging_cap[i] * t - (current_soc - 1) * battery_capacity / charging_eff) / t
                        else:
                            soc[i] = current_soc
                            battery[i] = (charging_cap[i] * t * charging_eff) / t
                            grid[i] = (charging_cap[i] * t) / t  # I did not want to cancel t, just for code consistency
                else:
                    current_soc = zero - consumption[i] / battery_capacity + charging_cap[
                        i] * t * charging_eff / battery_capacity
                    if current_soc > 1:
                        soc[i] = 1
                        battery[i] = (charging_cap[i]*t*charging_eff - (current_soc-1)*battery_capacity)/t
                        grid[i] = (charging_cap[i] * t - (current_soc - 1) * battery_capacity / charging_eff) / t
                    else:
                        soc[i] = current_soc
                        battery[i] = (charging_cap[i]*t*charging_eff)/t
                        grid[i] = (charging_cap[i] * t) / t
        return [soc, battery, grid]

    @staticmethod
    @jit(nopython=True)
    def _balanced(driving_code, charging_eff, battery_capacity, soc_init, state, consumption, charging_cap, t):
        """
        #TODO DOCSTRING

        Args:
            driving_code ([type]): [description]
            charging_eff ([type]): [description]
            battery_capacity ([type]): [description]
            soc_init ([type]): [description]
            state ([type]): [description]
            consumption ([type]): [description]
            charging_cap ([type]): [description]
            t ([type]): [description]

        Returns:
            [type]: [description]
        """
        soc = np.empty(consumption.shape)
        battery = np.empty(consumption.shape)
        grid = np.empty(consumption.shape)
        soc_ahead = np.empty(consumption.shape)
        rows = soc.shape[0]
        i = 0
        while i < rows:
            if i == 0:
                zero = soc_init
            else:
                zero = soc[i - 1]
            if state[i] == driving_code:
                if zero == 1:
                    current_soc = zero - consumption[i] / battery_capacity
                    soc[i] = current_soc
                    battery[i] = 0
                    grid[i] = 0
                else:
                    current_soc = zero - consumption[i] / battery_capacity + charging_cap[
                        i] * t * charging_eff / battery_capacity
                    if current_soc > 1:
                        soc[i] = 1
                        battery[i] = (charging_cap[i]*t*charging_eff - (current_soc-1)*battery_capacity)/t
                        grid[i] = (charging_cap[i] * t - (current_soc - 1) * battery_capacity / charging_eff) / t
                    else:
                        soc[i] = current_soc
                        battery[i] = (charging_cap[i]*t*charging_eff)/t
                        grid[i] = (charging_cap[i] * t) / t  # I did not want to cancel t, just for code consistency
            else:
                if charging_cap[i] * t > 0:
                    j = i
                    cero = zero
                    while state[j] == state[i]:
                        current_soc = cero - consumption[j] / battery_capacity + charging_cap[
                            j] * t * charging_eff / battery_capacity
                        if current_soc > 1:
                            soc_ahead[j] = 1
                        else:
                            soc_ahead[j] = current_soc
                        j += 1
                        cero = current_soc
                    k = j - i  # length in the same state, this will help to jump the queue
                    if np.any(soc_ahead[i:j] == 1):
                        soc_diff = 1 - zero
                        delta_charging = soc_diff * battery_capacity / charging_eff / k
                        cero = zero
                        for m in range(i, j):
                            current_soc = cero - consumption[
                                m] / battery_capacity + delta_charging * charging_eff / battery_capacity
                            if current_soc > 1:
                                soc[m] = 1
                                battery[m] = (delta_charging*charging_eff - (current_soc-1)*battery_capacity)/t
                                grid[m] = (delta_charging - (current_soc - 1) * battery_capacity / charging_eff) / t
                            else:
                                soc[m] = current_soc
                                battery[m] = (delta_charging*charging_eff)/t
                                grid[m] = delta_charging / t
                            cero = current_soc
                        i = m
                    else:
                        cero = zero
                        for m in range(i, j):
                            current_soc = cero - consumption[m] / battery_capacity + charging_cap[
                                m] * t * charging_eff / battery_capacity
                            if current_soc > 1:
                                soc[m] = 1
                                battery[m] = (charging_cap[m]*t*charging_eff - (current_soc-1)*battery_capacity)/t
                                grid[m] = (charging_cap[m] * t - (
                                            current_soc - 1) * battery_capacity / charging_eff) / t
                            else:
                                soc[m] = current_soc
                                battery[m] = (charging_cap[m]*t*charging_eff)/t
                                grid[m] = (charging_cap[m] * t) / t
                            cero = current_soc
                        i = m
                else:  # if charging capacity is zero
                    current_soc = zero
                    soc[i] = current_soc
                    battery[i] = 0
                    grid[i] = 0
            i += 1
        return [soc, battery, grid]

    @staticmethod
    @jit(nopython=True)
    def _A2BatPoint(from_, to_, point, driving_code, charging_eff, battery_capacity, soc_init, state, consumption,
                    charging_cap, hr, t):
        """
        #TODO DOCSTRING

        Args:
            from_ ([type]): [description]
            to_ ([type]): [description]
            point ([type]): [description]
            driving_code ([type]): [description]
            charging_eff ([type]): [description]
            battery_capacity ([type]): [description]
            soc_init ([type]): [description]
            state ([type]): [description]
            consumption ([type]): [description]
            charging_cap ([type]): [description]
            hr ([type]): [description]
            t ([type]): [description]

        Returns:
            [type]: [description]
        """
        debug = False
        ante = 0
        count = 0
        if debug:
            print('driving:', driving_code)
            print('point:', point)
        soc = np.empty(consumption.shape)
        battery = np.empty(consumption.shape)
        grid = np.empty(consumption.shape)
        soc_ahead = np.empty(consumption.shape)
        preferenceignore = np.zeros(consumption.shape)
        rows = soc.shape[0]
        i = 0
        while i < rows:  # code 1
            # start with a little code for avoid endless loop
            if ante == i:
                count += 1
            else:
                count = 0
            if count == 10:
                print('The simulation has reached an endless loop')
                raise
            ante = i
            # end little code
            # now starts function

            if i == 0:
                zero = soc_init
            else:
                zero = soc[i - 1]
            if (state[i] == point) | (preferenceignore[i] == 1) | (state[i] == driving_code) | (point == -1):
                if debug:
                    print(i, 'A', state[i], zero, 'pref', preferenceignore[i])
                if (is_between(np.mod(hr[i], 24), (from_, to_))) | (preferenceignore[i] == 1) | (
                        state[i] == driving_code):
                    if debug:
                        print('    AA')
                    if state[i] == driving_code:
                        if debug:
                            print('      driving')
                        # if zero == 1:
                        #     current_soc = zero - consumption[i]/battery_capacity
                        #     soc[i] = current_soc
                        #     battery[i] = 0
                        #     grid[i] = 0
                        # else:
                        current_soc = zero - consumption[i] / battery_capacity + charging_cap[
                            i] * t * charging_eff / battery_capacity
                        if current_soc > 1:
                            soc[i] = 1
                            battery[i] = (charging_cap[i]*t*charging_eff - (current_soc-1)*battery_capacity)/t
                            grid[i] = (charging_cap[i] * t - (current_soc - 1) * battery_capacity / charging_eff) / t
                        else:
                            soc[i] = current_soc
                            battery[i] = (charging_cap[i]*t*charging_eff)/t
                            grid[i] = (charging_cap[i] * t) / t  # I did not want to cancel t, just for code consistency
                    else:
                        if debug:
                            print('      NO driving')
                        if zero < 0:
                            if debug:
                                print('      yes negative')
                            n = i - 1
                            gap = (zero - 0.05) * battery_capacity
                            while gap < 1.5:  # 1.5 kWh
                                n -= 1
                                if state[n] == driving_code:
                                    gap = gap - consumption[n] + charging_cap[n] * t * charging_eff * 0.5
                                else:
                                    gap = gap - consumption[n] + charging_cap[n] * t * charging_eff
                                if n < 1:
                                    print(
                                        'The simulation has reached the starting step. Change options to a more '
                                        'flexible one')
                                    break
                                if debug:
                                    print(n, gap)
                            p = n
                            while state[p] == state[n]:  # code 4
                                p -= 1
                                if p < 0:
                                    break  # p=-1
                            if debug:
                                print('p', p, 'i', i, 'socp', soc[p])
                            for idx in range(p + 1, i):
                                preferenceignore[idx] = 1
                            i = p + 1
                            continue
                        else:
                            j = i
                            cero = zero
                            while state[j] == state[i]:  # code 2
                                current_soc = cero - consumption[j] / battery_capacity + charging_cap[
                                    j] * t * charging_eff / battery_capacity
                                if current_soc > 1:
                                    soc_ahead[j] = 1
                                else:
                                    soc_ahead[j] = current_soc
                                j += 1
                                cero = current_soc
                            k = j - i  # length in the same state, this will help to jump the queue
                            if np.any(soc_ahead[i:j] == 1):
                                if debug:
                                    print('      ANY in state: soc of 1')
                                soc_diff = 1 - zero
                                delta_charging = soc_diff * battery_capacity / charging_eff / k
                                cero = zero
                                for m in range(i, j):
                                    current_soc = cero - consumption[
                                        m] / battery_capacity + delta_charging * charging_eff / battery_capacity
                                    if current_soc > 1:
                                        soc[m] = 1
                                        battery[m] = (delta_charging * charging_eff - (
                                                    current_soc - 1) * battery_capacity) / t
                                        grid[m] = (delta_charging - (
                                                    current_soc - 1) * battery_capacity / charging_eff) / t
                                    else:
                                        soc[m] = current_soc
                                        battery[m] = (delta_charging*charging_eff)/t
                                        grid[m] = delta_charging / t
                                    cero = current_soc
                                i = m
                            else:
                                if debug:
                                    print('      NO in state: soc of 1')
                                cero = zero
                                for m in range(i, j):
                                    current_soc = cero - consumption[m] / battery_capacity + charging_cap[
                                        m] * t * charging_eff / battery_capacity
                                    if current_soc > 1:
                                        soc[m] = 1
                                        battery[m] = (charging_cap[m]*t*charging_eff - (current_soc-1)*battery_capacity)/t
                                        grid[m] = (charging_cap[m] * t - (
                                                    current_soc - 1) * battery_capacity / charging_eff) / t
                                    else:
                                        soc[m] = current_soc
                                        battery[m] = (charging_cap[m]*t*charging_eff)/t
                                        grid[m] = (charging_cap[m] * t) / t
                                    cero = current_soc
                                i = m
                else:
                    if debug:
                        print('AB')
                    current_soc = zero
                    soc[i] = current_soc
                    battery[i] = 0
                    grid[i] = 0
            else:
                if debug:
                    print(i, 'B', state[i], zero, 'pref', preferenceignore[i])
                current_soc = zero
                soc[i] = current_soc
                battery[i] = 0
                grid[i] = 0
            i += 1
        return [soc, battery, grid, preferenceignore]

    # @staticmethod
    # @jit(nopython=True)
    # def A2BatPoint_old(from_, to_, point, driving_code, charging_eff, battery_capacity, soc_init, state, consumption,
    #                    charging_cap, hr, t):
    #     """
    #
    #
    #     Args:
    #         from_ ([type]): [description]
    #         to_ ([type]): [description]
    #         point ([type]): [description]
    #         driving_code ([type]): [description]
    #         charging_eff ([type]): [description]
    #         battery_capacity ([type]): [description]
    #         soc_init ([type]): [description]
    #         state ([type]): [description]
    #         consumption ([type]): [description]
    #         charging_cap ([type]): [description]
    #         hr ([type]): [description]
    #         t ([type]): [description]
    #
    #     Returns:
    #         [type]: [description]
    #     """
    #     print(point)
    #     print(driving_code)
    #     soc = np.empty(consumption.shape)
    #     battery = np.empty(consumption.shape)
    #     grid = np.empty(consumption.shape)
    #     soc_ahead = np.empty(consumption.shape)
    #     preferenceignore = np.zeros(consumption.shape)
    #     rows = soc.shape[0]
    #     i = 0
    #     while i < rows:  # code 1
    #         if i == 0:
    #             zero = soc_init
    #         else:
    #             zero = soc[i - 1]
    #         if state[i] == driving_code:
    #             print(i, 'd', zero, preferenceignore[i])
    #             if zero == 1:
    #                 current_soc = zero - consumption[i] / battery_capacity
    #                 soc[i] = current_soc
    #                 battery[i] = 0
    #                 grid[i] = 0
    #             else:
    #                 current_soc = zero - consumption[i] / battery_capacity + charging_cap[
    #                     i] * t * charging_eff / battery_capacity
    #                 if current_soc > 1:
    #                     soc[i] = 1
    #                     battery[i] = charging_cap[i] * t * charging_eff - (current_soc - 1) * battery_capacity
    #                     grid[i] = (charging_cap[i] * t - (current_soc - 1) * battery_capacity / charging_eff) / t
    #                 else:
    #                     soc[i] = current_soc
    #                     battery[i] = charging_cap[i] * t * charging_eff
    #                     grid[i] = (charging_cap[i] * t) / t  # I did not want to cancel t, just for code consistency
    #         elif (state[i] == point) | (preferenceignore[i] == 1) | (point == -1):
    #             print(i, state[i], zero, preferenceignore[i])
    #             if (is_between(np.mod(hr[i], 24), (from_, to_))) | (preferenceignore[i] == 1):
    #                 j = i
    #                 cero = zero
    #                 negative = False
    #                 while state[j] == state[i]:  # code 2
    #                     current_soc = cero - consumption[j] / battery_capacity + charging_cap[
    #                         j] * t * charging_eff / battery_capacity
    #                     if current_soc <= 0:
    #                         negative = i  # index when negative while driving
    #                     if current_soc > 1:
    #                         soc_ahead[j] = 1
    #                     else:
    #                         soc_ahead[j] = current_soc
    #                     j += 1
    #                     cero = current_soc
    #                 if negative:
    #                     cap = 0.01 + zero - current_soc
    #                     n = i
    #                     imagsoc = 0
    #                     while cap > imagsoc:  # code 3
    #                         n -= 1
    #                         imagsoc += charging_cap[n] * t * charging_eff / battery_capacity
    #                         cap += consumption[n] / battery_capacity
    #                     p = n
    #                     while state[p] == state[n]:  # code 4
    #                         p -= 1
    #                         if p < 0:
    #                             break  # p=-1
    #                     for idx in range(p + 1, negative):
    #                         preferenceignore[idx] = 1
    #                     i = p + 1
    #                     continue
    #                 k = j - i  # length in the same state, this will help to jump the queue
    #                 if np.any(soc_ahead[i:j] == 1):
    #                     soc_diff = 1 - zero
    #                     delta_charging = soc_diff * battery_capacity / charging_eff / k
    #                     cero = zero
    #                     for m in range(i, j):
    #                         current_soc = cero - consumption[
    #                             m] / battery_capacity + delta_charging * charging_eff / battery_capacity
    #                         if current_soc > 1:
    #                             soc[m] = 1
    #                             battery[m] = delta_charging * charging_eff - (current_soc - 1) * battery_capacity
    #                             grid[m] = (delta_charging - (current_soc - 1) * battery_capacity / charging_eff) / t
    #                         else:
    #                             soc[m] = current_soc
    #                             battery[m] = delta_charging * charging_eff
    #                             grid[m] = delta_charging / t
    #                         cero = current_soc
    #                     i = m
    #                 else:
    #                     cero = zero
    #                     for m in range(i, j):
    #                         current_soc = cero - consumption[m] / battery_capacity + charging_cap[
    #                             m] * t * charging_eff / battery_capacity
    #                         if current_soc > 1:
    #                             soc[m] = 1
    #                             battery[m] = charging_cap[m] * t * charging_eff - (current_soc - 1) * battery_capacity
    #                             grid[m] = (charging_cap[m] * t - (
    #                                         current_soc - 1) * battery_capacity / charging_eff) / t
    #                         else:
    #                             soc[m] = current_soc
    #                             battery[m] = charging_cap[m] * t * charging_eff
    #                             grid[m] = (charging_cap[m] * t) / t
    #                         cero = current_soc
    #                     i = m
    #             else:
    #                 current_soc = zero - consumption[i] / battery_capacity
    #                 soc[i] = current_soc
    #                 battery[i] = 0
    #                 grid[i] = 0
    #         else:
    #             print(i, 'else', zero, preferenceignore[i])
    #             current_soc = zero - consumption[i] / battery_capacity
    #             soc[i] = current_soc
    #             battery[i] = 0
    #             grid[i] = 0
    #         i += 1
    #     return [soc, battery, grid, preferenceignore]

    def _check_success(self):
        """
        Check and set success in self.success. The actual_soc minimum must be higher than the self.soc_min.
        """
        if self.profile['actual_soc'].min() >= self.soc_min:
            cons_t = round(self.profile['consumption'].sum(), 2)
            chrg_t = round(self.profile['charge_battery'].sum()*self.t, 2)
            sto_i = round(self.battery_capacity * self.soc_init, 2)
            sto_e = round(self.battery_capacity * self.profile['actual_soc'].values[-1], 2)
            bal_t = round(sto_i + chrg_t - cons_t - sto_e, 2)
            if bal_t != 0.0:
                print('Balance:', bal_t, '   Consumption:', cons_t, 'charge_battery:', chrg_t, 'sto_init:', sto_i,
                      'sto_end:', sto_e)
            self.success = True
        else:
            self.success = False

    # def change_battery_capacity(self, new_capacity):
    #     """
    #
    #
    #     Args:
    #         new_capacity ([type]): [description]
    #     """
    #     self.change_battery_cap = True
    #     self.battery_capacity = new_capacity

    def _clean(self):
        """
        Deletes all attributes of object which are not in keep_attr.
        """
        to_rem = list(self.__dict__.keys())[:]
        keep_attr = [
            'kind',
            'input',
            'change_battery_cap',
            'pointmissing',
            'success',
            'option',
            'profile',
            'timeseries',
            'name'
        ]
        for r in keep_attr:
            if r in to_rem:
                to_rem.remove(r)
        for attr in to_rem:
            self.__dict__.pop(attr, None)
        del to_rem

    def save_profile(self, folder, description=' '):
        """
        Saves object profile as a pickle file.

        Args:
            folder (str): Where the files will be stored. Folder is created in case it does not exist.
            description (str, optional): Description which can be saved in object attribute. Defaults to " ".
        """
        self.description = description
        info = self.__dict__
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, self.name + '.pickle')
        with gzip.open(filepath, 'wb') as file:
            pickle.dump(info, file)
        del info
        print('File saved : ' + filepath)
        return None
