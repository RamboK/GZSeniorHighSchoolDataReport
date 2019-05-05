from init_config.property import SUBJECT
import ItemStatistics as mi
import OptionStatistics as mo
import OverallStatistics as mos
import ScoreRange as msr
import city_boxplot as mcb
import dist_boxplot as mdb
import school_boxplot as msb
for subject in SUBJECT:
    mi.small(subject)
    mo.optionStatistics(subject)
    mos.overall_province(subject)
    mos.overall_city(subject)
    msr.scoreRangeStatistics(subject)
    mcb.draw_city_boxplot(subject)
    mdb.draw_dist_boxplot(subject)
    msb.draw_school_boxplot(subject)
