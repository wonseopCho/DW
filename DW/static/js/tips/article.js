
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

function bs_input_file() {
  $('#id_video', parent.document).before(
    function() {
      if ( ! $(this).prev().hasClass('input-ghost') ) {
        var element = $("<input type='file' class='input-ghost' style='visibility:hidden; height:0'>");
        element.attr("name",$(this).attr("name"));
        element.change(function(){
          $('.input-file').find('input').val((element.val()).split('\\').pop());
        });
        $('.input-file').find("button.btn-choose").click(function(){
          console.log('icon_CLicked');
          element.click();
        });
        $('.input-file').find("button.btn-reset").click(function(){
          element.val(null);
          $(this).parents(".input-file").find('input').val('');
          $('#id_video', parent.document).parents(".input-file").find('input').val('');
        });
        $('.input-file').find('input').css("cursor","pointer");
        $('.input-file').find('input').mousedown(function() {
          element.click();
          return false;
        });
        return element;
      }
    }
  );
}

$(document).ready(function(){
  var pContents;
  var ref = document.referrer.split("/")[3];
  if (ref!='admin'){
    $('#summernote').on('summernote.init', function() {
      $(`.note-style,
         .note-font,
         .note-fontname,
         .note-fontsize,
         .note-color,
         .note-para,
         .note-height,
         .note-table,
         .note-view,
         .note-help,
         .btn-sm:has(.note-icon-link),
         .btn-sm:has(.note-icon-video),
         .btn-sm:has(.note-icon-minus)
         `).remove();  
      $('.note-insert').append(`
            <div style="float:left;width:88%;height:30px;border:0px solid blue;margin-left:0px;">
              <div class="form-group" style="border:0px solid red;">
                <div class="input-group input-file" name="video" id="id_video" style="widht:100%;border:0px solid yellow;">
                  <span class="input-group-btn" style="border:0px solid red;width:14%">
                    <button class="btn btn-default btn-choose" type="button" style="width:100%;height:30px;padding-top:4px;border-radius:0px"><i class="note-icon-video"></i></button>
                  </span>
                  <input id="_file" type="text" style="height:30px" class="form-control" placeholder='Choose a file...' />
                  <span class="input-group-btn">
                     <button class="btn btn-warning btn-reset" type="button" style="height:30px">Reset</button>
                  </span>
                </div>
              </div>
            </div>`);
      $('#summernote').css('border','1px solid red');
      $('.note-toolbar .btn-sm').css({'width':'12%'});
      bs_input_file();   
    });
  };
  $('#summernote').on('summernote.image.upload', function(we, files) {
     // console.log(we, files);
     console.log('file',files);
     // $('#summernote').summernote('insertImage', imageUrl);
     // var orientation = 1;
     // var imageUrl = '/media/django-summernote/2018-07-27/afe6ac61-6323-4761-8337-98d60f6c37bb.jpg';
     // var imgNode = $('<img>').attr('src',imageUrl);
     // loadImage.parseMetaData(
     //     files[0],
     //     function (data) {
     //         if (!data.imageHead) {
     //             return;
     //         }
     //         orientation = data.exif.get('Orientation');
     //         console.log('ori', orientation);
             
     //         var pi=loadImage(
     //             imageUrl,
     //             function (img) {
     //                 if(img.type === "error") {
     //                     console.log("Error loading image " + imageUrl);
     //                 } else {
     //                      // $('#summernote').summernote('insertImage', imageUrl);
     //                     // document.querySelector('.panel-body').appendChild(img);
     //                     console.log(img);
     //                 }
     //             },
     //             {maxWidth: 600,orientation: orientation,canvas: false}
     //         );
     //         console.log(pi);
     //         $('#summernote').summernote('insertNode', pi);

     //     }
     // );
     

  });
  $('#summernote').on('summernote.media.delete', function(we, files) {
    console.log(we,"------------",files);
    var src = files[0].src.split("/");
    imageDelete(src.slice(4).join("/"));
  });

  
  // $('#summernote').on('summernote.change', function(we, contents, $editable) {
  //   if(String(pContents).length > String(contents).length){
  //     console.log("pre_",pContents, "new_",contents);
  //   }
  //   pContents = contents;
  // });
});

