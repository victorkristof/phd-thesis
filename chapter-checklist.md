# Chapter Checklist

A checklist for all the steps to do in order to transform a paper into a thesis chapter.

- [ ] Include files from paper folder

```bash=sh
cp path-to-paper-folder/*.{tex,bib} text/path-to-chaper/
cp path-to-paper-folder/fig/*.pdf text/figures/
```

- [ ] Create main.tex file in chapter folder and link to sections

- [ ] Update names and paths to figures in the Latex files

```
vidir text/figures
vim /includegraphics/ **/x-chapter/*.tex
```

- [ ] Compile thesis with `make` and correct compilation errors

- [ ] Add path to root thesis.tex

```vim
argadd *.tex
bufdo 1put! ='%! TEX root = ../thesis.tex'
```

- [ ] Lint Latex files

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

```vim
call ReplaceReference(item, chapter_code)
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
