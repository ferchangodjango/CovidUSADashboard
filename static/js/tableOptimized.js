const celda=document.querySelectorAll(".ganancia");

/*Define the function for  manipuling the data
Than the fetch get from the any API
*/
function GetDataApi(res){
    let VentaPato=parseFloat(res['VentaTiendaElPato']);
    let VentaCocodrilo=parseFloat(res['VentaTiendaElCocodrilo']);
    let VentaTiendaLaBorrega=parseFloat(res['VentaTiendaLaBorrega']);
    let VentaTiendaElPatoHORA2=parseFloat(res['VentaTiendaElPatoHORA2']);
    let VentaTiendaElCocodriloHORA2=parseFloat(res['VentaTiendaElCocodriloHORA2']);
    let VentaTiendaLaBorregaHORA2=parseFloat(res['VentaTiendaLaBorregaHORA2']);
    let listaVentas=[VentaPato,VentaCocodrilo,
        VentaTiendaLaBorrega,VentaTiendaElPatoHORA2,
        VentaTiendaElCocodriloHORA2,VentaTiendaLaBorregaHORA2];
    let i=0;

    celda.forEach(element => {
        element.innerHTML=listaVentas[i];
        i+=1;
    });

    celda.forEach(element => {
        let value=parseFloat(element.innerText);
        if(value>100){
            element.style.backgroundColor="#33DE2B";
        }
        else if(value<=100){
            element.style.backgroundColor="#E83C3C";
    
        } })    
}

//Get the data for first time
fetch('http://127.0.0.1:5000/apiTable')
.then((res)=>res.json())
.then((res)=>GetDataApi(res));

//
function VentasGet(){
    fetch('http://127.0.0.1:5000/apiTable')
    .then((res)=>res.json())
    .then((res)=>GetDataApi(res));
};