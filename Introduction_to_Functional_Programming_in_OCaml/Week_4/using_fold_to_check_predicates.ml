(* Using List.fold_left, write a function 
 * for_all : ('a -> bool) -> 'a list -> bool that 
 * takes as an argument a list l and a predicate 
 * p of type bool. It must return true if and only 
 * if all elements of l satisfy the predicate p *)
let for_all p l = List.fold_left (fun acc v -> acc && (p v)) true l;;


(* Using List.fold_left, write a function exists: 
 * ('a -> bool) -> 'a list -> bool that takes as an 
 * argument a list l  and a predicate p of type bool. 
 * It must returns true if at least one element of l 
 * satisfies the predicate p *)
let exists p l = List.fold_left (fun acc v -> acc || (p v)) false l;;


(* An easier to understand recursive version *)
let rec sorted_simple cmp l = 
  match l with
  | h :: (b :: _ as t) -> cmp b h >= 0 && sorted_simple cmp t 
  | _ -> true ;;


(* Returns the same as above but uses List.fold *)
let sorted cmp l =
  match l with
  | [] -> true
  | h::t-> 
    let bool = List.fold_left 
      (fun option e -> 
	match option with
	| Some(prev_elem) when (cmp prev_elem e) <= 0 -> Some(e)
	| _ -> None) 
      (Some(List.hd l))
      l in if bool = None then false else true;;

sorted (fun x y -> compare y x) [-1; 2; -2; 3; 4; -5; -5];;
sorted compare [-4; 1; 4];;


