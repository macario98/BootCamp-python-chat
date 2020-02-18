
class cargaDatos
{
	constructor(){
		this.$ = document
	}

	mostrarMSG(input = 'div', list = []){
		let e = this.$.querySelector(input)
		e.value = ''
		list.forEach(element => {
			for (const prop in element) {
				let formato = `(${prop}) : ${element[prop]}`
				console.log(formato)
				e.value += `\n${formato}`
			}
		});
	}
	mostrarUser(input = 'div', list = []){
		let e = this.$.querySelector(input)
		e.value = ''
		list.forEach(element => {
			e.value += `\n${element[2]}  -  ${element[1]}  -  ${element[3]}`
			console.log(element)
		});
	}
}
class peticiones extends cargaDatos
{
	constructor(url = 'http://127.0.0.1:8000'){
		super()
		this.url = url
		this.listMSG = []
		this.listUsers = []
	}

	request(path = '/', method='GET', elem='div', callback){
		fetch(this.url+path, {method, mode:'cors'})
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

	getMSG(path = '/'){
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

	getUSERS(path = '/'){
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

let contador = 0
function actualizar(){
	let p = new peticiones()
	contador += 1
	p.getMSG('/msg')
	p.getUSERS('/users')
	console.clear()
	console.log('Peticiones al server:', contador)
}
function enviarMSG(){
	getLocalIPs(function(ips) { // <!-- ips is an array of local IP addresses.
		miIP = ips[0]
		textbox = document.querySelector('#msg')
		let datos = {}
		datos[miIP] = textbox.value
		
		let s = new peticiones()
		s.sendMSG('/', JSON.stringify(datos) )
		textbox.value = ''
		//dato = JSON.stringify({miIP:textbox.value})
		//alert(JSON.stringify(datos))
	});
}

document.querySelector('#Send').onclick = enviarMSG
document.querySelector('#msg').onkeydown = enter
function enter(e){
	if (e.keyCode === 13 && !e.shiftKey) {
		//e.preventDefault();
		enviarMSG()
		alert('Enter')
	}
}
setInterval(actualizar, 8000)