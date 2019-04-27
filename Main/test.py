from Main.init_config.property import SUBJECT
import Main.ItemStatistics as mi
import Main.OptionStatistics as mo
import Main.OverallStatistics as mos
import Main.ScoreRange as msr
subject = "tongyongjishu"
for subject in SUBJECT:
#   mi.small(subject)
#   mo.optionStatistics(subject)
#   mos.overall_province(subject)
#   mos.overall_city(subject)
    msr.scoreRangeStatistics(subject)
    pass