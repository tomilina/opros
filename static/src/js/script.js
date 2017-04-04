function call_ajax(id)
{
    var countries = document.getElementById("country");
    var country_id = countries.options[countries.selectedIndex].value;
    var regions = document.getElementById("region");

    odoo.define('opros.region', function (require)
    {
        'use strict';
        var ajax = require('web.ajax');
        ajax.jsonRpc('/ajax/region', 'call', {
            'param' : country_id,
        }).always(function (data) {
            //то что передал контроллер
            var info = data;
//            alert(data);
            document.getElementById("region").innerHTML='';
            if (info.length!=0){
                var regions=document.getElementById('region');
                for(var i=0; i < info.length; i++)
                {
                    //создем option
                    var option = document.createElement('option');
                    option.innerHTML = info[i].name;
                    var value = document.createAttribute("value");
                    value.value=info[i].id
                    option.setAttributeNode(value);
                    //option.value = info[i].id;

                    //добавляем к select
                    regions.appendChild(option);
                }
            }
            else{
                    //создем option
                    var option = document.createElement('option');
                    option.value = "";
                    option.innerHTML = "Регион...";
                    option.disabled = "disabled";
                    //добавляем к select
                    regions.appendChild(option);
            }

        });
    });
};
