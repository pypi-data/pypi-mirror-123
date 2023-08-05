BEV models
==========

This example shows the different cars that are included in the database. A Sankey diagram can be used to clearly identify the energy usage for each car.

To initialize the example1 and create a project folder, the template *eg1* must be selected:

.. code-block:: bash

    $ emobpy create -n <give a name> -t eg1

.. warning::
    Before running this example, install and activate an emobpy dedicated environment (conda recommended).

The initialisation creates a folder and file structure as follows.

.. code-block:: bash

    ├── my_evs
    │   └── config_files
    │       ├── DepartureDestinationTrip_Worker.csv
    │       ├── DistanceDurationTrip.csv
    │       ├── rules.yml
    │       ├── TripsPerDay.csv
    │   ├── eg1.ipynb

Everything, running and visualization, happens in a single jupyter notebook file. In the default settings a single mobility profile is created and three consumption profiles for different car types. For each car a Sankey diagram is created to show the different energy usage of the cars.
