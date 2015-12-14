type pair = 
  {index:int; value:int};;

let b = [|5;-20;9;2;-800;-9;1;2|];;
let c = [|-5; -2; -10; -7; -15; -9; 12; -1; 2; -13; -8; -14|];;
let d = [|-1; 3; 4|];;

let smaller (a:int) (b:int) = if a < b then a else b;;

let min a =
  let b = Array.copy a in 
  Array.sort compare b; b.(0);;


let min_index a =
  let rec helper a n = 
    if a.(n) = min a
    then n
    else helper a (n+1) in
helper a 0;;

min b;;
min_index b;;
