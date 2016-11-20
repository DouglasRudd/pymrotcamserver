var __coord = 'REL'
var __axis = 'X' //X,Y
var __direction = 1 //1: forward , -1: backward
var __angle = 5 //in degree


function renew_position(data){
    $('#X').html(data.X);
    $('#Y').html(data.Y); 
}

function get_renew_position() {
   $.get("/position",renew_position,"json") 
   //
   //var d = new Date();
   //document.getElementById("X").innerHTML = d.toLocaleTimeString();
}

function manual_axis_control(){
    $.post("/control",{
        coord : __coord,
        axis : __axis,
        direction : __direction,
        angle : __angle
    });
}

// binding job mode buttons
$(document).ready(function(){
    $("button").click(function(){                    
        var sender = $(this);
        __coord = 'REL';
        __axis = sender.data('axis');
        __direction = sender.data('dir');
        __angle = $('#angle').val();
        manual_axis_control();
    });

    var __timer = setInterval(get_renew_position,1000);

});
