requirejs.config({
    baseUrl: '/lib',
    paths: {
        jquery: 'jquery/jquery-3.5.1.min'
    }
});

requirejs(['jquery'], function( $ ) {
    console.log( $ )
});
