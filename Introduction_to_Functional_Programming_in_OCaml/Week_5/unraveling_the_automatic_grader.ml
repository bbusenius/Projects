type report = message list
and message = string * status
and status = Successful | Failed;;

type 'a result = Ok of 'a | Error of exn;;

(* Call the given function on the given argument. 
 * Return Ok with the result if everything goes well or 
 * Error with the exception raised on failure *)
let exec f x =
  try 
    Ok(f x) 
  with
  | x -> Error (x);;


(* compare : 'a result -> 'a result -> ('a -> string) -> message *) 
(* let compare (user : 'a result) (reference : 'a result) (to_string : ('a -> string)) : message = *)
let compare user reference to_string = 
  match user with 
  | Ok a ->  
      if user = reference 
      then ("got correct value "^to_string a, Successful)
      else ("got unexpected value "^to_string a, Failed)
  | Error a -> 
      if user = reference 
      then ("got correct exception "^exn_to_string a, Successful)
      else ("got unexpected exception "^exn_to_string a, Failed)
