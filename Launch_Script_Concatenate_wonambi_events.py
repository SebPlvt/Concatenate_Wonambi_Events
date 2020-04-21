# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 10:46:53 2019

@author: Sébastien Polvent
@mail: sebastien.polvent@unicaen.fr
@mail: seb6347@gmail.com
"""

import concatenate_wonambi_events_class as cwe
import U1077LogoClass


#//////////////////////////////////////////////////////////////////////////////
#//                           ##  MAIN PROGRAM  ##                           //
#//////////////////////////////////////////////////////////////////////////////
U1077LogoClass.U1077_Logo().print_logo()
#initialize object
wonambi_concatenated_events = cwe.ConcatenatedWonambiEvents()
#launch concatenation process
wonambi_concatenated_events.launch_concatenation_process()
#print a dataframe with frequencies of matching combinations of spindles detections
try:
    df_analyse_spindle_detections = \
    wonambi_concatenated_events.analyze_spindles_detections_concordance(
        detection_types=wonambi_concatenated_events.spindles_detection_types)
except NameError:
    print('Error : No spindles detections found !')
