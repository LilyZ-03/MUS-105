###############################################################################

## You can import from score, theory and any python module you want to use.

from code import interact
from http.client import CannotSendRequest
from itertools import count
from sre_constants import IN
from tracemalloc import start
from .score import Pitch, Interval, Mode, import_score
from .theory import Analysis, Rule, timepoints
from copy import copy

# A template directory that is copied into your analysis.
# Consult the documentation for more information.

melodic_checks = {
    # Pitch checks
    'MEL_START_NOTE': None,
    'MEL_CADENCE': None,
    'MEL_TESSITURA': None,
    'MEL_DIATONIC': None,
    # Melodic interval checks
    'INT_STEPWISE': None,
    'INT_CONSONANT': None,
    'INT_SIMPLE': None,
    'INT_NUM_LARGE': None,
    'INT_NUM_UNISON': None,
    'INT_NUM_SAMEDIR': None,
    # Leap checks
    'LEAP_RECOVERY': None,  
    'LEAP_NUM_CONSEC': None,
    # Shape checks
    'SHAPE_NUM_CLIMAX': None,
    'SHAPE_ARCHLIKE': None,
    'SHAPE_UNIQUE': None
}

# Here is an example of a rule. You can define as many rules as you like.
# The purpose of a rule is to perform some analytical check(s) and
# then update the self.analysis.results dictionary with its findings.
class LaitzMelodyRule(Rule):

    # Rule initializer.
    def __init__(self, analysis):
        # Always set the rule's back pointer to its analysis!
        super().__init__(analysis, "My Laitz82 Melody rule.")
        # Now initialize whatever attributes your rule defines.
        # ...

    def pitch_checks(self):
        scale = self.analysis.score.get_metadata("main_key").scale()
       
        # starting note check - tonic triad
        start_pitch_pnum = self.analysis.melody[0].pitch.pnum() 
        # print("scale:", scale)
        # print(self.analysis.melody)
        # print(start_pitch_pnum)
        if start_pitch_pnum == scale[0] or start_pitch_pnum == scale[2] or start_pitch_pnum == scale[4]:
            self.analysis.results['MEL_START_NOTE'] = True
        else: 
            self.analysis.results['MEL_START_NOTE'] = []

        # cadence check - 7-1 or 2-1
        end_pitch_pnum = self.analysis.melody[len(self.analysis.melody) - 1].pitch.pnum()
        second_to_last_pnum = self.analysis.melody[len(self.analysis.melody) - 2].pitch.pnum()
        if end_pitch_pnum == scale[0] and (second_to_last_pnum == scale[1] or second_to_last_pnum == scale[6]):
            self.analysis.results['MEL_CADENCE'] = True
        else:
            self.analysis.results['MEL_CADENCE'] = []
        
        melody = self.analysis.melody
        # tessitura check - central Major 6th of the melody's range
        # find the range?
        lowest_note_pos = 0
        highest_note_pos = 0
        
        for i in range(len(melody)):
            if melody[i].pitch.keynum() < melody[lowest_note_pos].pitch.keynum():
                lowest_note_pos = i
            elif melody[i].pitch.keynum() > melody[highest_note_pos].pitch.keynum():
                highest_note_pos = i

        # interval_range = Interval(melody[lowest_note_pos].pitch, melody[highest_note_pos].pitch)
        range_midpoint = (melody[lowest_note_pos].pitch.keynum() + melody[highest_note_pos].pitch.keynum()) / 2
        upper_bound, lower_bound = range_midpoint + 4.5, range_midpoint - 4.5
        print(range_midpoint, upper_bound, lower_bound)

        count_out_of_tessitura = 0
        for i in melody:
            # print(i.pitch.keynum(), count_out_of_tessitura)
            if i.pitch.keynum() < lower_bound or i.pitch.keynum() > upper_bound:
                count_out_of_tessitura += 1
        
        if (count_out_of_tessitura / len(melody)) <= 0.25:
            self.analysis.results['MEL_TESSITURA'] = True
        else:
            self.analysis.results['MEL_TESSITURA'] = []

        # diatonic check
        non_diatonic = []
        
        for i in range(len(melody)):
            if melody[i].pitch.pnum() not in scale:
                if str(self.analysis.score.get_metadata("main_key").mode) == "Mode.MINOR" and melody[i].pitch.pnum() == scale[6] + 1:
                    pass
                else: 
                    non_diatonic.append(i+1)
        if len(non_diatonic) == 0:
            self.analysis.results['MEL_DIATONIC'] = True
        else:
            self.analysis.results['MEL_DIATONIC'] = non_diatonic
    
    def melodic_interval_checks(self):
        
        #stepwise check - 51%
        melody = self.analysis.melody
        intervals = []
        count_stepwise = 0
        for i in range(len(melody) - 1):
            itv = Interval(melody[i].pitch, melody[i + 1].pitch)
            intervals.append(itv)
            if itv.span == 1:
                count_stepwise += 1

        if count_stepwise / (len(melody) - 1) >= 0.51:
            self.analysis.results['INT_STEPWISE'] = True
        else:
            self.analysis.results['INT_STEPWISE'] = []

        
        # pairs of [span, quality]
        # what about seconds?
        consonant_intervals = [ [0, 6], [1, 5], [1, 7], [2, 5], [2, 7], [3, 6], [4, 6], [5, 5], [5, 7], [7, 6] ]

        # consonant interval check
        # simple interval check
        # number of large interval check
        # number of unison check
        dissonant_intervals = []
        complex_intervals = []
        large_intervals = []
        unisons = []
        for i in range(len(intervals)):
            pair_dat = [intervals[i].span, intervals[i].qual]
            if pair_dat not in consonant_intervals:
                dissonant_intervals.append(i + 1)
            if intervals[i].xoct != 0:
                complex_intervals.append(i + 1)
            if intervals[i].span >= 4 or intervals[i].xoct != 0:
                large_intervals.append(i + 1)
            elif intervals[i].span == 0:
                unisons.append(i + 1)
        
        if len(dissonant_intervals) == 0:
            self.analysis.results['INT_CONSONANT'] = True
        else:
            self.analysis.results['INT_CONSONANT'] = dissonant_intervals
        
        if len(complex_intervals) == 0:
            self.analysis.results['INT_SIMPLE'] = True
        else:
            self.analysis.results['INT_SIMPLE'] = complex_intervals

        if len(large_intervals) <= 1:
            self.analysis.results['INT_NUM_LARGE'] = True
        else:
            self.analysis.results['INT_NUM_LARGE'] = large_intervals[1:]

        if len(unisons) <= 1:
            self.analysis.results['INT_NUM_UNISON'] = True
        else:
            self.analysis.results['INT_NUM_UNISON'] = unisons[1:]

        # number of consecutive same direction interval check
        count_consecutive = 1
        current_dir = intervals[0].sign
        fail_samefir = []
        for i in range(1, len(intervals)):
            if intervals[i].sign == current_dir:
                count_consecutive += 1
            else:
                current_dir = intervals[i].sign
                count_consecutive = 1
            if count_consecutive > 3:
                fail_samefir.append(i + 2)
        
        if len(fail_samefir) == 0:
            self.analysis.results['INT_NUM_SAMEDIR'] = True
        else:
            self.analysis.results['INT_NUM_SAMEDIR'] = fail_samefir

    def leap_checks(self):

        melody = self.analysis.melody
        
        intervals = []
        for i in range(len(melody) - 1):
            itv = Interval(melody[i].pitch, melody[i + 1].pitch)
            intervals.append(itv)
        
        # leap recovery check
        leap_combined = []
        leap_combined.append(intervals[0])

        # consecutive leap check prep
        consecutive_leap_num = []
        if intervals[0].span > 1:
            consecutive_leap_num.append(1)
        else: 
            consecutive_leap_num.append(0)

        for i in range(1, len(intervals)):
            if intervals[i].span > 1:
                consecutive_leap_num.append(consecutive_leap_num[i - 1] + 1)
            else:
                consecutive_leap_num.append(0)
            if intervals[i].sign == intervals[i - 1].sign and intervals[i].span > 1 and intervals[i - 1].span > 1:
                leap_combined.append(intervals[i].add(intervals[i - 1]))
            else:
                leap_combined.append(intervals[i])

        # print(leap_combined)
    
        fail_recovery = []
        for i in range(len(leap_combined)):
            if leap_combined[i].span == 3:
                if i + 1 == len(leap_combined):
                    fail_recovery.append(len(melody))
                elif leap_combined[i].sign == leap_combined[i + 1].sign:
                    fail_recovery.append(i + 2)
            elif leap_combined[i].span >= 4:
                if i + 1 == len(leap_combined):
                    fail_recovery.append(-len(melody))
                elif not (leap_combined[i].sign == -leap_combined[i + 1].sign and leap_combined[i + 1].span == 1):
                    fail_recovery.append(-(i + 2))

        if len(fail_recovery) == 0:
            self.analysis.results['LEAP_RECOVERY'] = True
        else:
            self.analysis.results['LEAP_RECOVERY'] = fail_recovery
        
        # consecutive leap check
        fail_consecutive = []

        for i in range(len(consecutive_leap_num)):
            if consecutive_leap_num[i] > 2:
                fail_consecutive.append(i + 1)
                
        if len(fail_consecutive) == 0:
            self.analysis.results['LEAP_NUM_CONSEC'] = True
        else:
            self.analysis.results['LEAP_NUM_CONSEC'] = fail_consecutive


    def shape_checks(self):
        melody = self.analysis.melody

        # climax check - only one climax
        highest_note_pos = 0
        
        for i in range(len(melody)):
            if melody[i].pitch.keynum() > melody[highest_note_pos].pitch.keynum():
                highest_note_pos = i

        count_climax = []
        highest_pitch = melody[highest_note_pos].pitch

        for i in range(len(melody)):
            if melody[i].pitch == highest_pitch:
                count_climax.append(i + 1)
        
        if len(count_climax) <= 1:
            self.analysis.results['SHAPE_NUM_CLIMAX'] = True
        else:
            self.analysis.results['SHAPE_NUM_CLIMAX'] = count_climax[1:]

        print(count_climax)

        # arch like shape check
        tps = timepoints(self.analysis.score, span=True, measures=True)
        num_of_beats = len(tps) * self.analysis.score.get_metadata('main_meter').num
        len_of_beat = 1 / self.analysis.score.get_metadata('main_meter').den
        start_of_central_third = (num_of_beats // 3 + 1) * (1 / self.analysis.score.get_metadata('main_meter').den)
        end_of_central_third = (num_of_beats // 3) * 2
        if num_of_beats % 3 != 0:
            end_of_central_third += 1
        end_of_central_third *= (1 / self.analysis.score.get_metadata('main_meter').den)
        print(start_of_central_third, end_of_central_third)
 
        durations = []
        for measure in tps:
            if len(measure) == 1:
                durations.append(self.analysis.score.get_metadata('main_meter').num / self.analysis.score.get_metadata('main_meter').den)
            else:
                for i in range(1, len(measure)):
                    # print(len(measure))
                    durations.append((measure[i].beat - measure[i - 1].beat).float())
                durations.append(self.analysis.score.get_metadata('main_meter').num / self.analysis.score.get_metadata('main_meter').den
                    - measure[len(measure) - 1].beat.float())

        for i in range(1, len(durations)):
            durations[i] += durations[i - 1]

        invalid_climaxes = []
        print(durations)

        for i_climax in count_climax:
            if durations[i_climax - 1] < start_of_central_third or durations[i_climax - 1] > end_of_central_third:
                invalid_climaxes.append(i_climax)
        
        if len(invalid_climaxes) == 0:
            self.analysis.results['SHAPE_ARCHLIKE'] = True
        else:
            self.analysis.results['SHAPE_ARCHLIKE'] = invalid_climaxes

        # unique shape check
        repetitive_motions = []

        if len(repetitive_motions) == 0:
            self.analysis.results['SHAPE_UNIQUE'] = True
        else:
            self.analysis.results['SHAPE_UNIQUE'] = repetitive_motions


    # This is where your rule does all its work. When the work is done you
    # should update the analysis results with your findings.
    def apply(self):
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        print(self.analysis.score.metadata)
        self.pitch_checks()
        self.melodic_interval_checks()
        self.leap_checks()
        self.shape_checks()
    
#    # Uncomment this code if you want your rule to print information to the
#    # the terminal just after it runs...
    # def display(self, index):
    #    print('-------------------------------------------------------------------')
    #    print(f"Rule {index+1}: {self.title}")
    #    print("I'm here!")


# ...ADD MORE RULES HERE!....


# A class representing a melodic analysis of a voice in a score. The class
# has three attributes to begin with, you will likely add more attributes.
# Consult the documentation for more information.
class MelodicAnalysis(Analysis):
    def __init__(self, score):
        # Call the superclass and give it the score. Don't change this line.
        super().__init__(score)
        # Copy the empty result checks template to this analysis. Don't
        # change this line
        self.results = copy(melodic_checks)
        # Create the list of rules this analysis runs. This example just
        # uses the demo Rule defined above.
        self.rules = [LaitzMelodyRule(self)]

    # You can define a cleanup function if you want.
    # def cleanup(self):
    #     self.melody, self.intervals, self.motions = [], [], []

    # You MUST define a setup function. A first few steps are
    # done for you, you can add more steps as you wish.
    def setup(self, args, kwargs):
        assert len(args) == 1, "Usage: analyze(<pvid>), pass the pvid of the voice to analyze."
        # melodic_id is the voice to analyze passed in by the caller.
        # you will want to use this when you access the timepoints
        voice_id = args[0]
        # print(voice_id)
        tps = timepoints(self.score, span=True, measures=False)
        # print(tps)
        self.melody = [ t.nmap[voice_id] for t in tps ]

    # This function is given to you, it returns your analysis results
    # for the autograder to check.  You can also use this function as
    # a top level call for testing. Just make sure that it always returns
    # self.results after the analysis has been performed!
    def submit_to_grading(self):
        # Call analyze() and pass it the pvid used in all the Laitz scores.
        self.analyze('P1.1')
        # Return the results to the caller.
        return self.results


if __name__ == "__main__":
    print("testing...")
    s = import_score("hw9/xmls/Laitz_p84G.musicxml")
    # print(s.get_part("P1")[1])
    analysis = MelodicAnalysis(s)
    print("score is: ", analysis.score.metadata)
    # print("timepoints is: ", analysis.timepoints)
    # print("rules are: ", analysis.rules)
    print(analysis.submit_to_grading())
    # analysis.setup(["P1.1"], 0)