# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 10:46:53 2019

@author: Sébastien Polvent
@mail: sebastien.polvent@unicaen.fr
@mail: seb6347@gmail.com
"""
import os
import time
from lxml import etree
import pandas as pd


class ConcatenatedWonambiEvents():
    """ConcatenatedWonambiEvents """



    def __init__(self):
        """ init
        sets attributes and list of wonambi files to process"""

        ##set minimum concatenations number required for processing spindles concatenations
        #should never be < 1 (to avoid the adding of a single event to concatenations
        #match_parameter=1 means : there is 1 match with the reference event
        #so it concatenates 2 events together
        self.match_parameter = 1
        ##

        os.chdir(os.getcwd())
        self.wonambi_files = \
            self.get_file_list_from_path(filetype='.xml', \
                                         path='./WONAMBI_EVENTS_CONCATENATE_INPUT_FILES')
        self.spindles_detection_types = []
        #do not use PHYSIP 'Spindles CzPz'
        self.spindles_events_names = ['Moelle2011', 'Lacourse2018', 'Ray2015', \
                                      'Martin2013', 'Wamsley2012', 'Nir2011', \
                                      'Ferrarelli2007']
        self.spindles_events_names.sort()



    def launch_concatenation_process(self):
        """ launch_concatenation_process
        Concatenates spindles events
        Concatenates slow waves events"""

        print("Please wait while processing...", flush=True)
        TIMER = time.time()

        for won_file in self.wonambi_files:
            print('\n' + won_file[:17] + '_______________________________________', flush=True)
            spindles_events = self.get_list_events(sourcefile=won_file, sleep_figure='spindles')
            artefacts_events = self.get_list_events(sourcefile=won_file, sleep_figure='artefacts')
            slow_waves_events = self.get_list_events(sourcefile=won_file, sleep_figure='slow waves')

            df_spindles_events = \
                self.create_dataframe_of_artefactsfree_events(stack_events=spindles_events, \
                                                              artefacts_events=artefacts_events)
            if slow_waves_events:
                df_slow_waves_events = \
                    self.create_dataframe_of_artefactsfree_events(stack_events=slow_waves_events, \
                                                                  artefacts_events=artefacts_events)

            concatenated_spindles_events, temp_spin_tab = \
                self.concatenate_events(df_events=df_spindles_events, \
                                        returns_detections_types=True)
            self.spindles_detection_types.extend(temp_spin_tab)
            if slow_waves_events:
                concatenated_slow_waves_events = self.concatenate_events(df_events=df_slow_waves_events)

            #add concatenated events from input xml file and save all in a new xml file
            #save spindles
            try:
                if concatenated_spindles_events:
                    print('\n' + won_file[:17] +', Number of concatenated events : ' \
                          + str(len(concatenated_spindles_events)), flush=True)
                    print('\n')
                    exported_file = \
                    self.save_concatenated_events_xml_file(wonambi_xml_file=won_file, \
                                                           events_list=concatenated_spindles_events, \
                                                           event_label='Concatenated_spindles', \
                                                           input_files_path=".\\WONAMBI_EVENTS_CONCATENATE_INPUT_FILES\\")
            except NameError:
                print('No Spindles events to save')
                exported_file = False
            #save slow waves
            if not exported_file:
                exported_file = won_file
                path_xml = ".\\WONAMBI_EVENTS_CONCATENATE_INPUT_FILES\\"
            else:
                path_xml = ".\\WONAMBI_EVENTS_CONCATENATED_EVENTS_FILES\\"
            try:
                if concatenated_slow_waves_events:
                    self.save_concatenated_events_xml_file(wonambi_xml_file=exported_file, \
                                                           events_list=concatenated_slow_waves_events, \
                                                           event_label='Concatenated_Slow_Waves', \
                                                           input_files_path=path_xml)
            except NameError:
                print('No Slow waves events to save')


        TEMPS_INTER = time.time() - TIMER
        print('\rAnalysis Completed !')
        print(f'Processing time : {TEMPS_INTER:.2f} seconds.')



    def concat_events(self, events1, events2):
        """concats events in an interval of time
        NOT USED IN THIS SCRIPT, WORKS"""
        concatenated_events = []
        for evt1 in events1:
            for evt2 in events2:
                if evt1[2] == evt2[2]:
                    if evt1[1] < evt2[0]:
                        break
                    elif evt1[0] <= evt2[0] and evt1[1] <= evt2[1] and evt1[1] >= evt2[0]:
                        concatenated_events.append([evt1[0], evt2[1], evt1[2], 'Good'])
                    elif evt1[0] >= evt2[0] and evt1[1] >= evt2[1] and evt1[0] <= evt2[1]:
                        concatenated_events.append([evt2[0], evt1[1], evt1[2], 'Good'])
                    elif evt1[0] >= evt2[0] and evt1[1] <= evt2[1]:
                        concatenated_events.append([evt2[0], evt2[1], evt1[2], 'Good'])
                    elif evt1[0] <= evt2[0] and evt1[1] >= evt2[1]:
                        concatenated_events.append([evt1[0], evt1[1], evt1[2], 'Good'])
        return concatenated_events



    def get_file_list_from_path(self, filetype, path):
        """ returns a list of the files in the path"""
        all_files_list = os.listdir(path)
        files_list = []
        for file in all_files_list:
            if file.count(filetype):
                #files_list.append(path + "\\" + file)
                files_list.append(file)
        return files_list



    def get_list_events(self, sourcefile, sleep_figure):
        """returns a list of Wonambi events from xml file in a list
        sleep_figure : 'spindles', 'artefacts', 'slow waves'
        """
        def create_events_list(list_of_events):
            """create_events_list"""
            events_by_type = []
            for item1 in list_of_events:
                temp_list = [x.text for x in item1]
                new_temp_list = []
                for temp in temp_list:
                    try:
                        if isinstance(float(temp), float):
                            new_temp_list.append(float(temp))
                    except ValueError:
                        new_temp_list.append(temp)
                events_by_type.append(new_temp_list)
            return events_by_type

        tree = etree.parse(os.getcwd() +
                           "\\WONAMBI_EVENTS_CONCATENATE_INPUT_FILES\\"
                           + sourcefile)
        root = tree.getroot()
        rater = [k for k in root.getchildren() if str(k).count('rater')][0]
        events = [k for k in rater.getchildren() if str(k).count('events')][0]
        list_event_type = [k for k in events.getchildren() if str(k).count('event_type')]
        list_all_events = []
        for event_type in list_event_type:
            type_evt = [event_type.get('type')]
            if type_evt[0] in self.spindles_events_names and sleep_figure == 'spindles':
                event = [k for k in event_type.getchildren() if str(k).count('event')]
                type_evt.append(create_events_list(event))
                if type_evt[1]:
                    list_all_events.append(type_evt)
            elif type_evt[0].count('Artefact') and sleep_figure == 'artefacts':
                event = [k for k in event_type.getchildren() if str(k).count('event')]
                list_all_events = create_events_list(event)
            elif type_evt[0].count('Slow Waves') and sleep_figure == 'slow waves':
                event = [k for k in event_type.getchildren() if str(k).count('event')]
                type_evt.append(create_events_list(event))
                if type_evt[1]:
                    list_all_events.append(type_evt)
        try:
            if list_all_events:
                return_exp = list_all_events
            else:
                return_exp = None
        except NameError:
            return_exp = -1
        return return_exp



    def create_dataframe_of_artefactsfree_events(self, stack_events, artefacts_events):
        """ create_dataframe_of_artefactsfree_events """

        def clean_events_from_artefacts(list_events, artefacts_events):
            """ removes events which are in an artefacts event,
            returns a cleaned list of events"""
            print('Number of events : ' + str(len(list_events)) + '.')
            list_copy = list_events[:]
            for spindle in list_events:
                artefact_marker = False
                for artefact in artefacts_events:
                    if spindle[0] > artefact[1]:
                        next
                    elif artefact[0] > spindle[1]:
                        break
                    elif (spindle[0] >= artefact[0] and spindle[0] <= artefact[1]) or \
                       (spindle[1] >= artefact[0] and spindle[1] <= artefact[1]):
                        artefact_marker = True
                        break
                if artefact_marker:
                    list_copy.remove(spindle)
            print('Number of cleaned events : ' + str(len(list_copy)) + \
                  '. Artefacts removed : ' + str(len(list_events) - len(list_copy)))
            return list_copy


        #create dataframe of artefact-free events
        all_events = []
        for ev in stack_events:
            print('\n' + str(ev[0]))
            temp_tab = clean_events_from_artefacts(list_events=ev[1], \
                                                   artefacts_events=artefacts_events)
            for ev2 in temp_tab:
                all_events.append([ev[0], ev2[0], ev2[1]])
        df_events = pd.DataFrame(data=all_events, \
                                     columns=['event_type', 'event_start', 'event_end'])
        df_events = df_events.sort_values('event_start')
        #compare and concatenate spindles events
        df_events.reset_index(inplace=True)
        return df_events



    def concatenate_events(self, df_events, returns_detections_types=False):
        """concatenate_events
        returns concatenated_events, returns detection_types if spindles only"""
        #match parameter : for spindles :
        #from which minimal number of detection methods for concatenation
        if returns_detections_types:
            match_parameter = self.match_parameter
        else:
            match_parameter = 0
        detection_types = []

        #select first event as reference interval
        event_start_ref = df_events.loc[0, 'event_start']
        event_end_ref = df_events.loc[0, 'event_end']
        event_type_ref = df_events.loc[0, 'event_type']

        concatenated_events = []
        nb_matches = 0
        temp_detection_types = [event_type_ref]
        #loop form 2nd event
        for ev in range(1, len(df_events.index)):

            #select event to compare with reference event
            event_start_comp = df_events.loc[ev, 'event_start']
            event_end_comp = df_events.loc[ev, 'event_end']

            #if compared event is in reference event interval
            if event_start_ref < event_start_comp < event_end_ref:
                ##if compared event end is outside reference event interval
                if event_end_comp > event_end_ref:
                    #it becomes the new reference event's end
                    event_end_ref = event_end_comp
                #increase the number of matching events for concatenation
                nb_matches += 1
                #append event type for further concatenation comparison
                temp_detection_types.append(df_events.loc[ev, 'event_type'])
            else:
                #else : events are concatenated and added to the list of concatenated events
                temp_detection_types.sort()
                detection_types.append(temp_detection_types)
                concatenated_events.append([event_start_ref, \
                                            event_end_ref, \
                                            'CZ (CzPz)', 'Good', nb_matches, temp_detection_types])

                #compared event becomes new reference
                event_start_ref = event_start_comp
                event_end_ref = event_end_comp
                event_type_ref = df_events.loc[ev, 'event_type']
                #reset list for new detection reference and nb_matches
                temp_detection_types = [event_type_ref]
                nb_matches = 0
        #only keep concatenations with required concatenation matching number
        concatenated_events2 = []
        detection_types2 = []
        for concat_evt in concatenated_events:
            if concat_evt[4] >= match_parameter:
                concatenated_events2.append(concat_evt)
                detection_types2.append(concat_evt[5])
        #returns concatenated_events, returns detection_types if spindles only
        if returns_detections_types:
            return concatenated_events2, detection_types2
        else:
            return concatenated_events2



    def save_concatenated_events_xml_file(self, wonambi_xml_file, events_list,
                                          event_label, input_files_path):
        """export_concatenated_events_wonambi_xml_file"""
        print("Saving new XML file...", flush=True)
        #parse xml
        tree = etree.parse(os.getcwd() + \
                           input_files_path + \
                           wonambi_xml_file)
        root = tree.getroot()
        rater = [x for x in root.getchildren() if str(x).count('rater')][0]
        events = [x for x in rater.getchildren() if str(x).count('events')][0]
        #add event type
        event_type = etree.SubElement(events, "event_type")
        event_type.set("type", event_label)
        for evt in events_list:
            #add events to xml file
            event = etree.SubElement(event_type, "event")

            event_start = etree.SubElement(event, "event_start")
            event_start.text = str(evt[0])

            event_end = etree.SubElement(event, "event_end")
            event_end.text = str(evt[1])

            event_chan = etree.SubElement(event, "event_chan")
            event_chan.text = str(evt[2])

            event_qual = etree.SubElement(event, "event_qual")
            event_qual.text = str(evt[3])

        export_file = wonambi_xml_file[:17] + "_scores_WONAMBI_" + event_label + ".xml"
        if event_label == 'Concatenated_Slow_Waves':
            file_label = 'Concatenated_Spindles_and_Slow_Waves'
            export_file = wonambi_xml_file[:17] + "_scores_WONAMBI_" + file_label + ".xml"
            if os.path.exists(".\\WONAMBI_EVENTS_CONCATENATED_EVENTS_FILES\\" + wonambi_xml_file):
                os.remove(".\\WONAMBI_EVENTS_CONCATENATED_EVENTS_FILES\\" + wonambi_xml_file)
                print("Previous file " + wonambi_xml_file + " deleted.")
        with open(".\\WONAMBI_EVENTS_CONCATENATED_EVENTS_FILES\\" + \
                  export_file, "wb") as xml_file:
            xml_file.write(etree.tostring(tree))
        print('New file ' + export_file + ' saved.', flush=True)

        if event_label == 'Concatenated_spindles':
            return export_file



    def powerset(self, seq):
        """Returns all the subsets of this set. This is a generator."""
        if len(seq) <= 1:
            yield seq
            yield []
        else:
            for item in self.powerset(seq[1:]):
                yield [seq[0]]+item
                yield item



    def analyze_spindles_detections_concordance(self, detection_types):
        """analyze_spindles_detections_concordance
        returns a dataframe with frequencies
        of matching combinations of spindles detections"""
        print("\nSpindles concordance comparizon, methods combination >= 10% of detections :")
        print('Please wait...', end='', flush=True)
        #find which detection algorithms detects same sleep figures
        set_detection_types = []
        for detection in detection_types:
            #remove duplicates (in case of detections on multiples channels)
            temp_list = list(set(detection))
            temp_list.sort()
            set_detection_types.append(temp_list)
        #create powerset of all spidles_events_names possible combinations
        powerset_events_names = [x for x in self.powerset(self.spindles_events_names)]
        #remove entries <2
        powerset_events_names = [x for x in powerset_events_names if len(x) >= 2]
        set_detection_types = [x for x in set_detection_types if len(x) >= 2]
        powerset_events_names.sort(key=len)
        set_detection_types.sort(key=len)
        total_number_of_detections = len(set_detection_types)
        #remove last entry if it is an empty list
        #if not powerset_events_names[len(powerset_events_names)-1:][0]:
        #    powerset_events_names.pop()


        #converts sorted lists of lists to list of strings
        powerset_events_names = [",".join(x) for x in powerset_events_names]
        set_detection_types = [",".join(x) for x in set_detection_types]
        powerset_events_names.sort(key=len)
        set_detection_types.sort(key=len)
        #create dataframe
        df_events_names_combinations = pd.DataFrame(data=None, columns=powerset_events_names)
        #fill dataframe with zeros
        for col in df_events_names_combinations.columns:
            df_events_names_combinations.loc[0, col] = 0
        #find matching combinations numbers
        for combination in powerset_events_names:
            for detections in set_detection_types:
                if detections.count(combination):
                    df_events_names_combinations.loc[0, combination] = \
                    df_events_names_combinations.loc[0, combination] + 1

        #transpose and format df
        df_events_names_combinations = df_events_names_combinations.T
        df_events_names_combinations = df_events_names_combinations.reset_index()
        df_events_names_combinations.columns = ['combination', 'number']
        df_events_names_combinations = df_events_names_combinations.sort_values(by='number', \
                                                                                ascending=False)
        #calc percentages
        df_events_names_combinations['percentage'] = \
            round((df_events_names_combinations['number'] / \
                   total_number_of_detections) * 100, 5)

        print('\rFrom ' + str(total_number_of_detections) + ' spindles concatenations.')
        df_mask = df_events_names_combinations['percentage'] >= 10
        filtered_df = df_events_names_combinations[df_mask].reset_index()
        del filtered_df['index']
        print(filtered_df)
        return df_events_names_combinations