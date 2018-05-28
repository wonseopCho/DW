
$(function(){
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    }); 
  });

function getCookie(c_name)
{
  if (document.cookie.length > 0)
  {
      c_start = document.cookie.indexOf(c_name + "=");
      if (c_start != -1)
      {
          c_start = c_start + c_name.length + 1;
          c_end = document.cookie.indexOf(";", c_start);
          if (c_end == -1) c_end = document.cookie.length;
          return unescape(document.cookie.substring(c_start,c_end));
      }
  }
  return "";
};

$(document).ready(function(){
    $('#summernote').on('summernote.image.upload', function(we, files) {
      // console.log(files);
    });
    $('#summernote').on('summernote.media.delete', function(we, files) {
      // console.log((files));
      var src = files[0].src.split("/");
      imageDelete(src.slice(4).join("/"));
    });

    function imageDelete(file){
        var _delete={};
        _delete.file = file;
        $.ajax({
          url:"/tips/imageDelete/",
          method:"post",
          data: _delete,
          success: function(res){
            if (res == 1){
              console.log(res,"success");
            }
          }, error: function(error){
            console.log(error);
            console.log("error");
          }
        });
    };
});

