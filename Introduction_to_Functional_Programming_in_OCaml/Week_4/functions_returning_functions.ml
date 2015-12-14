(* Function definition using explicit mattern matching*)
let rec equal_on_common l1 l2 = match l1,l2 with
  | [],_ -> true
  | _,[] -> true
  | h1::r1,h2::r2 -> h1=h2 && equal_on_common r1 r2;;

(* Same as above, using nested functions *)
(*let rec equal_on_common = fun l1 l2 -> l1 = l2;;*) 
let rec equal_on_common = function
  | [] -> (function _ -> true)
  | h1::r1 -> 
    function 
    | [] -> true
    | h2::r2 -> h1=h2 && equal_on_common r1 r2;;
