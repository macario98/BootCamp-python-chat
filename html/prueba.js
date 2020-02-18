function createTableMSG(list = []) {
	template = ``;
	list.forEach(element =>{
		template += `
		<tr>
			<td>${element.ip}</td>
			<td>${element.m}</td>
		</tr>
		`;
	})
	document.querySelector('#tblmsg').innerHTML = template;
}
function createTableUSER(list = []) {
	template = ``;
	list.forEach(element =>{
		template += `
		<tr>
			<td>${element.user}</td>
			<td>${element.ip}</td>
		</tr>
		`;
	})
	document.querySelector('#tbluser').innerHTML = template;
}


function test(){
	user = [{user: 'mac', ip:'192.168.1.2'},{user: 'hd', ip:'192.168.45.12'}]
	createTableUSER(user);
	msg = [{ip:'192.168.1.1', m:'hola'}]
	createTableMSG(msg)
}
test()
