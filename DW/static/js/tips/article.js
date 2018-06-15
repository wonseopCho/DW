
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
            <div style="float:left;width:88%;height:30px;border:0px solid red;margin-left:4px">
              <div class="form-group" style="border:0px solid red;">
                <div class="input-group input-file" name="video" id="id_video">
                  <span class="input-group-btn">
                    <button class="btn btn-default btn-choose" type="button" style="height:30px;padding-top:4px"><i class="note-icon-video"></i></button>
                  </span>
                  <input id="_file" type="text" style="height:30px" class="form-control" placeholder='Choose a file...' />
                  <span class="input-group-btn">
                     <button class="btn btn-warning btn-reset" type="button" style="height:30px">Reset</button>
                  </span>
                </div>
              </div>
            </div>`);
      $('#summernote').css('border','1px solid red');

      bs_input_file();   
    });
  };
  $('#summernote').on('summernote.image.upload', function(we, files) {
     console.log(we, files);
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

