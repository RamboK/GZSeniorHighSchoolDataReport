from Main.init_config.property import SUBJECT
import Main.ItemStatistics as mi
import Main.OptionStatistics as mo
import Main.OverallStatistics as mos
import Main.ScoreRange as msr
import Main.city_boxplot as mcb
import Main.dist_boxplot as mdb
import Main.school_boxplot as msb
for subject in SUBJECT:
    mi.small(subject)
    mo.optionStatistics(subject)
    mos.overall_province(subject)
    mos.overall_city(subject)
    msr.scoreRangeStatistics(subject)
    mcb.draw_city_boxplot(subject)
    mdb.draw_dist_boxplot(subject)
    msb.draw_school_boxplot(subject)