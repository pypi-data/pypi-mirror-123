"""
This module contains a tool functions used to create a new project.
"""

from multiprocessing import Lock, Process, Queue, Manager, cpu_count
import numpy as np
import random
import numba

class Unit:
    """
    This class represents a unit. In this way a value and a unit can be saved and with class methods the unit
    can easily be changed. The default value used by the programme is always the 1 value in unit_scale.
    """

    def __init__(self, val, unit, description = "No description given."):
        self.val = val
        self.unit = unit
        self.description = description

    def convert_to(self, new_unit, msg=False):

        def change_unit(self, new_unit, msg):
            unit_scale = {'time': {'h': 1 / 3600, 'min': 1 / 60, 's': 1},
                          'velocity': {'km/h': 1, 'km/min': 1 / 60, 'km/s': 1 / 3600, 'm/h': 1000, 'm/min': 1000 / 60,
                                       'm/s': 1000 / 3600},
                          'energy': {'kWh': 1, 'Wh': 1000},
                          'power': {'kW': 1, 'W': 1000},
                          'voltage': {'V': 1, 'kW': 1 / 1000},
                          'distance': {'km': 1/1000, 'm': 1, 'cm': 100},
                          'weight': {'kg': 1, 'g': 1000, 't': 1 / 1000},
                          'volume': {'m3': 1},
                          'area': {'m2': 1}
                          }

            # Get correct scale for unit
            found = False
            for key, value in unit_scale.items():
                if self.unit in value:
                    found = True
                    scale = value
                    break
            if not found:
                return

            # Check if new_unit could not be loaded in scale
            if new_unit not in scale:
                if msg:
                    print('The given unit is not known and can not be converted.')
                return

            conversion_value = scale[self.unit]
            # Change value and unit
            for key, value in scale.items():
                scale[key] = value / conversion_value

            if msg:
                print(f'Unit of value changed: {self.val} {self.unit} -> {self.val * scale[new_unit]} {new_unit}')
            self.val *= scale[new_unit]
            self.unit = new_unit

            return self

        # Check if value is None
        if not self.val:
            if msg:
                print('Unit could not be converted because value is None.')
            return


        change_unit(self, new_unit=new_unit, msg=msg)

        return self

    def convert_to_default_value(self):
        self.convert_to('s')
        self.convert_to('km/h')
        self.convert_to('kWh')
        self.convert_to('kW')
        self.convert_to('V')
        self.convert_to('m')
        self.convert_to('kg')
        self.convert_to('m3')
        self.convert_to('m2')

        return self

    def info(self):
        print(f'val: {self.val}, unit: {self.unit}, description: {self.description}')


def parallelize(function=None, inputdict: dict = None, nr_workers=1, **kargs):
    """
    Parallelize function to run program faster.
    The queue contains tuples of keys and objects, the function must be consistent when getting data from queue.

    Args:
        function (function, optional): Function that is to be parallelized. Defaults to None.
        inputdict (dict, optional): Contains numbered keys and as value any object. Defaults to None.
        nr_workers (int, optional): Number of workers, so their tasks can run parallel. Defaults to 1.

    Returns:
        dict: Dictionary the given functions creates.
    """
    total_cpu = cpu_count()
    print(f"Workers: {nr_workers} of {total_cpu}")
    if nr_workers > total_cpu:
        nr_workers = total_cpu
        print(f"Workers: {nr_workers}")
    with Manager() as manager:
        dc = manager.dict()
        queue = Queue()
        for key, item in inputdict.items():
            queue.put((key, item))
        queue_lock = Lock()
        processes = {}
        for i in range(nr_workers):
            if kargs:
                processes[i] = Process(target=parallel_func,
                                       args=(
                                           dc,
                                           queue,
                                           queue_lock,
                                           function,
                                           kargs,
                                       ))
            else:
                processes[i] = Process(target=parallel_func,
                                       args=(
                                           dc,
                                           queue,
                                           queue_lock,
                                           function,
                                       ))
            processes[i].start()
        for i in range(nr_workers):
            processes[i].join()
        outputdict = dict(dc)
    return outputdict


