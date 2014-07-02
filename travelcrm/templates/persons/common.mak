<%def name="persons_selector(name='person_id', values=[], can_edit=True)">
    <%
        _func_id = h.common.gen_id()
        _id = h.common.gen_id()
        _storage_id = h.common.gen_id()
        _tb_id = "tb-%s" % _id
    %>
    % if can_edit:
    <script type="text/javascript">
        function add_${_func_id}(input_id){
            var id = $('#' + input_id).combogrid('getValue');
            if(is_int(id)){
                var input = $('<input type="hidden" name="${name}">').val(id);
                input.appendTo('#${_storage_id}');
                $('#' + input_id).combogrid('clear');
                $('#${_id}').datagrid('reload');
            }
            return false;
        }
        function delete_${_func_id}(grid_id){
            var rows = get_checked($('#' + grid_id));
            $.each(rows, function(i, row){
                $('#${_storage_id} input[name=${name}][value=' + row.id + ']').remove();
            });
            $('#' + grid_id).datagrid('reload');
            return false;
        }
    </script>
    % endif
    <script type="text/javascript">
        function formatter_${_func_id}(index, row){
            var html = '<table width="100%" class="grid-details">';
            if(row.phone){
                html += '<tr>'
                    + '<td width="25%" class="b">${_(u'phone')}</td>'
                    + '<td>' + row.phone + '</td>'
                    + '</tr>';
            }
            if(row.email){
                html += '<tr>'
                    + '<td width="25%" class="b">${_(u'email')}</td>'
                    + '<td>' + row.email + '</td>'
                    + '</tr>';
            }
            if(row.skype){
                html += '<tr>'
                    + '<td width="25%" class="b">${_(u'skype')}</td>'
                    + '<td>' + row.skype + '</td>'
                    + '</tr>';
            }
            if(row.customer_citizen_passport){
                html += '<tr>'
                    + '<td width="25%" class="b">${_(u'citizen passport')}</td>'
                    + '<td>' + row.customer_citizen_passport + '</td>'
                    + '</tr>';
            }
            if(row.customer_foreign_passport){
                html += '<tr>'
                    + '<td width="25%" class="b">${_(u'foreign passport')}</td>'
                    + '<td>' + row.customer_foreign_passport + '</td>'
                    + '</tr>';
            }
            html += '</table>';
            return html;
        }
    </script>
    <table class="easyui-datagrid"
        id="${_id}"
        data-options="
            url:'/persons/list',border:false,
            singleSelect:true,
            rownumbers:true,sortName:'id',sortOrder:'desc',
            idField:'_id',checkOnSelect:false,
            selectOnCheck:false,toolbar:'#${_tb_id}',
            view: detailview,
            onExpandRow: function(index, row){
                var row_id = 'row-${_id}-' + row.id;
                $('#' + row_id).load(
                    '/persons/details?id=' + row.id, 
                    function(){
                        $('#${_id}').datagrid('fixDetailRowHeight', index);
                        $('#${_id}').datagrid('fixRowHeight', index);
                    }
                );
            },
            detailFormatter: function(index, row){
                var row_id = 'row-${_id}-' + row.id;
                return '<div id=' + row_id + '></div>';
            },          
            onBeforeLoad: function(param){
                var id = [0];
                $.each($('#${_storage_id} input[name=${name}]'), function(i, el){
                    id.push($(el).val());
                });
                param.id = id.join();                            
                param.rows = 0;
                param.page = 0;
            }
        " width="100%">
        <thead>
            % if can_edit:
                <th data-options="field:'_id',checkbox:true">${_(u"id")}</th>
            % endif
            <th data-options="field:'id',sortable:true,width:60">${_(u"id")}</th>
            <th data-options="field:'name',sortable:true,width:200">${_(u"name")}</th>
            <th data-options="field:'birthday',sortable:true,width:100">${_(u"birthday")}</th>
            <th data-options="field:'age',sortable:true,width:60">${_(u"age")}</th>
        </thead>
    </table>
    <div id="${_storage_id}">
        % for person in values:
            ${h.tags.hidden(name, person)}
        % endfor
    </div>
    % if can_edit:
    <div class="datagrid-toolbar" id="${_tb_id}">
        <div class="actions button-container dl40">
            <div style="display: inline-block;padding-top:2px;">
                <%
                    f_id = h.common.gen_id()
                %>
                ${h.fields.persons_combobox_field(request, None, f_id, id=f_id)}
            </div>
            <div class="button-group minor-group ml1">
                <a href="#" class="button" onclick="add_${_func_id}('${f_id}');">${_(u"Add")}</a>
                % if 'edit' in h.permisions.get_persons_permisions(request):
                <a href="#" class="button _action" 
                    data-options="
                        container:'#${_id}',action:'dialog_open',url:'/persons/edit',property:'with_row'
                    ">
                    ${_(u"Edit")}</a>
                % endif
                <a href="#" class="button danger" onclick="delete_${_func_id}('${_id}');">${_(u"Delete")}</a>
            </div>
        </div>
        <div class="ml35 tr" style="padding-top: 5px;">
            ${h.common.error_container(name=name)}
        </div>
    </div>
    % endif
</%def>