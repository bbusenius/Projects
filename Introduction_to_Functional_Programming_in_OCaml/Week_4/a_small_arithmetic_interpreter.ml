(* Datatype *)
type operation =
    Op of string * operation * operation
  | Value of int;;

(* Environment *)
type env = (string * (int -> int -> int)) list;;

(* Setup an inital environment constant *)
let initial_env = [("max", max)];;

(* 
 * Return the function associated with a name in 
 * the environment. If there  is no function with 
 * the name given, return invalid_arg "lookup_function" 
 *)
let rec lookup_function n = function      
  | [] ->  invalid_arg "lookup_function"
  | (fn,f)::xs-> if fn=n then f else (lookup_function n xs)

(* Stupid test function only needed to mave the env valid *)
let add a b c =
 a + b + c;; 

(* A stupid min function *)
let mini a b =
  if a < b then a else b;; 

(* Take an environment env, a name for the function name 
 * and a function op, and return a new environment 
 * containing the function op that is associated with 
 * the name n e.g. [("name", op)]
 *)
let add_function name op env =
  env @  [(name, op)];;

(* Make an updated copy of the environment with a
 * lame min function *)
let my_env = add_function "min" mini initial_env;; 

(* Same as above but with a lambda FAIL *)
let my_env = fun a b c d -> add_function "min" (if a < b then a else b) initial_env ;;  

(* Take an environment and an operation description 
 * and computes the operation.
 *
 * The result is either:
 * 
 * Directly the value or
 * An operation that takes two computed values 
 * and a function from the environment.
 *
 *)
let rec compute env op =
  match op with
  | Value x -> x
  | Op (x,y,z) -> let f = lookup_function x env in f (compute env y) (compute env z);;


(* Same as above but done better *)
let rec compute_eff env = function
  | Value x -> x
  | Op (x,y,z) -> lookup_function x env (compute_eff env y) (compute_eff env z);;
