COLORS = ["red", "green", "blue", "white", "magenta", "yellow", "cyan",  "black", "orange"];

function leiabox() {
    onVolumeChange = function() {
        //console.log("VolumeChange");
        volume = $("#slider-volume").slider("value");
        $("#volume-setPoint").text(volume);
        if (leiabox.postUI) {
            leiabox.sendVolume(volume);
        }
    }

    onVolumeStartSlide = function() {
        console.log("startSlide");
        leiabox.volumeSliding=true;
    }

    onVolumeStopSlide = function() {
        console.log("stopSlide");
        leiabox.volumeSliding=false;
    }

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

    onProgram3 = function() {
        var button_selector = "#program3";
        console.log("program3");
        if (leiabox.postUI) {
            leiabox.sendProgram(3);
        }
    }

    onButtonDown = function(value) {
        console.log("sendButtonDown " + value);
        $.ajax({url: "/leiabox/buttonDown?value=" + value});
    }

    onButtonUp = function(value) {
        console.log("sendButtonUp " + value);
        $.ajax({url: "/leiabox/buttonUp?value=" + value});
    }

    sendProgram = function(value) {
        $.ajax({url: "/leiabox/setProgram?value=" + value});
    }

    sendVolume = function(value) {
        console.log("sendVolume " + value);
        $.ajax({url: "/leiabox/setVolume?value=" + value});
    }

    initButtons = function() {
        $("#slider-volume").slider({min: 50,
                                    max: 100,
                                    change: this.onVolumeChange,
                                    start: this.onVolumeStartSlide,
                                    stop: this.onVolumeStopSlide});
        $("#program0").click(function() { leiabox.onProgram0(); });
        $("#program1").click(function() { leiabox.onProgram1(); });
        $("#program3").click(function() { leiabox.onProgram3(); });

        for (var i=0; i<32; i++) {
            (function(i) {
                $("#button"+i).mousedown(function() { leiabox.onButtonDown(i); });
                $("#button"+i).mouseup(function() { leiabox.onButtonUp(i); });
            })(i);
        }
    }

    parseSettings = function(settings) {
        //console.log(settings);
        this.postUI = false;
        try {
            if (!leiabox.volumeSliding) {
                $("#slider-volume").slider({value: settings.volume});
            }
            $("#volume-moving").text("");
        }
        finally {
            this.postUI = true;
        }
    }

    requestSettings = function() {
        $.ajax({
            url: "/leiabox/getStatus",
            dataType : 'json',
            type : 'GET',
            success: function(newData) {
                leiabox.parseSettings(newData);
                setTimeout("leiabox.requestSettings();", 1000);
            },
            error: function() {
                console.log("error retrieving settings");
                setTimeout("leiabox.requestSettings();", 5000);
            }
        });
    }

    start = function() {
         this.postUI = true;
         this.initButtons();
         this.requestSettings();
    }

    return this;
}

$(document).ready(function(){
    leiabox = leiabox()
    leiabox.start();
});

