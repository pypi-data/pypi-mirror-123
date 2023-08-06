=====
Usage
=====

Basic Usages
------------

To use FEMAP neutral Parser in a project::

        >>> from femap_neutral_parser import Parser

To instantiate a new parser, just pass a filepath::

        >>> neu = Parser("tests/data/mystran_00.NEU")

To have a list of available blocks::

        >>> neu.available_blocks()
        {'header': 100, 'output_sets': 450, '_output_vectors': 451}

Or maybe in a more human-friendly way is to use `info()` method, which prints
available results and outputs::

        >>> neu.info()
        <BLANKLINE>
        Analysis
        ========
         * subcase 1: Analyse. NASTRAN SPC 1 - lc1. test (MYSTRAN::Static)
         * subcase 2: Analyse. NASTRAN SPC 1 - lc2. test (MYSTRAN::Static)
        <BLANKLINE>
        Outputs
        =======
        access to one of them using `._output_vectors[<title>][<SubcaseID>]['record']
        <BLANKLINE>
         * displacements::t_total -> RSS translation
         * displacements::t1 -> T1 translation
         * displacements::t2 -> T2 translation
         * ...
         * cbar_stress::min_comb_a -> BAR EndA Min Stress
         * cbar_stress::min_comb_b -> BAR EndB Min Stress


Access available blocs by attribute::

        >>> from pprint import pprint as pp
        >>> pp(neu.output_sets)
        {1: {'anal_type': 'Static',
             'from_prog': 'Unknown',
             'integer_format': None,
             'notes': '',
             'process_type': None,
             'title': 'Analyse. NASTRAN SPC 1 - lc1. test',
             'value': 0.0},
         2: {'anal_type': 'Static',
             'from_prog': 'Unknown',
             'integer_format': None,
             'notes': '',
             'process_type': None,
             'title': 'Analyse. NASTRAN SPC 1 - lc2. test',
             'value': 0.0}}

Low-level data access
---------------------


Under the hood, output vectors (block451) are organized as nested dictionaries ``[<vector title>][<LCID>]``::

        >>> pp(neu._output_vectors["displacements::t_total"][2])
        {'abs_max': 2.578386,
         'calc_warn': True,
         'cent_total': True,
         'comp_dir': 1,
         'component_vec': [10002.0,
                           10003.0,
                           10004.0,
                           0.0,
                           0.0,
                           0.0,
                           0.0,
                           0.0,
                           0.0,
                           0.0],
         'id_max': 7,
         'id_min': 1,
         'max_val': 2.578386,
         'min_val': 0.0,
         'record': array([( 1, 0.000000e+00), ( 2, 2.045391e-01), ( 3, 0.000000e+00),
               ( 4, 1.468270e-02), ( 5, 9.231050e-05), ( 6, 6.276400e-01),
               ( 7, 2.578386e+00), ( 8, 1.025100e-01), ( 9, 2.578363e+00),
               (10, 1.916094e+00), (11, 1.100510e+00), (12, 2.389742e+00)],
              dtype=[('NodeID', '<i8'), ('displacements::t_total', '<f8')]),
         'vecID': 10001}


Aggregated Outputs
------------------

Slightly highest level than `_output_vectors` access, aggregated output is available using `Parser.vectors()` method. For example, to get all outputs for translations vectors::

        >>> arr = neu.vectors(("displacements::t1", "displacements::t2", "displacements::t3"))
        >>> arr
        rec.array([( 1,  0.        , 0.,  0.000000e+00, 1),
                   ( 2, -0.1870816 , 0.,  0.000000e+00, 1),
                   ...
                   (11,  0.        , 0., -1.100510e+00, 2),
                   (12,  0.        , 0., -2.389742e+00, 2)],
                  dtype=[('NodeID', '<i8'), ('displacements::t1', '<f8'), ('displacements::t2', '<f8'), ('displacements::t3', '<f8'), ('SubcaseID', '<i8')])

Returned value is a numpy structured array (`<https://numpy.org/doc/stable/user/basics.rec.html>`_). If Pandas is available, you can request to have a DataFrame instead::

        >>> neu.vectors(("displacements::t1", "displacements::t2", "displacements::t3"), asdf=True)
                           displacements::t1  displacements::t2  displacements::t3
        SubcaseID NodeID                              
        1         1       0.000000       0.0  0.000000
                  2      -0.187082       0.0  0.000000
        ...
                  11      0.000000       0.0 -0.956073
                  12      0.000000       0.0 -1.602912
        2         1       0.000000       0.0  0.000000
                  2      -0.204539       0.0  0.000000
        ...
                  11      0.000000       0.0 -1.100510
                  12      0.000000       0.0 -2.389742   

You can also request subcaseIDs, or request raw headers::
 
        >>> neu.vectors(("displacements::t1", "displacements::t2", "displacements::t3"), asdf=True, raw=True, 
        ...              SubcaseIDs=2)
                          T1 translation  T2 translation  T3 translation
        SubcaseID NodeID                                                
        2         1             0.000000             0.0        0.000000
                  2            -0.204539             0.0        0.000000
        ...
                  11            0.000000             0.0       -1.100510
                  12            0.000000             0.0       -2.389742

High-Level access
-----------------

At highest level, you can use the `get` method that already organize vectors for you::

        >>> neu.get(what="displacements", asdf=True)
                                t1   t2        t3        r1        r2            r3
        SubcaseID NodeID                                                           
        1         1       0.000000  0.0  0.000000 -0.000432  0.008923  4.699029e-03
                  2      -0.187082  0.0  0.000000  0.000432  0.008923  4.666047e-03
        ...
        2         1       0.000000  0.0  0.000000 -0.000007  0.009755  5.137517e-03
                  2      -0.204539  0.0  0.000000  0.000007  0.009755  5.101457e-03
        ...
                  11      0.000000  0.0 -1.100510  0.000000  0.010988  1.006013e-06
                  12      0.000000  0.0 -2.389742  0.000000  0.004149  1.360364e-08

  
