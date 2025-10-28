# mf

_Maja's file manager_

## Feats

- h | [left] : move to parent dir
- l | [right] : move to child dir / preview file
- j | [up] : move cursor up
- k | [down] : move cursor down

## Architecture

- load working dir
- loop:
  - getcommand
  - update data
  - draw screen

- data
  - left : all data about the left screen - filebrowser
    - fnames : list of filenames in working directory
    - idx : index of curently selected file
    - selection : set of selected indexes
    - path : working dir
    - offset : start drawing fname list after offset files (scrolling)

  - right : all data about preview pane
    - this is currently a bit undefined, probably will have to have more than one type of content


## TODO

- [ ] scrolling - offset use
- [ ] move to parent
- [ ] move to child
- [ ] txt preview
- [ ] img preview

