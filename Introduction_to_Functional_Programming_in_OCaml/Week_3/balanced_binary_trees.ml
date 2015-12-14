(* Representation of a binary tree *)
type 'a bt =
  | Empty
  | Node of 'a bt * 'a * 'a bt ;;

(* Calculate the height of a binary tree *)
let rec height t = 
  match t with
  | Empty -> 0
  | Node (left, _, right) -> 1 + max (height left) (height right)
;;

(* Check of a binary tree is balanced *)
let rec balanced t  =
  match t with 
  | Empty -> true
  | Node (left, _, right) -> 
    height left = height right 
    && balanced left 
    && balanced right;;
