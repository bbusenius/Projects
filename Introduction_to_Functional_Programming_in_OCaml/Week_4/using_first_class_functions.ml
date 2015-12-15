type int_ff = int -> int;;

(* WTF?? *)
let rec compose = function 
  | [] -> fun x -> x 
  | f::g -> fun x -> f((compose g) x) ;;

 compose [((-) 7); ((/) 4); ((+) 10); ((-) 7)] 2;;

(* The function fixedpoint applies repetitively f to the result 
 * of its previous application, starting from start, until it 
 * reaches a value y where the difference between y and (f y) is 
 * smaller than delta. In that case it returns the value of y. 
 * For instance, fixedpoint cos 0. 0.001 yields approximately 0.739
*)
let rec fixedpoint f start delta =
  match start with
  | y -> if abs_float(y -.(f y)) < delta then y else fixedpoint f (f y) delta;;


fixedpoint cos 0. 0.001;;
