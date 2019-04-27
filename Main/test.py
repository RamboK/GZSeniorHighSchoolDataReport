from init_config.property import SUBJECT
import ItemStatistics as mi
import OptionStatistics as mo
import OverallStatistics as mos
import ScoreRange as msr
subject = "tongyongjishu"
for subject in SUBJECT:
    mi.small(subject)
    mo.optionStatistics(subject)
    mos.overall_province(subject)
    mos.overall_city(subject)
    msr.scoreRangeStatistics(subject)
    
