function populateResults(data) {
  $('#recommendations_list').children().remove();
  $.each(data, function(i, x) {
    if (i < 20) {
      $('#recommendations_list').append('<li><div class="recommendation_entry"><span class="recommendation_label">'+x[0]+'</span></div></li>')
    }
  })
}

function getRatings() {
  // FIXME cleaner way to construct query?
  var ratings_list = $('input[type=radio].first-star').map(function(i, x) {
    movie_id = x.name.split('_')[0]
    num_stars = $(x).data('rating').rater.children().filter('.star-rating-on').length
    if (num_stars == 0) {
      return [[movie_id, null]];
    } else {
      return [[movie_id, num_stars]]
    }
  });
  ratings_query = {}
  ratings_list.each(function(i, x) {
    if (x[1] == null) {
      ratings_query[x[0]] = null;
    } else {
      ratings_query[x[0]] = String(x[1]);
    }
  });

  $.ajax({
    type: 'post',
    url: '/predict',
    data: JSON.stringify(ratings_query),
    contentType: 'application/json',
    dataType: 'json',
    success: populateResults
  });
}

$(document).ready(function() {
    $('.stars').rating(
      { 
        callback: getRatings
      }
    );
});

