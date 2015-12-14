type int_ff = int -> int;;

(* WTF?? *)
let rec compose = function 
  | [] -> fun x -> x 
  | f::g -> fun x -> f((compose g) x) ;;

 compose [((-) 7); ((/) 4); ((+) 10); ((-) 7)] 2;;

(* Double WTF?? *)
let rec fixedpoint f start delta =
  "WTF";;
