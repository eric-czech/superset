import d3 from 'd3';
import { colorScalerFactory } from '../javascripts/modules/colors';

const $ = require('jquery');
d3.tip = require('d3-tip');

//require('./heatmapx.css');
// https://cdn.plot.ly/plotly-latest.js
//require('../vendor/plotly-latest.js');
//<script type="text/javascript" src="https://cdn.plot.ly/plotly-latest.min.js"></script>


function MGDSRXLinearVis(slice) {
  function refresh() {
    // Header for panel in explore v2
    const header = document.getElementById('slice-header');
    const headerHeight = header ? 30 + header.getBoundingClientRect().height : 0;
    const margin = {
      top: headerHeight,
      right: 10,
      bottom: 35,
      left: 35,
    };


    d3.json(slice.jsonEndpoint(), function (error, payload) {
      if (error) {
        slice.error(error.responseText, error);
        return;
      }
      const data = payload.data;
      slice.container.html('');
      const fd = payload.form_data;
      const container = d3.select(slice.selector);

      var traces = [{x: data.y, y: data.x, z: data.z, type: 'heatmap', colorscale: 'Viridis', showscale: true}];

      Plotly.newPlot(slice.containerId, traces);

      slice.done(payload);
    });
  }
  return {
    render: refresh,
    resize: refresh,
  };
}

module.exports = MGDSRXLinear;
