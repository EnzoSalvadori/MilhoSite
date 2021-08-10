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

$(function ($) {

  //fazer uma validação para entrar aqui so no processamento
  if (document.getElementById("img-pro")) {
    $.ajax({
      url: "../json",
      type: 'GET',
      dataType: 'json', // added data type
      success: function (res) {
        console.log(res.data)
        if (res.data == "fila") {
          var div = document.getElementById("div-cont");
          var fila = document.createElement("p");
          fila.style.textAlign = 'center';
          fila.style.fontSize = '2vh';
          fila.style.marginTop = '4vh';
          fila.setAttribute('id', "fila");
          fila.innerHTML = "Seu processamento está na fila de espera, aguarde um instante."
          div.appendChild(fila);
          var fila2 = document.createElement("p");
          fila2.style.textAlign = 'center';
          fila2.style.fontSize = '1.2vh';
          fila2.setAttribute('id', "fila2");
          fila2.innerHTML = "Lembrando que você não precisa aguardar nesta página, assim que seu processamento terminar todos os dados serão enviados no seu e-mail."
          div.appendChild(fila2);
        }
        $('#progressBar').attr('aria-valuenow', res.data).css('width', res.data + '%').text(res.data + '%');
        if (res.data == 100) {
          console.log("terminou")
        }
      }
    });
    const intervalLength = 3000;
    const interval = setInterval(() => {
      $.ajax({
        url: "../json",
        type: 'GET',
        dataType: 'json', // added data type
        success: function (res) {
          $('#progressBar').attr('aria-valuenow', res.data).css('width', res.data + '%').text(res.data + '%');
          if (res.data != "fila") {
            try {
              document.getElementById("fila").remove();
              document.getElementById("fila2").remove();
            } catch (error) {
    
            }
          }
          if (res.data == 100) {
            var div = document.getElementById("div-cont");
            var verimgs = document.createElement("a");
            verimgs.setAttribute("href","../imagens");
            verimgs.style.textAlign = 'center';
            verimgs.innerHTML = "Vizualizar seus resultados";
            div.appendChild(verimgs);
            clearInterval(interval);
          }
        }
      });
    }, intervalLength);
  }
  let xhr = new XMLHttpRequest();
  xhr.open('GET', 'https://viacep.com.br/ws/88040400/json');
  $('form').on('submit', function (event) {
    event.preventDefault();
    var imagem = document.getElementById("imagem");
    var botao = document.getElementById("botao");
    var barra = document.getElementById("barra");
    if (imagem.value == "") {
      alert('Por favor selecione um arquivo para envio');
      return;
    }
    botao.innerHTML = "Fazendo upload";
    botao.disabled = true;
    var formData = new FormData($('form')[0]);
    $.ajax({
      xhr: function () {
        var xhr = new window.XMLHttpRequest();
        xhr.upload.addEventListener('progress', function (e) {
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
    if (file.name.split('.').pop().toUpperCase() == "TIFF" || file.name.split('.').pop().toUpperCase() == "TIF") {
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

