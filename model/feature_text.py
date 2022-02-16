
feature = "leverage_12m_std"

suffixes = ['_std','_log','_win','_sqrt']

suffix = '_std'

feature.endswith(suffix)

feature[:-len(suffix)]

feature + suffix

feature.removeprefix(suffix)

feature.removesuffix(suffix)
