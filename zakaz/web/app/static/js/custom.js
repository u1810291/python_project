$(function($) {
    function activeForm(formSelector, onSuccess) {
        var $form = $(formSelector);
        var $submitButton = $form.find('[data-button="submit"]');
        var url = $form.attr('action');
        var method = $form.attr('method');
        var csrftoken = $('meta[name=csrf-token]').attr('content')

        $submitButton.click(function(event) {
            $submitButton.prop('disabled', true);
            $.ajax(url, {
                method: method,
                data: $form.serializeJSON(),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                beforeSend: function(xhr, settings){
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken)
                    }
                    $form.find('[data-field-error]').empty().hide();
                },
                success: function(data, textStatus, jqXHR) {
                    onSuccess(data, textStatus, jqXHR, $form, $submitButton);
                },
                error: function(response) {
                    var json = response.responseJSON;
                    if($.isArray(json)) {
                        // todo: rewrite this shit
                        json.forEach(function(itemData, i) {
                            var $activeItems = $form.find('[data-active-form-item]');
                            for(var field in itemData) {
                                var $errorField = $activeItems.eq(i).find('[name$="'+field+']"]').parent().find('[data-field-error]');
                                $errorField.html(itemData[field]).show();
                            }
                        });
                    } else {
                        for(var field in json) {
                            var $errorField = $form.find('[name="'+field+'"]').parent().find('[data-field-error]');
                            $errorField.html(json[field]).show();
                        }
                    }
                    $submitButton.prop('disabled', false);
                }
            });
            return event.preventDefault();
        });
    }

    /**
     * Create & Init Ajax Forms
     */

    // Sign In form
    activeForm('#signin_modal form', function(data, textStatus, jqXHR, $form, $submitButton) {
        window.location.reload();
    });

    // Restore password form
    activeForm('#restore_password_modal form', function(data, textStatus, jqXHR, $form, $submitButton) {
        var dataSuccessModal = $submitButton.data('success-modal');
        $('.modal').modal('hide');
        $(dataSuccessModal).modal('show');
    });

    // Consolidation form
    activeForm('form.consolidation-service-form[data-active-form]', function(data, textStatus, jqXHR, $form, $submitButton) {
        var nextUrl = $form.data('next');
        window.location.href = nextUrl;
    });

    // purchase form
    activeForm('form.purchase-service-form[data-active-form]', function(data, textStatus, jqXHR, $form, $submitButton) {
        var nextUrl = $form.data('next');
        window.location.href = nextUrl;
    });

    // Sign In 2 form
    activeForm('#signin2_modal form', function(data, textStatus, jqXHR, $form, $submitButton) {
        window.location.reload();
    });

    // User info form
    activeForm('form.user_info_form[data-active-form]', function(data, textStatus, jqXHR, $form, $submitButton) {
        var nextUrl = $form.data('next');
        window.location.href = nextUrl;
    });
    $('form.user_info_form [data-action-enable-checkout]').change(function() {
        var $form = $('form.user_info_form[data-active-form]');
        var $submitButton = $form.find('[data-button="submit"]');
        if(this.checked) {
            $submitButton.prop('disabled', false);
        }else{
            $submitButton.prop('disabled', true);
        }
    });
});

