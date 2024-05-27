/**Get the element with the class .ganancia, in this case
 * this class is from a td
 * Note: I think the code maybe can be optimized, becouse creating a function main and call them
 * but we can do that in a new file.
 */
const celda=document.querySelectorAll(".ganancia");

fetch('http://127.0.0.1:5000/apiTable')
.then((res)=>res.json())
.then((res)=>{
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

    console.log(VentaPato);
    console.log(VentaCocodrilo);
    console.log(VentaTiendaLaBorrega);

    celda.forEach(element => {
        element.innerHTML=listaVentas[i];
        i+=1;
    });
});

/**  We add this function for refresh the element with fetch, than is+
 * similar to AJAX, becouse is asincronic request, and update only any
 * elements
 */
celda.forEach(element => {
    let value=parseFloat(element.innerText);
    if(value>100){
        element.style.backgroundColor="#33DE2B";
    }
    else if(value<=100){
        element.style.backgroundColor="#E83C3C";

    } })

function VentasGet(){
    fetch('http://127.0.0.1:5000/apiTable')
    .then((res)=>res.json())
    .then((res)=>{
        let VentaPato=parseFloat(res['VentaTiendaElPato']);
        let VentaCocodrilo=parseFloat(res['VentaTiendaElCocodrilo']);
        let VentaTiendaLaBorrega=parseFloat(res['VentaTiendaLaBorrega']);
        let VentaTiendaElPatoHORA1=parseFloat(res['VentaTiendaElPatoHORA2']);
        let VentaTiendaElCocodriloHORA2=parseFloat(res['VentaTiendaElCocodriloHORA2']);
        let VentaTiendaLaBorregaHORA2=parseFloat(res['VentaTiendaLaBorregaHORA2']);
        let listaVentas=[VentaPato,VentaCocodrilo,
            VentaTiendaLaBorrega,VentaTiendaElPatoHORA1,
            VentaTiendaElCocodriloHORA2,VentaTiendaLaBorregaHORA2];
        let i=0;

        console.log(VentaPato);
        console.log(VentaCocodrilo);
        console.log(VentaTiendaLaBorrega);

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
        
            } 
        });
    });
};

