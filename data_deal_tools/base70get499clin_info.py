# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re
inputfile = 'E:\\data\\前列腺癌PRADDATA\\outclin_ctbp1_info.txt'
hang_flag = {}
with open(inputfile,'r',encoding='utf-8')as p:
    langs = p.readlines()
    for lang in langs:
        lang = lang.strip('\n')
        if re.findall('A0_Samples', lang):
            lang_list = lang.split('\t')
            for i in range(len(lang_list)):
                if re.match('A0_Samples',lang_list[i]):
                    hang_flag['As'] = i
                elif re.match('CTBP1',lang_list[i]):
                    hang_flag['CTBP1'] = i
                elif re.match('stage_event.gleason_grading.gleason_score',lang_list[i]):
                    hang_flag['s_score'] = i
                elif re.match('stage_event.gleason_grading.primary_pattern',lang_list[i]):
                    hang_flag['s_pattern'] = i
                elif re.match('stage_event.gleason_grading.secondary_pattern', lang_list[i]):
                    hang_flag['ssecondary_pattern'] = i
                elif re.match('stage_event.tnm_categories.pathologic_categories.pathologic_T',lang_list[i]):
                    hang_flag['s_categories.pathologic_T'] = i
                elif re.match('stage_event.tnm_categories.clinical_categories.clinical_M', lang_list[i]):
                    hang_flag['sclinical_categories.clinical_M'] = i
                elif re.match('stage_event.tnm_categories.clinical_categories.clinical_T', lang_list[i]):
                    hang_flag['sclinical_categories.clinical_T'] = i
                elif re.match('A1_OS', lang_list[i]):
                    hang_flag['A1_OS'] = i
                elif re.match('A2_Event', lang_list[i]):
                    hang_flag['A2_Event'] = i
                elif re.match('A3_T',lang_list[i]):
                    hang_flag['A3_T'] = i
                elif re.match('A4_N',lang_list[i]):
                    hang_flag['A4_N'] = i
                elif re.match('A5_M',lang_list[i]):
                    hang_flag['A5_M'] = i
                elif re.match('biochemical_recurrence',lang_list[i]):
                    hang_flag['b_recurrence'] = i
                elif re.match('bone_scan_results',lang_list[i]):
                    hang_flag['b_results'] = i
                elif re.match('days_to_first_biochemical_recurrence',lang_list[i]):
                    hang_flag['dbiochemical_recurrence'] = i
                elif re.match('drugs.drug.drug_name',lang_list[i]):
                    hang_flag['ddrug_name'] = i
                elif re.match('drugs.drug.measure_of_response',lang_list[i]):
                    hang_flag['dmeasure_of_response'] = i
                elif re.match('drugs.drug.regimen_indication',lang_list[i]):
                    hang_flag['d_indication'] = i
                elif re.match('follow_ups.follow_up.days_to_new_tumor_event_after_initial_treatment',lang_list[i]):
                    hang_flag['finitial_treatment'] = i
                elif re.match('follow_ups.follow_up.days_to_second_biochemical_recurrence',lang_list[i]):
                    hang_flag['f_recurrence'] = i
                elif re.match('follow_ups.follow_up.days_to_third_biochemical_recurrence',lang_list[i]):
                    hang_flag['fchemical_recurrence'] = i
                elif re.match('follow_ups.follow_up.followup_treatment_success',lang_list[i]):
                    hang_flag['ffollowup_treatment_success'] = i
                elif re.match('follow_ups.follow_up.new_neoplasm_event_occurrence_anatomic_site',lang_list[i]):
                    hang_flag['f_anatomic_site'] = i
                elif re.match('follow_ups.follow_up.new_neoplasm_event_type',lang_list[i]):
                    hang_flag['fneoplasm_event_type'] = i
                elif re.match('follow_ups.follow_up.new_tumor_event_after_initial_treatment',lang_list[i]):
                    hang_flag['f_initial_treatment'] = i
                elif re.match('follow_ups.follow_up.person_neoplasm_cancer_status',lang_list[i]):
                    hang_flag['fcancer_status'] = i
                elif re.match('follow_ups.follow_up.primary_therapy_outcome_success',lang_list[i]):
                    hang_flag['foutcome_success'] = i
                elif re.match('follow_ups.follow_up.tumor_progression_post_ht',lang_list[i]):
                    hang_flag['f_post_ht'] = i
                elif re.match('follow_ups.follow_up.type_ofprogression_of_disease_ht',lang_list[i]):
                    hang_flag['fof_disease_ht'] = i
                elif re.match('follow_ups.follow_up.vital_status',lang_list[i]):
                    hang_flag['f_status'] = i
                elif re.match('new_tumor_events.new_tumor_event.additional_pharmaceutical_therapy',lang_list[i]):
                    hang_flag['new_pharmaceutical_therapy'] = i
                elif re.match('new_tumor_events.new_tumor_event.days_to_new_tumor_event_after_initial_treatment',lang_list[i]):
                    hang_flag['new_after_initial_treatment'] = i
                elif re.match('new_tumor_events.new_tumor_event.new_neoplasm_occurrence_anatomic_site_text',lang_list[i]):
                    hang_flag['new_site_text'] = i
                elif re.match('new_tumor_events.new_tumor_event.tumor_progression_post_ht',lang_list[i]):
                    hang_flag['new_post_ht'] = i
                elif re.match('new_tumor_events.new_tumor_event.type_of_progression_after_ht',lang_list[i]):
                    hang_flag['new_after_ht'] = i
                elif re.match('person_neoplasm_cancer_status',lang_list[i]):
                    hang_flag['person_status'] = i
                elif re.match('primary_therapy_outcome_success',lang_list[i]):
                    hang_flag['primary_success'] = i
                elif re.match('radiations.radiation.measure_of_response',lang_list[i]):
                    hang_flag['radiatof_response'] = i
                elif re.match('radiations.radiation.numfractions',lang_list[i]):
                    hang_flag['radnumfractions'] = i
                elif re.match('radiations.radiation.radiation_dosage', lang_list[i]):
                    hang_flag['radiat_dosage'] = i
                elif re.match('radiations.radiation.regimen_indication', lang_list[i]):
                    hang_flag['radia_indication'] = i
                elif re.match('radiations.radiation.units',lang_list[i]):
                    hang_flag['radiaunits'] = i
                elif re.match('stage_event.psa.days_to_psa',lang_list[i]):
                    hang_flag['stage_psa'] = i
                elif re.match('stage_event.psa.psa_value',lang_list[i]):
                    hang_flag['stagvalue'] = i
                elif re.match('vital_status', lang_list[i]):
                    hang_flag['vital_status'] = i
            hangshou = lang_list[hang_flag['As']] \
                       + '\t' + lang_list[hang_flag['CTBP1']]\
                       + '\t' + lang_list[hang_flag['s_score']]\
                       + '\t' + lang_list[hang_flag['s_pattern']]\
                       + '\t' + lang_list[hang_flag['ssecondary_pattern']]\
                       + '\t' + lang_list[hang_flag['s_categories.pathologic_T']]\
                       + '\t' + lang_list[hang_flag['sclinical_categories.clinical_M']]\
                       + '\t' + lang_list[hang_flag['sclinical_categories.clinical_T']]\
                       + '\t' + lang_list[hang_flag['A1_OS']]\
                       + '\t' + lang_list[hang_flag['A2_Event']]\
                       + '\t' + lang_list[hang_flag['A3_T']]\
                       + '\t' + lang_list[hang_flag['A4_N']]\
                       + '\t' + lang_list[hang_flag['A5_M']]\
                       + '\t' + lang_list[hang_flag['b_recurrence']]\
                       + '\t' + lang_list[hang_flag['b_results']]\
                       + '\t' + lang_list[hang_flag['dbiochemical_recurrence']]\
                       + '\t' + lang_list[hang_flag['ddrug_name']]\
                       + '\t' + lang_list[hang_flag['dmeasure_of_response']]\
                       + '\t' + lang_list[hang_flag['d_indication']]\
                       + '\t' + lang_list[hang_flag['finitial_treatment']]\
                       + '\t' + lang_list[hang_flag['f_recurrence']]\
                       + '\t' + lang_list[hang_flag['fchemical_recurrence']]\
                       + '\t' + lang_list[hang_flag['ffollowup_treatment_success']]\
                       + '\t' + lang_list[hang_flag['f_anatomic_site']]\
                       + '\t' + lang_list[hang_flag['fneoplasm_event_type']]\
                       + '\t' + lang_list[hang_flag['f_initial_treatment']]\
                       + '\t' + lang_list[hang_flag['fcancer_status']]\
                       + '\t' + lang_list[hang_flag['foutcome_success']]\
                       + '\t' + lang_list[hang_flag['f_post_ht']]\
                       + '\t' + lang_list[hang_flag['fof_disease_ht']]\
                       + '\t' + lang_list[hang_flag['f_status']]\
                       + '\t' + lang_list[hang_flag['new_pharmaceutical_therapy']]\
                       + '\t' + lang_list[hang_flag['new_after_initial_treatment']]\
                       + '\t' + lang_list[hang_flag['new_site_text']]\
                       + '\t' + lang_list[hang_flag['new_post_ht']]\
                       + '\t' + lang_list[hang_flag['new_after_ht']]\
                       + '\t' + lang_list[hang_flag['person_status']]\
                       + '\t' + lang_list[hang_flag['primary_success']]\
                       + '\t' + lang_list[hang_flag['radiatof_response']]\
                       + '\t' + lang_list[hang_flag['radnumfractions']]\
                       + '\t' + lang_list[hang_flag['radiat_dosage']]\
                       + '\t' + lang_list[hang_flag['radia_indication']]\
                       + '\t' + lang_list[hang_flag['radiaunits']]\
                       + '\t' + lang_list[hang_flag['stage_psa']]\
                       + '\t' + lang_list[hang_flag['stagvalue']]+'\t'+lang_list[hang_flag['vital_status']]+'\n'  #这样是OK的
            with open('E:\\haxqd\\201806\\outclin_ctbp1_info499.txt','w')as ww:
                ww.write(str(hangshou))
        elif re.findall("TCGA",lang):
            lang_list = lang.split('\t')
            hangshou = lang_list[hang_flag['As']] \
                       + '\t' + lang_list[hang_flag['CTBP1']]\
                       + '\t' + lang_list[hang_flag['s_score']]\
                       + '\t' + lang_list[hang_flag['s_pattern']]\
                       + '\t' + lang_list[hang_flag['ssecondary_pattern']]\
                       + '\t' + lang_list[hang_flag['s_categories.pathologic_T']]\
                       + '\t' + lang_list[hang_flag['sclinical_categories.clinical_M']]\
                       + '\t' + lang_list[hang_flag['sclinical_categories.clinical_T']]\
                       + '\t' + lang_list[hang_flag['A1_OS']]\
                       + '\t' + lang_list[hang_flag['A2_Event']]\
                       + '\t' + lang_list[hang_flag['A3_T']]\
                       + '\t' + lang_list[hang_flag['A4_N']]\
                       + '\t' + lang_list[hang_flag['A5_M']]\
                       + '\t' + lang_list[hang_flag['b_recurrence']]\
                       + '\t' + lang_list[hang_flag['b_results']]\
                       + '\t' + lang_list[hang_flag['dbiochemical_recurrence']]\
                       + '\t' + lang_list[hang_flag['ddrug_name']]\
                       + '\t' + lang_list[hang_flag['dmeasure_of_response']]\
                       + '\t' + lang_list[hang_flag['d_indication']]\
                       + '\t' + lang_list[hang_flag['finitial_treatment']]\
                       + '\t' + lang_list[hang_flag['f_recurrence']]\
                       + '\t' + lang_list[hang_flag['fchemical_recurrence']]\
                       + '\t' + lang_list[hang_flag['ffollowup_treatment_success']]\
                       + '\t' + lang_list[hang_flag['f_anatomic_site']]\
                       + '\t' + lang_list[hang_flag['fneoplasm_event_type']]\
                       + '\t' + lang_list[hang_flag['f_initial_treatment']]\
                       + '\t' + lang_list[hang_flag['fcancer_status']]\
                       + '\t' + lang_list[hang_flag['foutcome_success']]\
                       + '\t' + lang_list[hang_flag['f_post_ht']]\
                       + '\t' + lang_list[hang_flag['fof_disease_ht']]\
                       + '\t' + lang_list[hang_flag['f_status']]\
                       + '\t' + lang_list[hang_flag['new_pharmaceutical_therapy']]\
                       + '\t' + lang_list[hang_flag['new_after_initial_treatment']]\
                       + '\t' + lang_list[hang_flag['new_site_text']]\
                       + '\t' + lang_list[hang_flag['new_post_ht']]\
                       + '\t' + lang_list[hang_flag['new_after_ht']]\
                       + '\t' + lang_list[hang_flag['person_status']]\
                       + '\t' + lang_list[hang_flag['primary_success']]\
                       + '\t' + lang_list[hang_flag['radiatof_response']]\
                       + '\t' + lang_list[hang_flag['radnumfractions']]\
                       + '\t' + lang_list[hang_flag['radiat_dosage']]\
                       + '\t' + lang_list[hang_flag['radia_indication']]\
                       + '\t' + lang_list[hang_flag['radiaunits']]\
                       + '\t' + lang_list[hang_flag['stage_psa']]\
                       + '\t' + lang_list[hang_flag['stagvalue']]+'\t'+lang_list[hang_flag['vital_status']]+'\n'  #这样是OK的
            with open('E:\\haxqd\\201806\\outclin_ctbp1_info499.txt','a')as ww:
                ww.write(str(hangshou))

