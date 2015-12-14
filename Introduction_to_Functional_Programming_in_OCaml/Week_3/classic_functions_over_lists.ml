(* Search a list for x *)
let rec mem x l = 
  match l with
  | [] -> false
  | [z] -> x = z 
  | z :: zs -> x = z || mem x zs;;

(* Concatonate two lists *)
let rec append l1 l2 = l1 @ l2;;

(* Make a list of tuple pairs from lists of an equal length *)
let rec combine (l1:int list) (l2:int list) =
  match (l1, l2) with
  | [], [] -> []
  | [x], [y] -> [(x,y)]
  | [x1;x2], [y1;y2] -> [(x1,y1);(x2,y2)]
  | x::xs, y::ys -> let pairs = combine xs ys in [x,y] @ pairs;;

(* Search for a pair that has k as the first element *)
let rec assoc l k =
  match l with
  | x::[] -> let a, b = x in if a = k then Some b else None
  | x::xs -> let a, b = x in if a = k then Some b else assoc xs k;;




assoc [("for", 38); ("begin", 42); ("if", 11); ("let", 73); ("done", 3); ("ocp", 9)] "if";;
assoc [("if", 38); ("do", 62); ("sig", 3); ("module", 11); ("struct", 12)] "open";;

