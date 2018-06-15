COLORS = ["red", "green", "blue", "white", "magenta", "yellow", "cyan",  "black", "orange"];

function leiabox() {
    onProgram0 = function() {
        var button_selector = "#program0";
        console.log("program0");
        if (leiabox.postUI) {
            leiabox.sendProgram(0);
        }
    }

    onProgram1 = function() {
        var button_selector = "#program1";
        console.log("program1");
        if (leiabox.postUI) {
            leiabox.sendProgram(1);
        }
    }

    sendProgram = function(value) {
        $.ajax({url: "/leiabox/setProgram?value=" + value});
    }

    initButtons = function() {
        $("#program0").click(function() { leiabox.onProgram0(); });
        $("#program1").click(function() { leiabox.onProgram1(); });
    }

    start = function() {
         this.postUI = true;
         this.initButtons();
    }

    return this;
}

$(document).ready(function(){
    leiabox = leiabox()
    leiabox.start();
});

