type 'a clist =
  | CSingle of 'a
  | CApp of 'a clist * 'a clist
  | CEmpty;;

let example =
  CApp (CApp (CSingle 1,
              CSingle 2),
        CApp (CSingle 3,
              CApp (CSingle 4, CEmpty)));;

(* Non-efficient version using @ *)
let rec to_list = function
  | CSingle x -> [x]
  | CApp (a,b) -> (to_list a) @ (to_list b)
  | CEmpty -> [];;

(* Efficient version in linear time *)
let rec to_list l =
  let rec tol l acc =
    match l with
    | CEmpty -> acc
    | CSingle x -> x::acc
    | CApp (l1, l2) -> tol l1 (tol l2 acc)
  in tol l [];;


let rec of_list l =
  match l with
  | [] -> CEmpty
  | [a] -> CSingle a
  | a::rest -> CApp (CSingle a, of_list rest)
;;

let append l1 l2 =
  match l1, l2 with
  | CEmpty, l2 -> l2
  | l1, CEmpty -> l1
  | l1, l2 -> CApp (l1, l2);;

let hd l = 
  match l with
  | x -> let f = to_list x in 
    match f with
    | [] -> None 
    | a::b -> Some a;; 

let tl l = 
  let nl = to_list l in
  match nl with
  | a::b -> hd (of_list b);;
  
let tl l = 
  let nl = to_list l in 
  match nl with
  | [] -> None
  | a::b -> let c = of_list b in
    match c with
    | a -> Some a;;
