import seaborn as sns

import matplotlib as mpl

import matplotlib.cm as cm
from cycler import cycler


pad = 0.0
n_colors = 2
sns.set(style="darkgrid")
cmap = cm.get_cmap('cividis')
mpl.rcParams['image.cmap'] = 'viridis'
mpl.rcParams['axes.prop_cycle'] = cycler('color', [cmap(pad + (1-2*pad)*i/(n_colors-1.)) for i in range(n_colors)])
mpl.rcParams['text.usetex'] = False
mpl.rcParams['text.latex.preamble'] = r"""
\usepackage{amsmath}
\usepackage{amssymb}

\newcommand{\filename}[1]{\emph{\replunderscores{#1}}}

\makeatletter
% \expandafter for the case that the filename is given in a command
\newcommand{\replunderscores}[1]{\expandafter\@repl@underscores#1_\relax}

\def\@repl@underscores#1_#2\relax{%
    \ifx \relax #2\relax
        % #2 is empty => finish
        #1%
    \else
        % #2 is not empty => underscore was contained, needs to be replaced
        #1%
        \textunderscore
        % continue replacing
        % #2 ends with an extra underscore so I don't need to add another one
        \@repl@underscores#2\relax
    \fi
}
\makeatother
"""