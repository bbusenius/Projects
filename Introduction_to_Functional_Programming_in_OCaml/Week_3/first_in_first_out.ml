(* Define a queue type *)
type queue = int list * int list

(* Test for an empty list *)
let is_empty (front, back) =
  match (front, back) with 
  | ([], []) -> true
  | ([x], [y]) -> false
  | ([x], []) -> false
  | ([], [y]) -> false
  | ([], x::y) -> false
  | (x::y, []) -> false
  | (x::y, a::b) -> false;;

(* Enqueue *)
let enqueue x (front, back) = 
  front, [x] @ back;;

(* Calculate lenth of a list *)
let rec len = function
  | [] -> 0
  | x :: xs -> 1 + len xs;;

(* Reverse a list *)
let rec rev = function
| [] -> []
| x :: xs -> rev xs @ [ x ];;
	
(* Split a list... *)
let split (l :int list) =
  let rec helper ((front :int list), (back :int list)) (accu :int list) =
    match (front, back) with
    | xs, ([] | [_]) -> (List.rev accu, xs)
    | [], _ -> ([], [])
    | x::xs, y::y'::ys -> let t = x::accu in helper (xs, ys) t
  in
  let z1, z2 = helper (l, l) [] in rev z2, z1;;

(* Dequeue *)
let dequeue ((front:int list), (back:int list)) =
  match front, back with 
  | [], _ -> let x::xs, q = split back in (x, (xs, q))
  | x::xs, q -> x, (xs, q)
;;



