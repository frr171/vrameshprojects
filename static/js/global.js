$(function() {
  // Auto-Fit videos
  $("div").fitVids();
  $("img").css("max-width", "100%");

  // Carousel background images
  $(".carousel .item").each(function(index) {
    $(this).css('background-image', "url(" + $(this).attr('data-image') + ")");
  })
})
