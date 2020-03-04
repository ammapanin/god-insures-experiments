#! /usr/bin/env/python

from ghana_program import ghana_experiment
reload(ghana_experiment)

root = ghana_experiment.run_program(subgroup = "AoG Dansoman Exhibition",
                                    debug = False)


