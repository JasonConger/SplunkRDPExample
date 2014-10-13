require([
    'underscore',
    'jquery',
    'splunkjs/mvc',
    'splunkjs/mvc/tableview',
    'splunkjs/mvc/simplexml/ready!'
], function(_, $, mvc, TableView) {
    
    var CustomIconRenderer = TableView.BaseCellRenderer.extend({
        canRender: function(cell) {
            return cell.field === 'Server';
        },
        render: function($td, cell) {
            
            var server = cell.value;
            
            $td.html(_.template('<a href="/custom/TemplateForXenApp/rdp/connect?server=<%- server%>" title="RDP to server: <%- server%>"><img src="/static/app/TemplateForXenApp/images/rdp.png" /></a> <%- server%>', {
                server: server
            }));
        }
    });
    
    mvc.Components.get('tblServers').getVisualization(function(tableView) {
        
        // Register custom cell renderer
        tableView.table.addCellRenderer(new CustomIconRenderer());

        // Force the table to re-render
        tableView.table.render();
    });
    
});
