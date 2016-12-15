//import d3 from 'd3';
//import { colorScalerFactory } from '../javascripts/modules/colors';

const $ = require('jquery');
//d3.tip = require('d3-tip');

//require('./heatmapx.css');
// https://cdn.plot.ly/plotly-latest.js
//require('../vendor/plotly-latest.js');
//<script type="text/javascript" src="https://cdn.plot.ly/plotly-latest.min.js"></script>


function heatmapxVis(slice) {
  function refresh() {
    //$('#code').attr('rows', '15');
    $.getJSON(slice.jsonEndpoint(), function (payload) {
      const data = payload.data;
//      slice.container.html('');
//      var traces = [{x: data.y, y: data.x, z: data.z, type: 'heatmap', colorscale: 'Viridis', showscale: true}];
//      Plotly.newPlot(slice.containerId, traces);

//      const url = slice.render_template(payload.form_data.url);
      slice.container.html('<iframe style="width:100%;" frameBorder="0"></iframe>');
      const iframe = slice.container.find('iframe');
      iframe.css('height', slice.height());
      iframe.attr('src', data.url);

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

//function heatmap3Vis(slice) {
//  function refresh() {
//    // Header for panel in explore v2
//    const header = document.getElementById('slice-header');
//    const headerHeight = header ? 30 + header.getBoundingClientRect().height : 0;
//    const margin = {
//      top: headerHeight,
//      right: 10,
//      bottom: 35,
//      left: 35,
//    };
//
//
//    d3.json(slice.jsonEndpoint(), function (error, payload) {
//      if (error) {
//        slice.error(error.responseText, error);
//        return;
//      }
//      const data = payload.data;
//      slice.container.html('');
//      const fd = payload.form_data;
//      const container = d3.select(slice.selector);
//
//
//      //const url = slice.render_template(payload.form_data.url);
//      slice.container.html('<iframe style="width:100%;"></iframe>');
//      const iframe = slice.container.find('iframe');
//      iframe.css('height', slice.height());
//      iframe.attr('src', data.filepath);
//      //var traces = [{x: data.y, y: data.x, z: data.z, type: 'heatmap', colorscale: 'Viridis', showscale: true}];
//
//      //Plotly.newPlot(slice.containerId, traces);
//      slice.done(payload);
//    });
//  }
//  return {
//    render: refresh,
//    resize: refresh,
//  };
//}

module.exports = heatmapxVis;
