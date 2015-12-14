(* Returns the last element of a list or 
(invalid_arg "last_element") when the list is empty *)
let rec last_element = function [x] -> x
  | [] -> (invalid_arg "last_element") 
  | x::y -> last_element y;;

(* Take a list l as argument, and that check that 
the list is sorted in increasing order according 
to the polymorphic comparison operator < *)
let rec is_sorted = function [] -> true
  | [a] -> true
  | a::b::c -> if a < b then is_sorted (b::c) else false;;

is_sorted [1;2;3;4;5];;
is_sorted [1;3;2;4;5];;
