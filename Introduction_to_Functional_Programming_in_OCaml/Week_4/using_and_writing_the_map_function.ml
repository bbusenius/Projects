type 'a tree =
    Node of 'a tree * 'a * 'a tree
  | Leaf of 'a;;

(* 
 * Transforms list of elements 'a into a list 
 * of singleton lists, e.g. wrap [1;2;3] 
 * should return [[1];[2];[3]] 
 *) 
let wrap l = 
  match l with
  | [] -> [[]]
  | h::t -> [[h]] @ List.map (function e -> [e]) t ;; 


(* 
 * Takes a binary tree and returns a tree of 
 * the same value where each leaf is the value 
 * of the original with the function f applied 
 * to it. 
 *)
let rec tree_map f = function
  | Leaf a -> Leaf (f a)
  | Node (lt, a, rt) -> 
      Node (tree_map f lt, f a, tree_map f rt);;



