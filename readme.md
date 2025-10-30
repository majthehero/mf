# mf

_Maja's file manager_

## Feats

- h | [left] : move to parent dir
- l | [right] : move to child dir / preview file
- j | [up] : move cursor up
- k | [down] : move cursor down
- r | [enter] : run cmd on file / selection - differentiate?

## Architecture

- load working dir
- loop:
  - draw screen
  - getcommand
  - update data

- data
  - left : all data about the left screen - filebrowser
    - fnames : list of filenames in working directory
    - idx : index of curently selected file
    - selection : set of selected indexes
    - path : working dir
    - offset : start drawing fname list after offset files (scrolling)

  - right : all data about preview pane
    - text_lines : list of lines for text previews
    - img_data : for viewing with viu

  - options : flags etc
    - show_hidden - false, flag a
    
## TODO

- [ ] run operation on current file - <cmd> <selected files>, e.g. `[enter] vim [enter]` or `[r] vim [enter]` open file in vim 
- [ ] img preview
- [x] scrolling - offset use
- [x] move to parent
- [x] move to child
- [x] txt preview

