var Overlay = {
    $overlay: $('<div id="overlay"></div>').appendTo('body'),
    
    show: function() {
        this.$overlay.show();
    },

    hide: function() {
        this.$overlay.hide();
    }
};

function showMessage(title, message) {
    $('#messageModal .modal-title').text(title);
    $('#messageContent').text(message);
    $('#messageModal').modal('show');
    Overlay.hide();
}
