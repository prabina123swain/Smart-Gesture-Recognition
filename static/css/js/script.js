var mybtn = document.getElementById('startbtn');
var myvideo = document.getElementById('video');
var mycanvas = document.getElementById('canvas');
var myphoto = document.getElementById('photo');
var base_data = "";

function sendRequest(base64Data) {
    var type = "json";
    if (base64Data !== "" && base64Data !== null) {
        if (type === "imgtobase") {
            $(".res-part").html("");
            $(".res-part").html(base64Data);
        } else if (type === "basetoimg") {
            var imageData = $("#imgstring").val();
            $(".res-part").html("");
            $(".res-part").append("<img src='data:image/jpeg;base64," + imageData + "' alt='' />");
        } else {
            var url = $("#url").val();
            $("#loading").show();
            $.ajax({
                url: url,
                type: "post",
                cache: false,
                async: true,
                crossDomain: true,
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                data: JSON.stringify({
                    image: base64Data
                }),
                success: function (res) {
                    $(".res-part").html("");
                    $(".res-part2").html("");
                    var imageData = res.image;
                    $(".res-part2").append("<img class='resp-img' src='data:image/jpeg;base64," +
                        imageData + "' alt='' />");
                    $("#loading").hide();
                }
            });
        }
    }
}

$(document).ready(function () {
    $("#loading").hide();

    $('#send').click(function () {
        sendRequest(base_data);
    });

    $('#uload').click(function () {
        $('#fileinput').focus().trigger('click');
    });

    $("#fileinput").change(function () {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                var url = e.target.result;
                var img = new Image();
                img.crossOrigin = 'Anonymous';
                img.onload = function () {
                    var canvas = document.createElement('CANVAS');
                    var ctx = canvas.getContext('2d');
                    canvas.height = this.height;
                    canvas.width = this.width;
                    ctx.drawImage(this, 0, 0);
                    base_data = canvas.toDataURL('image/jpeg', 1.0).replace(
                        /^data:image.+;base64,/, '');
                    canvas = null;
                };
                img.src = url;
                $('#photo').attr('src', url);
                $('#photo').show();
                $('#video').hide();
            };
            reader.readAsDataURL(this.files[0]);
        }
    });
});
