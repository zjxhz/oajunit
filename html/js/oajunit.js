function hideAllTables(){
    $('.table-tests').hide();
}
function showTable(locator, text){
    hideAllTables();
    $(locator).show(1000);
    if(text)
        $('#category').text(text);
}

function hideAllButTrend(){
    hideAllTables();
    showTable('#table_trend');
}

window.addEventListener('load', hideAllButTrend);