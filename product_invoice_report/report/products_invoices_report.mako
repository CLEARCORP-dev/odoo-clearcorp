<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
		<style type="text/css">
        	.overflow_ellipsis {
            text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap;
        }
        ${css}
    </style>
	</head>
    <body> 
		<%setLang(user.lang)%>
		<%get_groups_report = get_group_lines(data)%>
		<div style="font-size: 20px; font-weight: bold; text-align: center;"> ${company.partner_id.name}</div>
        <div style="font-size: 25px; font-weight: bold; text-align: center;"> ${_('Products Invoices Report')}</div>
    	<div class="act_as_table data_table">
        	<div class="act_as_row labels">
            	<div class="act_as_cell">
                            %if get_filter(data) == 'filter_date':
                                ${_('Dates Filter')}
                            %elif get_filter(data) == 'filter_period': 
                                ${_('Periods Filter')}
                            %elif get_filter(data) == '':
                                ${_('Filter')}
                             %elif get_filter(data) == 'filter_no':
                                ${_('Filter')}
                            %endif
            	</div>
            	<div class="act_as_cell">${_('Group By')}</div>
        	</div>
        	<div class="act_as_row">
        		<div class="act_as_cell">
                            %if get_filter(data) == 'filter_date':
                                ${_('From:')}
                                ${get_date_from(data)}                               
                            %elif get_filter(data) == 'filter_period':
                                ${_('From:')}
                                ${data['form']['period_from'][1]}
                            %elif get_filter(data) == '':
                                ${_('No apply')}                             
                            %elif get_filter(data) == 'filter_no':
                                ${_('No apply')}
                            %endif                              
                            %if get_filter(data) == 'filter_date':
                                ${_('To:')}
                                ${get_date_to(data)}                         
                            %elif get_filter(data) == 'filter_period':
                                ${_('To:')}
                                ${data['form']['period_to'][1]}                  
                            %endif 
            	</div>
            	<div class="act_as_cell">
                    	 %if get_sort(data) == 'sort_date':
                    	 	${_('Date Invoice')}
                    	 %elif get_sort(data) == 'sort_period':
                    	 	${_('Period')}
                    	 %elif get_sort(data) == 'sort_partner':
                    		${_('Customer')}
                    	%elif get_sort(data) == 'sort_product_category':
							${_('Category Product')}
                		%elif get_sort(data) == 'sort_product':
                			${_('Product')}
                		%else:
                			${_('No')}
                		%endif
            	</div>
        	</div>
    	</div>	

    	<div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>      
    		<div class="act_as_table list_table" style="">
        		<div class="act_as_thead" style="vertical-align: right;">
            		<div class="act_as_row labels" style="font-weight: bold; text-align:left;font-size: 13px;">
                    	 %if get_sort(data) != 'sort_date':
                    	<div class="act_as_cell" style="width:8%;">${_('Date Invoice')}</div>
                    	%endif                
                    	<div class="act_as_cell" style="width:11%;">${_('Invoice')}</div>
                    	%if get_sort(data) != 'sort_partner':
                    	<div class="act_as_cell" style="width:12%;">${_('Customer')}</div>
                    	%endif
                    	%if get_sort(data) != 'sort_product_category':
                    	<div class="act_as_cell" style="width:12%">${_('Category Product')}</div>
                    	%endif
                		%if  get_sort(data) != 'sort_product':
                		<div class="act_as_cell" style="width:12%">${_('Product')}</div>
                		%endif
                		<div class="act_as_cell amount" style="width:7%">${_('Quantity')}</div>
                		<div class="act_as_cell amount" style="width:12%">${_('Price Unit')}</div>
                		<div class="act_as_cell amount" style="width:12%">${_('Discount')}</div>
                		<div class="act_as_cell amount" style="width:14%">${_('Total')}</div>
					</div>
				</div>
			<div/>
			
			%for group in get_groups_report:
    		<%quantity,subtotal = get_quantities_group(group,data)%>  
    		<div class="act_as_table list_table" style="">
        		<div class="act_as_thead" style="vertical-align: right;">
            		<div class="act_as_row labels" style="font-weight: bold; text-align:left;font-size: 12px;">
                    	 %if get_sort(data) == 'sort_date':
                    	 <div class="act_as_cell">${group[0]['date_invoice'] or ''}</div>
                    	 %elif get_sort(data) == 'sort_period':
                    	 <div class="act_as_cell">${group[0]['period_id'] or ''}</div>
                    	 %elif get_sort(data) == 'sort_partner':
                    	 <div class="act_as_cell">${group[0]['partner_id'] or ''}</div>
                    	 %elif get_sort(data) == 'sort_product':
                    	 <div class="act_as_cell">${group[0]['product_id'] or ''}</div>
                    	 %elif get_sort(data) == 'sort_product_category':
                    	 <div class="act_as_cell">${group[0]['categ_id'] or ''}</div>            
						%endif
					</div>
				</div>
			<div/>
	
			<div class="act_as_table list_table" style="">
        	%for line in group:
        		<div class="act_as_tbody" style="vertical-align: right;">
            		<div class="act_as_row lines" style="font-weight:normal; text-align:left;font-size: 12px;">
                    	%if get_sort(data) != 'sort_date':
                    	<div class="act_as_cell" style="width:8%;">${line['date_invoice'] or ''}</div>   
                    	%endif                
                    	<div class="act_as_cell" style="width:11%;">${line['number'] or ''}</div>
                    	%if get_sort(data) != 'sort_partner':
                    	<div class="act_as_cell" style="width:12%;">${line['partner_id'] or ''}</div>
                    	%endif
                    	%if get_sort(data) != 'sort_product_category':
                    	<div class="act_as_cell" style="width:12%">${line['categ_id'] or ''}</div>
                    	%endif
                		%if get_sort(data) != 'sort_product':
                		<div class="act_as_cell" style="width:12%">${line['product_id'] or ''}</div>
                		%endif
                		<div class="act_as_cell amount" style="width:7%">${line['quantity'] or '0.0'}</div>
                		<div class="act_as_cell amount" style="width:12%">${line['price_unit']  or '0.0'}</div>
                		<div class="act_as_cell amount" style="width:12%">${line['discount'] or '0.0'}</div>
                		<div class="act_as_cell amount" style="width:14%">${line['subtotal'] or '0.0'}</div>	
					</div>
				</div>
			%endfor
				<div class="act_as_row lines" style="font-weight: bold;font-size: 12px">
            			%if get_sort(data) != 'sort_date':
                    	<div class="act_as_cell"></div> 
                    	%endif                
                    	<div class="act_as_cell"></div>
                    	%if get_sort(data) != 'sort_partner':
                    	<div class="act_as_cell"></div>
                    	%endif
                    	%if get_sort(data) != 'sort_product_category':
                    	<div class="act_as_cell"></div>
                    	%endif
                		%if get_sort(data) != 'sort_product':
                		<div class="act_as_cell"></div>
                		%endif
            			<div class="act_as_cell amount">${quantity or '0.0'}</div>
                        <div class="act_as_cell amount"></div>
                        <div class="act_as_cell amount"></div>
                        <div class="act_as_cell amount">${subtotal or '0.0'}</div>
            	</div>
			<div/>
			%endfor
				
    </body>

</html>
