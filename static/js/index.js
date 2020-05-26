var NavOpen = false;
var ModalOpen = false;
/* Set the width of the sidebar to 250px (show it) */
function openNav() {
    NavOpen = true;
    document.getElementById("mySidepanel").style.width = "50%";
    document.getElementById("open_button").style.visibility = "hidden";

}

/* Set the width of the sidebar to 0 (hide it) */
function closeNav() {
    NavOpen = false;
    document.getElementById("mySidepanel").style.width = "0%";
    document.getElementById("open_button").style.visibility = "visible";
}

window.onload = function(){
// Get the modal
    var modal = document.getElementById("myModal");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks on the button, open the modal
    document.getElementById("socialBtn").onclick = function() {
        ModalOpen = true;
        modal.style.display = "block";
    }

    $( document ).click(function( event ) {

        var target = $( event.target );
        //console.log(target)
        if(NavOpen == true && ModalOpen == false){
            if(!(target.is( 'div#mySidepanel.sidepanel') || target.is('a')  ) ){
                closeNav();
            }
            if(target.is('a.closebtn'))
                closeNav()
        } 
        else if(ModalOpen == true){ 
            if (target.is(modal) || target.is(span)) {
                ModalOpen = false;
                modal.style.display = "none";
            }
        }
        else if(ModalOpen == false && NavOpen == false){
            if(target.is( 'button.openbtn')){
                openNav();
            }
        }
    });
}