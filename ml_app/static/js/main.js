// ml_app/static/js/main.js
$(document).ready(function () {
    // Tooltip initializer - Common for all pages
    $('[data-toggle="tooltip"]').tooltip();

    // Range input event handler - Common for all pages
    $('input[type="range"]').on('input', function () {
        var id = $(this).attr('id');
        $('#' + id + '_value').text($(this).val());
    });

    // Code specific to datasets.html
    if ($('#feature-descriptions').length > 0) { // Only run if we're on the datasets page
        console.log($('#feature-descriptions').attr('data-value'));
        var featureDescriptions = JSON.parse($('#feature-descriptions').attr('data-value'));

        function plotGraph(feature) {
            var graphData = JSON.parse($('#' + feature + '-data').text());
            var config = { displayModeBar: false };
            Plotly.newPlot('graph', graphData.data, graphData.layout, config);
        }
        // Handle window resize
        $(window).resize(function () {
            Plotly.Plots.resize('graph');
        });
        function updateDescription(feature) {
            $('#feature-description').text(featureDescriptions[feature]);
        }

        var initialFeature = $('#feature-selection').val();
        plotGraph(initialFeature);
        updateDescription(initialFeature);

        $('#feature-selection').change(function () {
            var selectedFeature = $(this).val();
            plotGraph(selectedFeature);
            updateDescription(selectedFeature);
        });
    }

    if ($('#forecast_chart').length > 0) { // Only run if we're on the Time Series page
        console.log($('#forecast_chart').data('traces'));
        var traces = ($('#forecast_chart').data('traces'));
        var config = { displayModeBar: false };
        Plotly.newPlot('forecast_chart', traces, { responsive: true }, config);

        // Handle window resize
        $(window).resize(function () {
            Plotly.Plots.resize('forecast_chart');
        });
    }

    if ($('#cluster_chart').length > 0) { // Only run if we're on the K-means page
        console.log($('#cluster_chart').data('plot'));
        var plotData = $('#cluster_chart').data('plot');
        var xAxis = $('#cluster_chart').data('xaxis');
        var yAxis = $('#cluster_chart').data('yaxis');
        var config = { displayModeBar: false };
        var layout = {
            title: 'Clusters',
            xaxis: { title: xAxis },
            yaxis: { title: yAxis }
        };
        Plotly.newPlot('cluster_chart', plotData, layout, config);

        // Handle window resize
        $(window).resize(function () {
            Plotly.Plots.resize('cluster_chart');
        });
    }

});