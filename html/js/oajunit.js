function hideAllTables(){
	$('.table-tests').css('display','none');
}
function showTable(locator){
	hideAllTables();
	$(locator).css('display','initial')
}