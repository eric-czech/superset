const $ = require('jquery');

function imageVis(slice) {
  function refresh() {
    $.getJSON(slice.jsonEndpoint(), function (payload) {
      const data = payload.data;
      const url = data.url + '?date=' + Date.now()
      slice.container.html('<img src="' + url + '">');
      //const iframe = slice.container.find('iframe');
      //iframe.css('height', slice.height());
      //iframe.attr('src', url);
      //console.log('Loading plotly iframe at "' + url + '"');
      slice.done(payload);
    })
    .fail(function (xhr) {
      slice.error(xhr.responseText, xhr);
    });
  }

  return {
    render: refresh,
    resize: refresh,
  };
}

module.exports = imageVis;
