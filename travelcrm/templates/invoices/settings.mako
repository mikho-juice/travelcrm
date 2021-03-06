<div class="dl50 easyui-dialog"
    title="${title}"
    data-options="
        modal:true,
        draggable:false,
        resizable:false,
        iconCls:'fa fa-pencil-square-o'
    ">
    ${h.tags.form(request.url, class_="_ajax", autocomplete="off")}
        <div class="easyui-tabs h100" data-options="border:false,height:300">
            <div title="${_(u'Main')}">
                <div class="form-field mb05">
                    <div class="dl15">
                        ${h.tags.title(_(u"active days"), True, "active_days")}
                    </div>
                    <div class="ml15">
                          ${h.tags.text(
                              'active_days',
                              rt.settings.get("active_days") if rt.settings else None,
                              class_='easyui-numberspinner',
                              data_options='min:1,editable:false' 
                          )}
                          ${h.common.error_container(name='actual_days')}
                    </div>
                </div>
            </div>
            <div title="${_(u'HTML template')}">
                ${h.tags.textarea(
                    'html_template', 
                    rt.settings.get("html_template") if rt.settings else None,
                    class_="rich-text-editor",
                    cols=73,
                    rows=18,
                )}
                <script>
                    $('textarea[name=html_template]').ace({lang: 'html'});
                </script>
            </div>
        </div>
        <div class="form-buttons">
            <div class="dl20 status-bar"></div>
            <div class="ml20 tr button-group">
                ${h.tags.submit('save', _(u"Save"), class_="button easyui-linkbutton")}
                ${h.common.reset('cancel', _(u"Cancel"), class_="button danger easyui-linkbutton")}
            </div>
        </div>
    ${h.tags.end_form()}
</div>
