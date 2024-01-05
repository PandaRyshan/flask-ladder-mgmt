var Overlay = {
    $overlay: $('<div id="overlay"></div>').appendTo('body'),
    
    show: function() {
        this.$overlay.show();
    },

    hide: function() {
        this.$overlay.hide();
    }
};
