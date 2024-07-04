## Creating onslide references with tikz

Define a new commmand

```
\usepackage{tikz}
\newcommand{\reference}[1]{%
    \begin{tikzpicture}[remember picture, overlay]
        \node [anchor=south west, xshift=0.7cm, yshift=0.65cm, text=kit-gray50, text width=\linewidth, execute at begin node=\setlength{\baselineskip}{1pt}] at (current page.south west){
            \tiny #1
        };
    \end{tikzpicture}
    }
```

Then use with e.g. ``\reference{[1] Degrave, et al. "Magnetic control of tokamak plasmas through deep reinforcement learning."}``.
Place footnote marks with ``\footnotemark{1}`` If you include one as above.
For multiple references on one slide add them with linebreaks in the same command.
