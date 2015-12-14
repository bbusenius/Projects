(*
 * Every triangle has a circumscribed circle, 
 * that is a circle that goes through the three 
 * points of a given triangle. 
 *
 * Calculate the radius of a circumscribed circle
 * when given the 3 angles a, b, c of of a triangle 
 * and its circumference s.
 * 
 * Optimize the function to make the calculation
 * with as few operations as possible by using
 * partial function application.
 * 
 *)

(* Get the math right *)
let ccr = fun a -> fun b -> fun c -> fun s -> 
  s /. (2. *. cos(a/.2.) *. 2. *. cos(b/.2.) *. 2. *. cos(c/.2.));;

(* Partially optimized version *)
let ccr a b c = 
  let f1 = (8. *. (cos (a/.2.)))*.((cos (b/.2.)))*.((cos (c/.2.)))
  in fun s ->  s /.f1;;

(* Weird version that kinda works *)
let ccr a b c =
  let fa a = (2. *. cos(a/.2.)) in 
  let fb b = (2. *. cos(b/.2.)) in 
  let fc c = (2. *. cos(c/.2.)) in 
  let f1 = fa a *. fb b *. fc c
  in fun s ->  s /.f1;;

(* Another weird version *)
let ccr = fun a -> fun b -> fun c -> fun s -> 
  let fa = (2. *. cos(a/.2.)) in 
  let fb = (2. *. cos(b/.2.)) in   
  let fc = (2. *. cos(c/.2.)) in  
  let f1 = fa *. fb *. fc in
  let fs = s /. f1 in fs ;;

(* Fully optimize the above function 
using partial function application *)



