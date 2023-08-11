1
2
3

#((1 2))

#((r 2)
  (3 4))

((fn (x y) (+ (*2 x) y)) 1 2)

(fn (x y) (+ x x y y))

(? ~ 2 3)

(< (' (1 2 3)))
(> (' (1 2 3)))

(def map
  (fn (lst f)
    (if lst
      (cons (f (< lst))
            (map (> lst) f))
      ~)))

(map (l 1 2 3 4)
  (fn (x) (+ x x x x)))


