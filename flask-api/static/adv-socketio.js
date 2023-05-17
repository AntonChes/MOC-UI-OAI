$(document).ready(function() {

    var bottomShadowClone = $( '.shadow--bottom' ).clone();

    var socket_bot = io.connect(document.domain + ':' + location.port + '/advanced');
    var socket_user = io(document.domain + ':' + location.port + '/advanced/user-input');

    var form = $( 'form#UserInputForm' ).on( 'submit', function( e ) {
        e.preventDefault();
        var user_input = $( 'textarea.user_input' ).val(),
            PreHeader = $( 'textarea#PreHeader' ).val(),
            modelName = $( 'input#modelName' ).attr('data-val'),
            // suffix = $( 'input#suffix' ).val(),
            maxTokens = $( 'input#maxTokens' ).val(),
            Temperature = $( 'input#Temperature' ).val(),
            topP = $( 'input#topP' ).val(),
            // nCompletions = $( 'input#nCompletions' ).val(),
            // stream = $( 'input#stream' ).attr('data-val'),
            // logprobs = $( 'input#logprobs' ).val(),
            // stop = $( 'input#stop' ).val(),
            presencePenalty = $( 'input#presencePenalty' ).val(),
            frequencyPenalty = $( 'input#frequencyPenalty' ).val();
            // bestOf = $( 'input#bestOf' ).val();

        var data = {
          sender_name : 'user',
          message : user_input,
          instruction: PreHeader,
          model_name: modelName,
        //   suffix: suffix,
          max_tokens: parseInt(maxTokens),
          temperature: parseFloat(Temperature),
          top_p: parseInt(topP),
        //   n_completions: parseInt(nCompletions),
        //   stream: Boolean(stream),
        //   logprobs: parseInt(logprobs),
        //   stop: stop,
          presence_penalty: parseFloat(presencePenalty),
          frequency_penalty: parseFloat(frequencyPenalty),
        //   best_of: parseInt(bestOf),
        };
        // console.log(data);

        socket_user.emit('user input (turbo)', data);
        $( 'textarea.user_input' ).val( '' ).focus();
        $( 'div.chat-content div.scroll-content' ).append( '<div class="right-chat-message chat-message"><p>'+data.message+'</p></div>' );
        $( 'div.chat-content div.scroll-content' ).append( '<div class="waiting left-chat-message chat-message"><p>...</p></div>' );
        scrollToElement($( 'div.chat-content div.scroll-content' ), $('.bottomy'));
        console.log('User Request:');        
        console.log(data);   
    });

    socket_user.on('after user input (turbo)', function(data){
        $( 'textarea.user_input' ).prop( "disabled", true );
        $( 'input.orange-btn' ).prop( "disabled", true );
        $( 'input.orange-btn' ).css({"background": "#E2E2E2", "border": "1px solid #E2E2E2"});
        socket_bot.emit('request to bot (turbo)', data);
    });

    socket_bot.on('bot input (turbo)', function(data) {
        $( 'div.waiting' ).remove();
        $( 'div.chat-content div.scroll-content' ).append( '<div class="left-chat-message chat-message"><p>'+data.message+'</p></div>' );
        $( 'textarea.user_input' ).prop( "disabled", false );
        $( 'input.orange-btn' ).prop( "disabled", false );
        $( 'input.orange-btn' ).css({"background": "#F1563C", "border": "1px solid #F1563C"});
        scrollToElement($( 'div.chat-content div.scroll-content' ), $('.bottomy'));
        socket_user.emit('check intent', data);
        console.log('Model Response:');        
        console.log(data);        
    });

    socket_user.on('image found', function(product_url) {
        $( 'div.waiting' ).remove();
        $( 'textarea.user_input' ).prop( "disabled", false );
        $( 'input.orange-btn' ).prop( "disabled", false );
        $( 'input.orange-btn' ).css({"background": "#F1563C", "border": "1px solid #F1563C"});
        $( 'textarea.user_input' ).val( '' ).focus();
        $( 'div.chat-content div.scroll-content' ).append( '<div class="left-chat-message chat-message"><p><img src="'+product_url+'" alt="'+product_url+'"/></p></div></div>' );
        scrollToElement($( 'div.chat-content div.scroll-content' ), $('.bottomy'));
    });

    socket_user.on('product card', function(product_data) {
        $( 'div.waiting' ).remove();
        $( 'textarea.user_input' ).prop( "disabled", false );
        $( 'input.orange-btn' ).prop( "disabled", false );
        $( 'input.orange-btn' ).css({"background": "#F1563C", "border": "1px solid #F1563C"});
        $( 'textarea.user_input' ).val( '' ).focus();
        $( 'div.chat-content div.scroll-content' ).append( '<div class="left-chat-message chat-message"><div class="card product-card"><div class="pimg"><img src="'+product_data.imgUrl+'" alt="'+product_data.imgUrl+'"/></div><div class="ptitle">'+product_data.title+'</div><div class="pprice"><span>Price: </span>$'+product_data.price+'</div><div class="card-btn"><a href="'+product_data.shop_link+'">ADD TO CART</a></div></div></div></div>' );
        scrollToElement($( 'div.chat-content div.scroll-content' ), $('.bottomy'));
    });

    socket_user.on('shopping-cart card', function(product_data) {
      $( 'div.waiting' ).remove();
      $( 'textarea.user_input' ).prop( "disabled", false );
      $( 'input.orange-btn' ).prop( "disabled", false );
      $( 'input.orange-btn' ).css({"background": "#F1563C", "border": "1px solid #F1563C"});
      $( 'textarea.user_input' ).val( '' ).focus();
      $( 'div.chat-content div.scroll-content' ).append( '<div class="left-chat-message chat-message"><div class="card shoppingcart-card"><div class="pimg"><img src="/static/img/cart-icon.svg"/></div><div class="ptitle">Back to shop and check</div><div class="pprice"></div><div class="card-btn"><a href="'+''+'">MY SHOPPING CART</a></div></div></div></div>' );
      // $( 'div.chat-content div.scroll-content' ).append( '<div class="left-chat-message chat-message"><div class="card shoppingcart-card"><div class="ptitle">Back to shop and check</div><div class="card-btn"><a href="'+""+'">MY SHOPPING CART</a></div></div></div>' );
      scrollToElement($( 'div.chat-content div.scroll-content' ), $('.bottomy'));
  });

    // CleaninChatHistory
    var clean_form = $( 'form#CleanChatHistoryForm' ).on( 'submit', function(e) {
      e.preventDefault();
      $( '#chatHistory' ).empty();
      $( 'textarea.user_input' ).prop( "disabled", false );
      $( 'input.orange-btn' ).prop( "disabled", false );
      $( 'input.orange-btn' ).css({"background": "#F1563C", "border": "1px solid #F1563C"});
      // $( '.shadow--bottom' ).css({"opacity": "0"});
      $( '.shadow--bottom' ).replaceWith(bottomShadowClone);
      socket_user.emit('cleaning chat history');
    });

})