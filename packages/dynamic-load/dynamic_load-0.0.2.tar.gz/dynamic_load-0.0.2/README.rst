Dynamically load modules for Python
===================================

Load python module, or member of module from string.

Example Usage
-------------
::

    from dynamic_load import dynamic_load
    dattime_module =  dynamic_load("datetime") # Load datetime module
    dattime_module.datetime.now()
    time_function = dynamic_load("time.time")
    time_function()

