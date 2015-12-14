(* A type *)
type e = EInt of int | EMul of e * e | EAdd of e * e;;

(* Verbose pattern matching *)
let simplify = function
  | EMul (EInt 1, e) -> e
  | EMul (e, EInt 1) -> e
  | EMul (EInt 0, e) -> EInt 0
  | EMul (e, EInt 0) -> EInt 0
  | EAdd (EInt 0, e) -> e
  | EAdd (e, EInt 0) -> e
  | e -> e

(* A simplified version using "or" patterns *)
let simplify = function
  | EMul (EInt 0, e) | EMul (e, EInt 0) -> EInt 0
  | EMul (EInt 1, e) | EMul (e, EInt 1) | EAdd (EInt 0, e) | EAdd (e, EInt 0) -> e | e -> e;;

(* Verbose pattern matching *)
let only_small_lists = function
  | [] -> []
  | [x] -> [x]
  | [x;y] -> [x;y]
  | _ -> []

(* A simplified version using the "or" and "as" patterns *) 
let only_small_lists = function
  | [] -> []
  | [x] | x::_ as l -> if List.length l > 2 then [] else l;;

(* Verbose pattern matching *)
let rec no_consecutive_repetition = function
  | [] -> []
  | [x] -> [x]
  | x :: y :: ys ->
      if x = y then
        no_consecutive_repetition (y :: ys)
      else
        x :: (no_consecutive_repetition (y :: ys));;

(* A simplified version breaking the expression into 
two distinct cases, dropping the if construct in favor of a when clause *)
let rec no_consecutive_repetition = function
  | [] -> []
  | [x] -> [x]
  | x :: y :: ys when x = y -> no_consecutive_repetition (y :: ys)
  | x :: y :: ys ->  x :: (no_consecutive_repetition (y :: ys));;
