type 'a bt =
  | Empty
  | Node of 'a bt * 'a * 'a bt ;;

exception Unbalanced of int ;;

let rec height = function
  | Empty -> 0
  | Node (t, _, t') -> 1 + (max (height t) (height t')) ;;

(* Helper function gets the first element of a tuple *)
let get_1_2 (a,_) = a;;
let get_2_2 (_,a) = a;;

let height t = 
  let rec helper t count =
    let c = count + 1 in
    match t with
    | Empty -> (0, c)
    | Node (t, _, t') -> 
        1 + (max (get_1_2(helper t c)) (get_1_2(helper t' c))), c
  in helper t 1;;



height
  (Node
    (Node
      (Node (Node (Node (Empty, -5, Empty), 3, Node (Empty, 0, Empty)), 0,
        Node (Node (Empty, -5, Empty), -4, Node (Empty, 3, Empty))),
      0,
      Node (Node (Node (Empty, -5, Empty), 3, Node (Empty, 2, Empty)), -3,
       Node (Node (Empty, -1, Empty), -1, Node (Empty, 1, Empty)))),
    -2,
    Node
     (Node (Node (Node (Empty, 4, Empty), 2, Node (Empty, 3, Empty)), 2,
       Node (Node (Empty, 3, Empty), -5, Node (Empty, -1, Empty))),
     -2,
     Node (Node (Node (Empty, -3, Empty), -3, Node (Empty, 3, Empty)), 4,
      Node (Node (Empty, -4, Empty), -4, Node (Empty, 0, Empty))))));;



height (Node (Node (Empty, 't', Empty), 'k', Node (Empty, 'l', Empty)));;

(* (1,2) *)
height (Node (Empty, 'd', Empty));;
