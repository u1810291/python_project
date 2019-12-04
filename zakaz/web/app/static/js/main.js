$(function(){

    function prettifyInput(event){
        var $parent = $(this).parent();
        var className = 'input--filled';

        if($(this).val()) {
            $parent.addClass(className);
            if(event.type  == 'focusout') {
                $parent.find('[data-field-error]').empty().hide();
            }
        } else {
            $parent.removeClass(className);
        }


    }

    $('input,textarea').ready(prettifyInput);
    $(document).on('blur', 'input,textarea', prettifyInput);

    $("a.showPass").click(function(event){
        event.preventDefault();
        var $passwordInputs = $("[name='password_confirm'], [name='password']");

        // Handle depending on state
        if ($passwordInputs.attr('type') === 'password'){
            var newType = 'text';
            var message = $(this).data('shown-message');
        } else {
            var newType = 'password';
            var message = $(this).data('hidden-message');
        }

        $passwordInputs.attr('type', newType);

        // Update inner text as well
        $(this).text(message);
    });


    $("[data-button='add-product']").click(function(event){
        event.preventDefault();

        var $form = $(".form-block");
        var $firstForm = $form.filter(':first-child').clone();
        var $container = $(document.createElement('div'), {"class": "form-block"});
        var $new = $container.append($firstForm);

        // Append clonned content
        $new.find('.from-block-alert-box').html('');
        $new.find('.from-block-alert-box').hide();
        $new.find('input').attr('value', '');
        $new.find('textarea').html('');
        $new.find('input,textarea').closest('.pretty-form__item-content').removeClass('input--filled');
        $new.find('input,textarea').closest('.pretty-form__item-content').find('[data-field-error]').empty().hide();

        $form.last().after($new.html());

        // Update indexes
        $(".form-block").each(function(index){
            $(this).attr('data-form-index', index);
        });

        // Update counters
        $(".product-index-counter").each(function(index){
            $(this).text(index + 1);
        });
    });

    $(document).on('click', "[data-button='product-remove']", function(event){
        event.preventDefault();
        var $form = $(this).closest('.form-block');

        // Make sure it's not first form
        if ($form.data('form-index') != ''){
            $form.hide(100, function(){
                $(this).removeClass('form-block').empty();

                // Update counters
                $(".product-index-counter").each(function(index){
                    $(this).text(index + 1);
                });
            });
        }
    });
});
