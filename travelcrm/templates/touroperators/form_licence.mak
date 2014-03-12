<div class="dl40 easyui-dialog"
    title="${title}"
    data-options="
        modal:true,
        draggable:false,
        resizable:false,
        iconCls:'fa fa-pencil-square-o'
    ">
    ${h.tags.form(request.url, class_="_ajax", autocomplete="off")}
        <div class="form-field">
            <div class="dl15">
                ${h.tags.title(_(u"licence num"), True, "licence_num")}
            </div>
            <div class="ml15">
                ${h.tags.text("licence_num", item.licence_num if item else None, class_="text w20")}
            </div>
        </div>
        <div class="form-field">
            <div class="dl15">
                ${h.tags.title(_(u"date from"), True, "date_from")}
            </div>
            <div class="ml15">
                ${h.fields.date_field(item.date_from if item else None, "date_from")}
            </div>
        </div>
        <div class="form-field">
            <div class="dl15">
                ${h.tags.title(_(u"date to"), True, "date_to")}
            </div>
            <div class="ml15">
                ${h.fields.date_field(item.date_to if item else None, "date_to")}
            </div>
        </div>
        <div class="form-buttons">
            <div class="dl20 status-bar"></div>
            <div class="ml20 tr button-group">
                ${h.tags.submit('save', _(u"Save"), class_="button")}
                ${h.common.reset('cancel', _(u"Cancel"), class_="button danger")}
            </div>
        </div>
    ${h.tags.end_form()}
</div>
