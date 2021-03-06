$(function() {
    $(".edit").click(function(e) {
        e.preventDefault();
        var array = e.target.id.split("_");
        var form = $("#editpost_"+array[1]);
        form.prev().addClass("hidden");
        form.removeClass("hidden");
        $(form).find("button").first().click(function(){
            form.prev().removeClass("hidden");
            form.addClass("hidden");
        })
    });

    $(".reply").click(function(e) {
        e.preventDefault();
        var array = e.target.id.split("_");
        var form = $("#replypost_"+array[1]);
        form.removeClass("hidden");
        $(form).find("button").first().click(function(){
            form.addClass("hidden");
        })
    });

    $(".flag").click(function(e) {
        e.preventDefault();
        $("#flag_alert").removeClass("hidden");
        $("#flag_alert").css("top",e.pageY).css("left",e.pageX);
        $("#flag_alert a.yes")[0].href = $(e.target).data("url");

    });
    $("#flag_alert a.no").click(function(e) {
        e.preventDefault();
        $("#flag_alert").addClass("hidden");
    });

});