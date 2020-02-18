class loadData
{
	constructor(){
		this.$ = document.querySelector
	}
	showMSG(input = 'tbody', list=[]){
		let e = this.$(input)
		e.value = ''

	}
}



class request
{
	constructor(url = 'http://127.0.0.1:8000'){
		this.url = url
		this.lisMSG = []
		this.listUSER = []
	}

	MSG(path = '/'){
		fetch(this.url+path, {mode:'cors'})
		.then( (response) => {
			return response.json()
		})
		.then( (data) =>{
			data.forEach(mensaje => {
				console.log('Peticiones')
				this.listMSG.push(mensaje)
			});
			console.log(this.listMSG)
			this.mostrarMSG('#listMSG', this.listMSG)
		})
	}

	USERS(path = '/'){
		fetch(this.url+path, {mode:'cors'})
		.then( (response) => {
			return response.json()
		})
		.then( (data) =>{
			data.forEach(mensaje => {
				console.log('Peticiones')
				this.listUsers.push(mensaje)
			});
			console.log(this.listUsers)
			this.mostrarUser('#listUSER', this.listUsers)
		})
	}

	sendMSG(path='/', data=''){
		fetch(this.url+path, {method:'POST', body:data, mode:'cors'})
		.then( (response) => {
			return response.text()
		})
		.then( (data) =>{
			// data.forEach(mensaje => {
			// 	console.log('Peticiones')
			// 	this.listUsers.push(mensaje)
			// });
			// console.log(this.listUsers)
			// this.mostrarUser('#listUSER', this.listUsers)
			alert(data)
		})
	}
}




function enter(event) {
	if (event.keyCode === 13 && !event.shiftKey) {
		enviarMSG()
		alert('Enter')
	}
}