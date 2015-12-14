type index = Index of int

let read a index =  
  match index with 
  | Index n -> a.(n);;

let inside a index =
  match index with 
  | Index n -> n >= 0 && n < Array.length a;;

let next index =
  match index with 
  | Index n -> let t = n+1 in Index t;;

let min a =
  let b = Array.copy a in 
  Array.sort compare b; b.(0);; 

let min_index a =
  let rec helper a n = 
    if a.(n) = min a
    then Index n
    else helper a (n+1) in
  helper a 0;;

let min_index_FAIL a =
  let rec loop i = 
    let cv = a.(i) in 
    let nv = a.(i-1) in
    let min = if cv < nv then Index i else Index (i-1) in
    if i-1 = 0 then min else loop(i-1) 
  in
  loop (Array.length a - 1);;
