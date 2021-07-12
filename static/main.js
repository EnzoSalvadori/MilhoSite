document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
  const dropZoneElement = inputElement.closest(".drop-zone");

  dropZoneElement.addEventListener("click", (e) => {
    inputElement.click();
  });

  inputElement.addEventListener("change", (e) => {
    if (inputElement.files.length) {
      updateThumbnail(dropZoneElement, inputElement.files[0]);
    }
  });

  dropZoneElement.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZoneElement.classList.add("drop-zone--over");
  });

  ["dragleave", "dragend"].forEach((type) => {
    dropZoneElement.addEventListener(type, (e) => {
      dropZoneElement.classList.remove("drop-zone--over");
    });
  });

  dropZoneElement.addEventListener("drop", (e) => {
    e.preventDefault();

    if (e.dataTransfer.files.length) {
      inputElement.files = e.dataTransfer.files;
      updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
    }

    dropZoneElement.classList.remove("drop-zone--over");
  });
});

$(function( $ ){
  $('form').on('submit', function (event) {
    event.preventDefault();
    var imagem = document.getElementById("imagem");
    var botao = document.getElementById("botao");
    var barra = document.getElementById("barra");
    if (imagem.value == ""){
      alert('Por favor selecione um arquivo para envio');
      return;
    }
    botao.innerHTML = "Fazendo upload";
    botao.disabled = true;
    var formData = new FormData($('form')[0]);
    $.ajax({
      xhr : function() {
				var xhr = new window.XMLHttpRequest();
				xhr.upload.addEventListener('progress', function(e) {
					if (e.lengthComputable) {
            var percent = Math.round((e.loaded / e.total) * 100);
            barra.style.visibility = "visible";
						$('#progressBar').attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');
					}
				});
				return xhr;
			},
      type: 'POST',
      url: '/upload/',
      data: formData,
      processData: false,
      contentType: false,
      success: function () {
        window.location.href = '/processando/'
      }
    });
  });
});

/**
 * Updates the thumbnail on a drop zone element.
 *
 * @param {HTMLElement} dropZoneElement
 * @param {File} file
 */
function updateThumbnail(dropZoneElement, file) {
  var imagem = document.getElementById("imagem");
  var formato = imagem.value.split(".");
  formato = (formato[formato.length - 1]).toUpperCase()
  if (formato != "PNG" && formato != "TIF" && formato != "TIFF" && formato != "JPEG" && formato != "JPG") {
    alert("O arquivo enviado não possui um dos formatos suportados (PNG) (JPEG) (JPG) (TIF) (TIFF)");
    imagem.value = "";
    return;
  }

  let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

  // First time - remove the prompt
  if (dropZoneElement.querySelector(".drop-zone__prompt")) {
    dropZoneElement.querySelector(".drop-zone__prompt").remove();
  }

  // First time - there is no thumbnail element, so lets create it
  if (!thumbnailElement) {
    thumbnailElement = document.createElement("div");
    thumbnailElement.classList.add("drop-zone__thumb");
    dropZoneElement.appendChild(thumbnailElement);
  }

  thumbnailElement.dataset.label = file.name;

  // Show thumbnail for image files
  if (file.type.startsWith("image/")) { 
    if(file.name.split('.').pop().toUpperCase() == "TIFF" || file.name.split('.').pop().toUpperCase() == "TIF"){
      thumbnailElement.style.backgroundImage = 'url("/static/placeholder.jpg")';
      return;
    }
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
    };
  } else {
    thumbnailElement.style.backgroundImage = null;
  }
}
