(* Calculate the product of the values 
 * of two lists. Example from the video *)
let product v1 v2 = 
  List.fold_left (+) 0 (List.map2 ( * ) v1 v2 );;

product [2;4;6] [1;3;5];;


(* Count the number of elements l that
 * satisfy p. Example from the video *)
let countif p l = List.fold_left
  (fun counter element -> 
    if p element then counter+1 else counter ) 0 l;;

countif (function x -> x > 0) [3;-17;42;-73;-256];;


(* Filter the elements of a list and return
 * a new list without the elements that
 * fail to satisfy the given criteria *)
let filter p l =
  List.fold_right (fun x a -> if p x then x :: a else a) l []


(* The real way *)
let filter2 = List.filter;;

filter (function x -> x > 0) [3;-17;42;-73;-256];;


(* Function that takes a predicate p and a 
 * list l and returns a pair of two lists where 
 * lpos is the list of all elements of l that 
 * satisfy p, and lneg is the list of all elements 
 * that do not satisfy p. NOTE TO SELF: 
 * x::l adds x to the head of a list l *)
let partition p l = List.fold_right
  (fun x (l,r) -> if p x then (x::l,r) else (l,x::r)) 
  l ([],[]);;


(* Implement the quicksort algorithm: 
 * https://en.wikipedia.org/wiki/Quicksort *)
let rec sort = function
    | [] -> []
    | h::r -> 
        let smaller, larger = List.partition (fun y -> y < h) r
          in sort smaller @ (h::sort larger)
