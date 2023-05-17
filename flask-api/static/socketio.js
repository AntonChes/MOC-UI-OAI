$(document).ready(function() {

    var socket_bot = io.connect(document.domain + ':' + location.port + '/');
    var socket_user = io(document.domain + ':' + location.port + '/user-input');

    var form = $( 'form' ).on( 'submit', function( e ) {
        e.preventDefault();
        var user_input = $( 'textarea.user_input' ).val(),
            PreHeaderName = $( 'input#PreHeaderName' ).val(),
            modelName = $( 'input#modelName' ).attr('data-val'),
            suffix = $( 'input#suffix' ).val(),
            maxTokens = $( 'input#maxTokens' ).val(),
            Temperature = $( 'input#Temperature' ).val(),
            topP = $( 'input#topP' ).val(),
            nCompletions = $( 'input#nCompletions' ).val(),
            stream = $( 'input#stream' ).attr('data-val'),
            logprobs = $( 'input#logprobs' ).val(),
            stop = $( 'input#stop' ).val(),
            presencePenalty = $( 'input#presencePenalty' ).val(),
            frequencyPenalty = $( 'input#frequencyPenalty' ).val(),
            bestOf = $( 'input#bestOf' ).val();

        var data = {
          sender_name : 'User',
          message : user_input,
          preheader_name: PreHeaderName,
          model_name: modelName,
          suffix: suffix,
          max_tokens: parseInt(maxTokens),
          temperature: parseFloat(Temperature),
          top_p: parseInt(topP),
          n_completions: parseInt(nCompletions),
          stream: Boolean(stream),
          logprobs: parseInt(logprobs),
          stop: stop,
          presence_penalty: parseFloat(presencePenalty),
          frequency_penalty: parseFloat(frequencyPenalty),
          best_of: parseInt(bestOf),
        };
        console.log(data);

        socket_user.emit('user input', data);
        $( 'textarea.user_input' ).val( '' ).focus();
        $( 'div.chat-content div.scroll-content' ).append( '<div class="left-chat-message chat-message"><p>'+data.message+'</p></div>' );
        $( 'div.chat-content div.scroll-content' ).append( '<div class="waiting right-chat-message chat-message"><p>...</p></div>' );
        scrollToElement($( 'div.chat-content div.scroll-content' ), $('.bottomy'));
    });

    socket_user.on('after user input', function(data){
        $( 'textarea.user_input' ).prop( "disabled", true );
        $( 'input.orange-btn' ).prop( "disabled", true );
        $( 'input.orange-btn' ).css({"background": "#E2E2E2", "border": "1px solid #E2E2E2"});
        socket_bot.emit('request to bot', data);
    });

    socket_bot.on('bot input', function(data) {
        $( 'div.waiting' ).remove();
        $( 'div.chat-content div.scroll-content' ).append( '<div class="right-chat-message chat-message"><p>'+data.message+'</p></div>' );
        $( 'textarea.user_input' ).prop( "disabled", false );
        $( 'input.orange-btn' ).prop( "disabled", false );
        $( 'input.orange-btn' ).css({"background": "#F1563C", "border": "1px solid #F1563C"});
        scrollToElement($( 'div.chat-content div.scroll-content' ), $('.bottomy'));
    });

    socket_user.on('image found', function(product_url) {
        $( 'div.waiting' ).remove();
        $( 'textarea.user_input' ).prop( "disabled", false );
        $( 'input.orange-btn' ).prop( "disabled", false );
        $( 'input.orange-btn' ).css({"background": "#F1563C", "border": "1px solid #F1563C"});
        $( 'textarea.user_input' ).val( '' ).focus();
        $( 'div.chat-content div.scroll-content' ).append( '<div class="right-chat-message chat-message"><p><img src="'+product_url+'" alt="'+product_url+'"/></p></div></div>' );
        scrollToElement($( 'div.chat-content div.scroll-content' ), $('.bottomy'));
    });

})