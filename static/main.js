//It is important to know that Dropzone.js uses ajax to upload files in a queue,
//so your endpoint should process the upload as a singular file not multiple.

Dropzone.autoDiscover=false; //prevent dropzone to automatically discover the dropzone object or the form and initiate it in your html
                             //It is recommanded to initiate form or the dropzone object by hand. This way you can get the dropzone instance and query it about the uploaded files.
const myDropzone = new Dropzone("#my-dropzone",{
    url:"upload/",//dropzone needs a url attribute or it complains, what value you put here does not really matter. It is only purpose is to prevent a javascript error message from chrome console
    maxFiles:4,
    maxFilesize:2,
    parallelUploads:4,
    acceptedFiles:".jpeg,.jpg,.bmp,.png,.gif",
    autoProcessQueue: false,// prevent dropzone from uploading automatically
    init: function () {
        var myDropzone = this;
        // for Dropzone to process the queue (instead of default form behavior):
        document.getElementById("submit-all").addEventListener("click", function(e) {
        // Make sure that the form isn't actually being sent.
        e.preventDefault();
        e.stopPropagation();
        myDropzone.processQueue();
        });


        // Listen to the sendingmultiple event. In this case, it's the sendingmultiple event instead
        // of the sending event because uploadMultiple is set to true.
        this.on("sendingmultiple", function() {
          // Gets triggered when the form is actually being sent.
          // Hide the success button or the complete form.
        });
        this.on("successmultiple", function(files, response) {
          // Gets triggered when the files have successfully been sent.
          // Redirect user or notify of success.
          
  
        });
        this.on("errormultiple", function(files, response) {
          // Gets triggered when there was an error sending the files.
          // Maybe show form again, and notify user of error
        });
        //this.on('error', function(file, response){
        //var resp = JSON.parse(response);
        //alert("code:" + resp.code + ", message: " + resp.message)
        //});
        this.on("error", function(file,message, xhr) {
        this.removeFile(file);
        //show error message
        var d1 = document.getElementById('showerror');
        d1.insertAdjacentHTML('beforeend', '<span style="color:red;font-weight:bold;">'+message+'</span>');
        //alert(message);
        });
        //checks if the file is added, here am using it to remove the error message each time a file is added
        this.on("addedfile", function(file) {
            //clear the error message
            document.getElementById('showerror').innerHTML = "";
        });
        // one upload complete remove files
        this.on("complete", function(file) { 
          document.getElementById("my-dropzone").innerHTML = "";
          document.getElementById("divbtn").innerHTML = "";
          setTimeout(function(){
            window.open("gallery_list", "_self");
         }, 2000);//wait 2 seconds 
          var d1 = document.getElementById('showeMsg');
          d1.insertAdjacentHTML('beforeend', '<span style="color:Green;font-weight:bold;">Images Uploaded Succeefully</span>');
       });
       
 }
});


//Ajax call to upload
    // Submit post on submit

  //  function getCookie(name) {
  //    let cookieValue = null;
  //    if (document.cookie && document.cookie !== '') {
  //        const cookies = document.cookie.split(';');
  //        for (let i = 0; i < cookies.length; i++) {
  //            const cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
  //            if (cookie.substring(0, name.length + 1) === (name + '=')) {
  //                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
  //                break;
  //            }
  //        }
  //    }
  //    return cookieValue;
  //}
  //const csrftoken = getCookie('csrftoken');



    
