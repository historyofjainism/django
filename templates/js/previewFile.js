const viewerConfig = {
    embedMode: "LIGHT_BOX"
  };

previewFile = function(file_url, file_title ) {

    {% if APP_ENVIRONMENT == "production" %}

    firebase.analytics().logEvent('File Open', {
      page: document.title,
      file: file_title
    });

    {% endif %}
    
    /* Initialize the AdobeDC View object */
    var adobeDCView = new AdobeDC.View({
        /* Pass your registered client id */
        clientId: "5f8d647bc3304af5ae8ad2841f30aeca"
    });

    /* Invoke the file preview API on Adobe DC View object */
    adobeDCView.previewFile({
        /* Pass information on how to access the file */
        content: {
            /* Location of file where it is hosted */
            location: {
                url: file_url,
                /*
                If the file URL requires some additional headers, then it can be passed as follows:-
                header: [
                    {
                        key: "<HEADER_KEY>",
                        value: "<HEADER_VALUE>",
                    }
                ]
                */
            },
        },
        /* Pass meta data of file */
        metaData: {
            /* file name */
            fileName: file_title
        }
    }, viewerConfig);
  }
  


/* Wait for Adobe Document Services PDF Embed API to be ready and enable the View PDF button 
document.addEventListener("adobe_dc_view_sdk.ready", function () {
    document.getElementById("view-pdf-btn").disabled = false;
});*/

/* Function to render the file using PDF Embed API. */
