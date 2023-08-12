1
2
3

#((1 2))

#((r 2)
  (3 4))

((fn (x y) (+ (*2 x) y)) 1 2)

(fn (x y) (+ x x y y))

(if ~ 2 3)

(< (' (1 2 3)))
(> (' (1 2 3)))

(def map
  (fn (lst f)
    (if lst
      (cons (f (< lst))
            (map (> lst) f))
      ~)))

(def lfold
  (fn (init lst f)
    (if lst
      (lfold (f init (< lst)) (> lst) f) 
      init)))

(def rfold
  (fn (init lst f)
    (if lst
      (f (< lst) (rfold init (> lst) f))
      init)))

(def reverse
  (fn (lst acc)
    (if lst
      (reverse (> lst) (cons (< lst) acc))
      acc)))

(reverse (l 1 2 3) ~)

(map (l 1 2 3 4) (fn (x)
  (+ x x x x)))

(lfold 0 (l 1 2 3 4) -)
(rfold 0 (l 1 2 3 4) -)

