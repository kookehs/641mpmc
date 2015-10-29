./gringo $@ \
    | ./reify \
    | ./clingo --parallel-mode=4 --outf=2 --seed=$RANDOM \
            - \
            metaS.lp \
            ./examples/reify/meta*.lp 1>./example_noshortcut.json 2>/dev/null
