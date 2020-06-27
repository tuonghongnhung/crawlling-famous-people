
var name = window.document.getElementById("name").firstChild.nodeValue;
var item;
var id;
var title;
var link_image;
var x;
function getVideo() {
    $.ajax({
        type: 'GET',
        url: 'https://www.googleapis.com/youtube/v3/search',
        async: false,
        data: {
                key: 'AIzaSyCm50J3kYcn868qgkXKA3CGgs_EKn8J9mA',
                q: name,
                part: 'snippet',
                maxResults: 1,
                type: 'video',
                
        },
        success: function(data){
            item = data.items[0];
            id = item.id.videoId;
            title = item.snippet.title;
            link_image = item.snippet.thumbnails.medium.url;
        },
        error: function(response){
            console.log("Request Failed");
        }
    });
}

function play(){
    var img = window.document.getElementById("image");
    var video = window.document.getElementById("video");

    img.style.display = "none";
    video.style.display="block";
    video
}
getVideo();

var img = window.document.getElementById("image");
console.log(link_image);
img.style.backgroundImage = link_image;

