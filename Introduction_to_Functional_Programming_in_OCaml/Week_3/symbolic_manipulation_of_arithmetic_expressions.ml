type exp =
  | EInt of int
  | EAdd of exp * exp
  | EMul of exp * exp

let example =
  EAdd (EInt 1, EMul (EInt 2, EInt 3))

let my_example = 
  EAdd (EMul (EInt 2, EInt 2),  EMul (EInt 3, EInt 3));;

let eval e =
  let rec trav = function
    | EInt a -> a
    | EAdd (EInt a, EInt b) -> a + b
    | EMul (EInt a, EInt b) -> a * b 
    | EAdd (exp1, exp2) -> trav exp1 + trav exp2
    | EMul (exp1, exp2) -> trav exp1 * trav exp2
  in trav e
;;

(* a * b + a * c then a * (b + c) *)
let factorize_OLD e = 
  match e with
  | EAdd (EMul (EInt a1, EInt b), EMul(EInt a2, EInt c)) -> 
      if a1 = a2 then
        EMul(EInt a1, EAdd(EInt b, EInt c))
      else e
  | e -> e ;;

(* a * b + a * c then a * (b + c) *)
let factorize e = 
  match e with
  | EAdd (EMul (a1, b), EMul(a2, c)) -> 
    if a1 = a2 then
      EMul(a1, EAdd(b, c))
    else e
  | e -> e ;;

(* a * (b + c) into a * b + a * c *)
let expand = function
  | EMul (a, EAdd (b,c)) -> EAdd (EMul (a,b), EMul (a,c))
  | expr -> expr ;;

(* Simplify an expression *)
let simplify e =
  match e with
  | EAdd (EInt 0, e) -> e
  | EAdd (e, EInt 0) -> e
  | EMul (EInt 0, e) -> EInt 0
  | EMul (e, EInt 0) -> EInt 0
  | EMul (EInt 1, e) -> e
  | EMul (e, EInt 1) -> e
  | e -> e;;
