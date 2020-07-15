window.onload = function() {

    function showStatus() {
        if (document.getElementById('status-1').checked) {
            document.getElementById('statusReport-1').style.display = 'block';
            document.getElementById('statusReport-2').style.display = 'none';
            document.getElementById('statusReport-3').style.display = 'none';
            document.getElementById('statusReport-4').style.display = 'none';
        }
        else if (document.getElementById('status-2').checked) {
            document.getElementById('statusReport-1').style.display = 'none';
            document.getElementById('statusReport-2').style.display = 'block';
            document.getElementById('statusReport-3').style.display = 'none';
            document.getElementById('statusReport-4').style.display = 'none';
        }
        else if (document.getElementById('status-3').checked) {
            document.getElementById('statusReport-1').style.display = 'none';
            document.getElementById('statusReport-2').style.display = 'none';
            document.getElementById('statusReport-3').style.display = 'block';
            document.getElementById('statusReport-4').style.display = 'none';
        } else if (document.getElementById('status-4').checked) {
            document.getElementById('statusReport-1').style.display = 'none';
            document.getElementById('statusReport-2').style.display = 'none';
            document.getElementById('statusReport-3').style.display = 'none';
            document.getElementById('statusReport-4').style.display = 'block';
        }
    }

    document.getElementsByName('status').forEach(element => {
        element.onclick = showStatus()
    }); 
    
    showStatus();
}