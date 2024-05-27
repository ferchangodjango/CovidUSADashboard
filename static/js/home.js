
function SendValuesInsert(csrf){

    const firstName=document.getElementById('FIRSTNAME').value;
    const lastName=document.getElementById('LASTNAME').value;
    const feedEmployed=document.getElementById('FEET').value;
    const commisionEmployed=document.getElementById('COMMISION').value;
    const idtEmployed=document.getElementById('IDT').value;
    const idfEmployed=document.getElementById('IDF').value;

    fetch('http://127.0.0.1:5000/apiInsert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-TOKEN': csrf
        },
        body: JSON.stringify({
            'FIRSTNAME':firstName,
            'LASTNAME':lastName,
            'FEET':feedEmployed,
            'COMMISION':commisionEmployed,
            'IDT':idtEmployed,
            'IDF':idfEmployed
        })
      }).then(response => response.json())
      .then(data => {console.log('Success:', data)})
}

function DeleteValuesSend(csrf){
  const firstName=document.getElementById('FIRSTNAME').value;
  const lastName=document.getElementById('LASTNAME').value;
  const feedEmployed=document.getElementById('FEET').value;
  const commisionEmployed=document.getElementById('COMMISION').value;
  const idtEmployed=document.getElementById('IDT').value;
  const idfEmployed=document.getElementById('IDF').value;

  fetch('http://127.0.0.1:5000/apiDelete',{
    method:'DELETE',
    headers:{
      'Content-type':'application/json',
      'X-CSRF-TOKEN':csrf
    },
    body:JSON.stringify({
      "FIRSTNAME":firstName,
      "LASTNAME":lastName
    })
  })
    .then((res)=>res.json())
    .then((data)=>console.log('Success',data));
};