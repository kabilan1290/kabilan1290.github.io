function test(){
  var x = document.getElementById('search').value;
  document.getElementById("demo").innerHTML = x;

}

function test2(){
	var a = ['ɑ','Α','α'][Math.floor(Math.random() * 3)];

	var b = ['Ь','β'][Math.floor(Math.random() * 3)];

	var c="Ϲ"

	var d=['ԁ','ժ']

    var obj ={'a':'ɑ','b':'Ь','ԁ':'ժ','c':"Ϲ","e":"Е","f":"Ϝ","g":"ɢ","h":"Η","i":"і","j":"ј","k":"κ","l":"ι","m":"Ϻ","n":"ɴ","o":"ο","p":"ρ","q":"Ⴓ","r":"ʀ","s":"ѕ","t":"τ","u":"υ","v":"ѵ","w":"ѡ","x":"χ","y":"у","z":"Ζ"}


  	var x = document.getElementById('search').value;
 	var final ="";	
 	var h = "https://";
 	 for (var i = 0; i < x.length; i++) {
 	 	var temp = x;

 	 	if (x.charAt(i) in obj){
 	 			n = obj[x.charAt(i)]
 	 			var_i = x.charAt(i)
 	 			t=x.replace(var_i,n);
 	 			
 	 			final =final+h+t+("\n")+("\n")

	 	 	}
	
		}



	
	swal({
  text: final
});
}