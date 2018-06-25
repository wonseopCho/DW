(function($) {

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
        console.log('listicletest');
        $('#id_category').change(
            function(){
                articleUpdate($('#id_category option:selected').val()); 
        });

        function articleUpdate(id){
            var updates={};
            updates.pk = parseInt(id);
            $.ajax({
              url:"/tips/listicle_admin/",
              method:"post",
              data: updates,
              success: function(res){
                $("#id_articles").html("");
                $(".sortedm2m-items").html("");
                var i=0;
                $.each(res, function(key, value){
                    // console.log("-->",i++, key, value);
                    $("#id_articles").prepend("<option value='"+key+"'>"+value+"</option>");
                     $(".sortedm2m-items").append(`<li class="sortedm2m-item"><label for="id_articles_`+i+`"><input type="checkbox" value="`+key+`" required="" id="id_articles_`+i+`" class="sortedm2m">`+value+`</label></li>`);
                });
              }, error: function(error){
                console.log(error);
                console.log("error");
              }
            });
        };
    });
})(django.jQuery);

