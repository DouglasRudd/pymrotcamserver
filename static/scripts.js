$(document).ready(function(){
    $("button").click(function(){                    
        var sender = $(this);
        $.post("/control",{
                name : sender.data('dir'),
                value : $('#angle').val()
        });
    });
});
