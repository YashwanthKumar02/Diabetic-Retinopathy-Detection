var user=document.querySelector('#username');
user.addEventListener('keyup',function(){
    var u_times=document.querySelector('.u_times');
    var u_check=document.querySelector('.u_check');
    if(user.value.length == 0 || user.value.length < 6){
        user.style.border='1px solid red';
        u_times.style.display='block';
        u_check.style.display='none';
        return false;
    }
    else{
        user.style.border='1px solid green';
        u_times.style.display='none';
        u_check.style.display='block';


    }
})

// var pass=document.querySelector('#password');
// pass.addEventListener('keyup',function(){
//     var p_times=document.querySelector('.p_times');
//     var p_check=document.querySelector('.p_check');
//     if(pass.value.length == 0 || pass.value.length < 10 || pass.value.match(/[0-9]/)==null || pass.value.match(/[A-Z]/)==null || pass.value.match(/[a-z]/)==null || pass.value.match(/[@\!\#\$\%\^\&\*\(\)\_\+\-\=\?\>\<\.\,]/)==null ){
//         pass.style.border='1px solid red';
//         p_times.style.display='block';
//         p_check.style.display='none';
//         return false;
//     }
//     else{
//         pass.style.border='1px solid green';
//         p_times.style.display='none';
//         p_check.style.display='block';
            
//     }
//     }
//     )
// var cpass=document.querySelector('#cpassword');
// cpass.addEventListener('keyup',function(){
//     let password=document.getElementById("password").value;
//     var p_times=document.querySelector('.p_times');
//     var p_check=document.querySelector('.p_check');
//     if(cpass.value==password){
//         cpass.style.border='1px solid green';
//         p_times.style.display='none';
//         p_check.style.display='block';
//     }
//     else{
//         cpass.style.border='1px solid red';
//         p_times.style.display='block';
//         p_check.style.display='none';
//         return false;

//             }
//     }
// )
// function cheackpassword()
// {
//     let password=document.getElementById("password").value;
//     let cpassword=document.getElementById("cpassword").value;
//     if(password==cpassword){
//         alert("passwords match");
//         alert("successfully registered");
//     }
//     else{
//         alert("password didnot match");
//     }
// }



// eyeIcon.addEventListener("click", () => {
//     // Toggle the password input type between "password" and "text"
//     passwordInput.type = passwordInput.type === "password" ? "text" : "password";

//     // Update the eye icon class based on the password input type
//     eyeIcon.className = `fa-solid fa-eye${passwordInput.type === "password" ? "" : "-slash"}`;
// });



let eyeicon =document.getElementById("eyeicon");
let ceyeicon =document.getElementById("ceyeicon");

		let password =document.getElementById("password");
        let cpassword =document.getElementById("cpassword");

		eyeicon.onclick =function(){
			if(password.type =="password"){
				password.type ="text";
				eyeicon.src ='https://res.cloudinary.com/dhva31opb/image/upload/v1686759944/eye-open_a3resw.png';
			}else{
				password.type="password";
				eyeicon.src ="https://res.cloudinary.com/dhva31opb/image/upload/v1686759945/eye-close_aw8s6d.png";
			}

            ceyeicon.onclick =function(){
                if(cpassword.type =="password"){
                    cpassword.type ="text";
                    ceyeicon.src ='https://res.cloudinary.com/dhva31opb/image/upload/v1686759944/eye-open_a3resw.png';
                }else{
                    cpassword.type="password";
                    ceyeicon.src ="https://res.cloudinary.com/dhva31opb/image/upload/v1686759945/eye-close_aw8s6d.png";
                }    
		}
    }    