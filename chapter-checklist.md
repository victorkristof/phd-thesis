# Chapter Checklist

- [ ] Include files from paper folder

```bash=sh
cp path-to-paper-folder/*.{tex,bib} path-to-chaper/
cp path-to-paper-folder/fig/*.pdf figures/
```

- [ ] Update names and paths to figures in the Latex files

```
vidir figures
vim /includegraphics/ *.tex
```

- [ ] Add path to root thesis.tex

```vim
bufdo 1put! ='%! TEX root = ../thesis.tex'
```

- [ ] Lint Latex files with ALE

```bash=sh
./lint.sh chapter-folder/*.tex
```

- [ ] Replace tab: by {chapter}:tab:
- [ ] Replace eq: by {chapter}:eq:
- [ ] Replace fig: by {chapter}:fig:
- [ ] Replace sec: by {chapter}:sec:

```vim
vim /{tab:/ *.tex
cdo s/{tab:/{lmp:tab:/c
```

- [ ] Add ~ before \ref
- [ ] Add ~ before \eqref
- [ ] Add ~ before \cite

```vim
vim / \\ref/ *.tex
cdo s/ \\ref/\~\\ref/c
```

- [ ] Italicize "i.e."
- [ ] Italicize "e.g."

```vim
vim / i\.e\./ *.tex
cdo s/ i\.e\./ \\textit{i.e.}/c
```

- [ ] Normalize equations
- [ ] Add missing citations
- [ ] Adapt size of tables
- [ ] Adapt size of figures
- [ ] Generate figures with correct size and font
- [ ] Adapt "Related Work" to mention introduction
- [ ] Adapt "Abstract" as short introduction to chapter
- [ ] Replace "Conclusion" by "Summary" and "Future Work" by "Perspective"
- [ ] Replace mention to "this paper" by "this chapter"

```vim
vim /\vthis (paper|work)/ *.tex
```
