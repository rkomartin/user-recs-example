function getRatings() {
  // construct the query by collecting all of the observed ratings, and by
  // marking all of the un-rated items with null
  ratings_query = {}
  $('input[type=radio].first-star').each(function(i, x) {
    movie_id = x.name.split('_')[0]
    num_stars = $(x).data('rating').rater.children().filter('.star-rating-on').length
    if (num_stars === 0) {
      ratings_query[movie_id] = null;
    } else {
      ratings_query[movie_id] = String(num_stars)
    }
  });

  // make the call to the server to get the recommendations
  $.ajax({
    type: 'post',
    url: '/recommend',
    data: JSON.stringify(ratings_query),
    contentType: 'application/json',
    dataType: 'json',
    success: populateResults
  });
}

function populateResults(data) {
  $('#recommendations_list').children().remove();
  $.each(data, function(i, x) {
    if (i < 20) {
      $('#recommendations_list').append('<li><div class="recommendation_entry"><span class="recommendation_label">'+x[0]+'</span></div></li>')
    }
  })
}

$(document).ready(function() {
    $('.stars').rating(
      { 
        callback: getRatings
      }
    );
});

