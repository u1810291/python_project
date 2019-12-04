// catalogue list
(function() {
    var selectedCatalogueTags = [];
    var defaultTag = parseInt($('[data-catalogue-list] li.active a').data('tag-id'));
    if($.inArray(defaultTag, selectedCatalogueTags) == -1) {
        selectedCatalogueTags.push(defaultTag);
    }
    var currentPage = 0;
    var itemsOnPage = 20;
    function updateShops() {
        var $catalogueItems = $('[data-catalogue-item]');

        // filter
        $catalogueItems.each(function(index, element) {
            var tags = $(element).data('tags').toString().split('|');
            var selectedTags = tags.filter(function(value) {
                return selectedCatalogueTags.indexOf(parseInt(value)) != -1;
            });

            if(selectedCatalogueTags.length > 0 && selectedTags.length <= 0) {
                $(element).hide();
            }else{
                $(element).show();
            }
        });

        // pagination
        var $visibleCatalogueItems = $('[data-catalogue-item]:visible');
        var totalItems = $visibleCatalogueItems.length;
        $visibleCatalogueItems.slice(currentPage, (1+currentPage)*itemsOnPage).show();
        $visibleCatalogueItems.slice((1+currentPage)*itemsOnPage).hide();
        var currentNumItems = $('[data-catalogue-item]:visible').length;

        // toggle show more button
        var $showMoreButton = $('[data-catalogue-show-more]');
        if(totalItems == currentNumItems) {
            $showMoreButton.hide();
        }else{
            $showMoreButton.show();
        }

        $('[data-catalogue-item]:visible').each(function(index, element) {
            var $lazyImage = $(element).find('.thumbnail').find('.lazy-image');
            if(!$lazyImage.data('is-loaded')) {
                $lazyImage.attr('src', $lazyImage.data('src'));
                $lazyImage.attr('data-is-loaded', true);
            }
        });

    }
    updateShops();

    $(document).on('click', "[data-catalogue-list] > li > a, [data-catalogue-list-mobile] > li > a", function(event){
        var $link = $(this);
        var $item = $link.closest('li');
        var currentTagId = $link.data('tag-id');

        if($.inArray(currentTagId, selectedCatalogueTags) == -1) {
            $('[data-catalogue-list] > li, [data-catalogue-list-mobile] > li').removeClass('active');
            selectedCatalogueTags = [parseInt(currentTagId)];
            $item.addClass('active');
        }
        updateShops();
        currentPage = 0;
        return event.preventDefault();
    });

    $(document).on('click', "[data-catalogue-list-mobile] > li > a", function(event){
        var name = $(this).clone().children().remove().end().text();
        $(this).closest('.navbar').find('.navbar-category-brand').text(name);
        $("html, body").animate({ scrollTop: $('#myCarousel').prop("scrollHeight") }, "slow");
    });

    $(document).on('click', "[data-catalogue-list] > li > a", function(event){
        var name = $(this).clone().children().remove().end().text();
        $('.catalogue-title').text(name);
        $("html, body").animate({ scrollTop: $('#myCarousel').prop("scrollHeight") }, "slow");
    });


    $(document).on('click', "[data-catalogue-show-more]", function(event){
        currentPage += 1
        updateShops();
        return event.preventDefault();
    });
})();


// thumbnail hint
$(function($) {
    $('[data-catalogue-item]').on({
        mouseenter: function () {
            $(this).find('.thumbnail-hint').show();
        },
        mouseleave: function () {
            $(this).find('.thumbnail-hint').hide();
        }
    });
});



// carusel swipe
$(function($) {
    var distanceX = 0;
    var beginX = 0;
    var endX = 0;
    var maxClickDistance = 30;
    $("#myCarousel .item a")
    .mousedown(function(event) {
        beginX = event.pageX;
        return event.preventDefault();
    })
    .click(function(event) {
        if(Math.abs(distanceX) > maxClickDistance) {
            var direction = "next";
            if(distanceX > 0 ) {
                direction = "prev";
            }
            $("#myCarousel").carousel(direction);
            return event.preventDefault();
        }
    })
    .mouseup(function(event) {
        endX = event.pageX;
        distanceX = endX - beginX;
        return event.preventDefault();
    });
});

// affix menu
$(function($) {
    function ready() {
        var selector = '.category-menu-desktop div[data-spy="affix"]';
        var headerHeight = $(selector).offset().top;
        var headerHeight = $('#myCarousel').outerHeight(true);
        var footerHeight = $('.ss-gradient-section').innerHeight();
        console.log(headerHeight + 100);
        $('.category-menu-desktop div[data-spy="affix"]').affix({
            offset: {
                top: headerHeight + 100,
                bottom: footerHeight + 200
            }
        }).on('affix.bs.affix', function () {
            $(this).css({
                'width': $(this).outerWidth()
            });
        }).on('affix-bottom.bs.affix', function () {
            $(this).css('bottom', 'auto');
        });
    }
    $(document).ready(ready);
   // $(window).on('page:load', ready);
});

// affix mobile menu
$(function($) {
    var selector = '.category-menu-mobile .container-fluid[data-spy="affix"]';
    var width = $(selector).width();
    $(selector).affix({
        offset: {
            top: $(selector).offset().top
        }
    });
});