def parallel_func(dc, queue=None, queue_lock=None, function=None, kargs={}):
    """
    #TODO DOCSTRING

    Args:
        dc ([type]): [description]
        queue ([type], optional): [description]. Defaults to None.
        queue_lock ([type], optional): [description]. Defaults to None.
        function ([type], optional): [description]. Defaults to None.
        kargs (dict, optional): [description]. Defaults to {}.

    Returns:
        [type]: [description]
    """

    while True:
        queue_lock.acquire()
        if queue.empty():
            queue_lock.release()
            return None
        key, item = queue.get()
        queue_lock.release()
        obj = function(**item, **kargs)
        dc[key] = obj


def set_seed():
    """
    Sets seed at the beginning of any python script or jupyter notebook. That allows to repeat the same calculations
    with exactly same results, without any random noise.
    """
    @numba.njit
    def set_seed_with_numba(seed):
        np.random.seed(seed)
        random.seed(seed)

    with open(f"config_files/seed.txt") as f:
        seed = int(f.read().replace('\n', ''))
    set_seed_with_numba(seed)


def check_for_new_function_name(attribute_error_name):
    """
    In an earlier update function names have been changed from camelCase to snake_case. To prevent users confusing this
    function raises a specific AttributeError of the user trys to access to old function name, which does not exist
    anymore.
    """
    new_names = {
        'ChooseChargingPoint': '_choose_charging_point',
        'ChooseChargingPointFast': '_choose_charging_point_fast',
        'drawing_soc': '_drawing_soc',
        'fill_rows': '_fill_rows',
        'initial_conf': '_initial_conf',
        'loadSettingDriving': '_load_setting_driving',
        'save_profile': 'save_profile',
        'setBatteryRules': '_set_battery_rules',
        'setScenario': 'set_scenario',
        'setVehicleFeature': '_set_vehicle_feature',
        'soc': '_soc',
        'testing_soc': '_testing_soc',

        'A2BatPoint': '_A2BatPoint',
        'balanced': '_balanced',
        'changeBatteryCapacity': 'x',
        'check_success': '_check_success',
        'immediate': '_immediate',
        'loadScenario': 'load_scenario',
        'setSubScenario': 'set_sub_scenario',

        'load_specs': '_load_specs',

        'cop_and_target_temp': '_cop_and_target_temp',
        'ev_par_test': '_ev_par_test',
        'loadSettingMobility': 'load_setting_mobility',

        'select_driving_cycle_index': '_select_driving_cycle_index',
        'get_index_speed': '_get_index_speed',

        'check': '_check',
        'layers_name': '_layers_name',
        'makearrays': '_makearrays',
        'zones_name': '_zones_name',

        'get_codes': '_get_codes',
        'get_efficiency': '_get_efficiency',
        'load_file': '_load_file',

        'frontal_area': '_frontal_area',
        'PMR': '_pmr',

        'airDensityFromIdealGasLaw': 'air_density_from_ideal_gas_law',
        'calcDewPoint': 'calc_dew_point',
        'calcDryAirPartialPressure': 'calc_dry_air_partial_pressure',
        'calcRelHumidity': 'calc_rel_humidity',
        'calcVaporPressure': 'calc_vapor_pressure',
        'humidairDensity': 'humidair_density',

        'loadfilesBatch': 'loadfiles_batch',
        'clean': '_clean',
        'group_trips_week': '_group_trips_week',
        'logging_meetcond': '_logging_meetcond',
        'MeetAllConditions': '_meet_all_conditions',
        'select_tour': '_select_tour',
        'setParams': 'set_params',
        'setStats': 'set_stats',
        'setRules': 'set_rules',
    }
    if attribute_error_name in new_names.keys():
        raise AttributeError(
            f'{attribute_error_name} does not exist. Note: We changed the attribute names from camelCase '
            f'to snake_case. \n The new attribute name for {attribute_error_name} is {new_names[attribute_error_name]}.')
    else:
        raise AttributeError(
            f'{attribute_error_name} does not exist. Note: We changed the attribute names from camelCase '
            f'to snake_case. \n You may have to adapt your attributes.')
