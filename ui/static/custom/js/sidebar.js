$(document).ready(function () {

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('sidebar-expanded sidebar-collapsed');
    });

    //put change active logic here
    $('.components > li').on('click', function() 
    {
        $('.active').removeClass('active');
        $(this).addClass('active');
    });

});





